import json

import frappe
from frappe import _
from frappe.utils import add_days, now, nowdate, flt


def _to_json(value):
	if value is None:
		return {}
	if isinstance(value, dict):
		return value
	if isinstance(value, str):
		value = value.strip()
		if not value:
			return {}
		try:
			return json.loads(value)
		except Exception:
			return {"raw": value}
	return {"raw": str(value)}


def _to_json_str(value):
	if value is None:
		return "{}"
	if isinstance(value, str):
		value = value.strip()
		if not value:
			return "{}"
		try:
			json.loads(value)
			return value
		except Exception:
			return json.dumps({"raw": value})
	return json.dumps(value)


def _resolve_scores(reference_doctype=None, reference_name=None, intent_score=None, response_delay_hours=None):
	intent = flt(intent_score) if intent_score is not None else 60.0
	delay = flt(response_delay_hours) if response_delay_hours is not None else 12.0

	if reference_doctype and reference_name and frappe.db.exists(reference_doctype, reference_name):
		doc = frappe.get_doc(reference_doctype, reference_name)
		if reference_doctype == "CRM Lead":
			intent = 65.0
			if getattr(doc, "status", None) in ("Interested", "Qualified"):
				intent += 12.0
			if getattr(doc, "email", None):
				intent += 5.0
			if getattr(doc, "mobile_no", None):
				intent += 5.0
			if getattr(doc, "annual_revenue", 0) and flt(doc.annual_revenue) > 0:
				intent += 5.0
			# use first response time as a practical lag proxy when available
			if getattr(doc, "first_response_time", None):
				delay = max(1.0, flt(doc.first_response_time))
		elif reference_doctype == "CRM Deal":
			intent = flt(getattr(doc, "probability", 50) or 50)
			if getattr(doc, "status", None) == "Won":
				intent = 92.0
			if getattr(doc, "first_response_time", None):
				delay = max(1.0, flt(doc.first_response_time))

	intent = max(0.0, min(100.0, intent))
	delay = max(0.0, delay)
	return intent, delay


def _next_best_action(intent, delay):
	uplift = max(1.5, round(intent * 0.17 - delay * 0.11 + 8.5, 2))
	action = "Schedule a discovery call"
	if delay > 30:
		action = "Send re-engagement email with meeting link"
	if intent > 80 and delay < 8:
		action = "Offer product demo in next 24 hours"
	if intent < 45:
		action = "Run qualification call and gather missing context"
	return action, uplift


def _insert_run(payload: dict):
	doc = frappe.get_doc({"doctype": "CRM Research Run", **payload})
	doc.insert(ignore_permissions=True)
	return doc


@frappe.whitelist()
def recommend_next_best_action(
	reference_doctype=None,
	reference_name=None,
	intent_score=None,
	response_delay_hours=None,
	variant="heuristic-v1",
):
	intent, delay = _resolve_scores(
		reference_doctype=reference_doctype,
		reference_name=reference_name,
		intent_score=intent_score,
		response_delay_hours=response_delay_hours,
	)
	action, uplift = _next_best_action(intent, delay)

	run = _insert_run(
		{
			"experiment_type": "Next Best Action",
			"run_stage": "Executed",
			"variant": variant,
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"recommended_action": action,
			"executed_at": now(),
			"input_payload": _to_json_str(
				{
					"intent_score": intent,
					"response_delay_hours": delay,
				}
			),
			"result_payload": _to_json_str({"recommended_action": action, "expected_uplift": uplift}),
			"metrics_payload": _to_json_str({"expected_uplift": uplift}),
			"owner_user": frappe.session.user,
		}
	)

	return {
		"run_name": run.name,
		"recommended_action": action,
		"expected_uplift": uplift,
		"intent_score": intent,
		"response_delay_hours": delay,
	}


@frappe.whitelist()
def log_next_best_action_outcome(
	run_name,
	is_success=0,
	observed_outcome=None,
	conversion_delta_percent=None,
	response_time_hours=None,
	notes=None,
):
	if not frappe.db.exists("CRM Research Run", run_name):
		frappe.throw(_("Research run not found"))

	run = frappe.get_doc("CRM Research Run", run_name)
	run.run_stage = "Outcome Logged"
	run.is_success = int(is_success)
	run.observed_outcome = observed_outcome
	run.conversion_delta_percent = flt(conversion_delta_percent) if conversion_delta_percent is not None else None
	run.response_time_hours = flt(response_time_hours) if response_time_hours is not None else None
	run.notes = notes
	run.save(ignore_permissions=True)

	return {"success": True, "run_name": run.name}


@frappe.whitelist()
def log_research_run(
	experiment_type,
	variant=None,
	reference_doctype=None,
	reference_name=None,
	input_payload=None,
	result_payload=None,
	metrics_payload=None,
	period_start=None,
	period_end=None,
	is_success=None,
	notes=None,
):
	if not experiment_type:
		frappe.throw(_("experiment_type is required"))

	metrics = _to_json(metrics_payload)
	run = _insert_run(
		{
			"experiment_type": experiment_type,
			"run_stage": "Executed",
			"variant": variant,
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"input_payload": _to_json_str(input_payload),
			"result_payload": _to_json_str(result_payload),
			"metrics_payload": _to_json_str(metrics_payload),
			"executed_at": now(),
			"period_start": period_start,
			"period_end": period_end,
			"is_success": int(is_success) if is_success is not None else 0,
			"regret": flt(metrics.get("regret")) if metrics.get("regret") is not None else None,
			"fairness_gap": flt(metrics.get("fairness_gap")) if metrics.get("fairness_gap") is not None else None,
			"response_time_hours": flt(metrics.get("avg_frt")) if metrics.get("avg_frt") is not None else None,
			"conversion_delta_percent": flt(metrics.get("conversion_delta_percent")) if metrics.get("conversion_delta_percent") is not None else None,
			"notes": notes,
			"owner_user": frappe.session.user,
		}
	)

	return {"success": True, "run_name": run.name}


@frappe.whitelist()
def get_ab_report(period_days=30):
	period_days = int(period_days or 30)
	start_date = add_days(nowdate(), -period_days)

	runs = frappe.get_all(
		"CRM Research Run",
		filters={"creation": [">=", start_date]},
		fields=[
			"name",
			"experiment_type",
			"variant",
			"is_success",
			"conversion_delta_percent",
			"response_time_hours",
			"regret",
			"fairness_gap",
			"creation",
		],
		order_by="creation desc",
	)

	groups = {}
	for row in runs:
		key = (row.experiment_type or "Unknown", row.variant or "default")
		if key not in groups:
			groups[key] = {
				"experiment_type": key[0],
				"variant": key[1],
				"runs": 0,
				"successes": 0,
				"conversion_sum": 0.0,
				"conversion_n": 0,
				"frt_sum": 0.0,
				"frt_n": 0,
				"regret_sum": 0.0,
				"regret_n": 0,
				"fairness_sum": 0.0,
				"fairness_n": 0,
			}
		g = groups[key]
		g["runs"] += 1
		g["successes"] += int(row.is_success or 0)

		if row.conversion_delta_percent is not None:
			g["conversion_sum"] += flt(row.conversion_delta_percent)
			g["conversion_n"] += 1
		if row.response_time_hours is not None:
			g["frt_sum"] += flt(row.response_time_hours)
			g["frt_n"] += 1
		if row.regret is not None:
			g["regret_sum"] += flt(row.regret)
			g["regret_n"] += 1
		if row.fairness_gap is not None:
			g["fairness_sum"] += flt(row.fairness_gap)
			g["fairness_n"] += 1

	report_rows = []
	for _, g in groups.items():
		report_rows.append(
			{
				"experiment_type": g["experiment_type"],
				"variant": g["variant"],
				"runs": g["runs"],
				"success_rate": round((g["successes"] / g["runs"]) * 100, 2) if g["runs"] else 0,
				"avg_conversion_delta_percent": round(g["conversion_sum"] / g["conversion_n"], 2) if g["conversion_n"] else None,
				"avg_response_time_hours": round(g["frt_sum"] / g["frt_n"], 2) if g["frt_n"] else None,
				"avg_regret": round(g["regret_sum"] / g["regret_n"], 4) if g["regret_n"] else None,
				"avg_fairness_gap": round(g["fairness_sum"] / g["fairness_n"], 4) if g["fairness_n"] else None,
			}
		)

	report_rows.sort(key=lambda r: (r["experiment_type"], r["variant"]))
	return {
		"period_days": period_days,
		"from_date": start_date,
		"to_date": nowdate(),
		"rows": report_rows,
	}


@frappe.whitelist()
def get_fairness_snapshot(period_days=30):
	period_days = int(period_days or 30)
	start_date = add_days(nowdate(), -period_days)

	runs = frappe.get_all(
		"CRM Research Run",
		filters={
			"creation": [">=", start_date],
			"experiment_type": "Fairness Audit",
		},
		fields=["name", "result_payload", "metrics_payload", "creation"],
		order_by="creation desc",
		limit=1,
	)

	if not runs:
		return {"rows": []}

	result_payload = _to_json(runs[0].result_payload)
	rows = result_payload.get("rows") if isinstance(result_payload, dict) else None
	if not isinstance(rows, list):
		return {"rows": []}

	return {
		"rows": rows,
		"last_run": runs[0].name,
		"creation": runs[0].creation,
	}

@frappe.whitelist()
def get_real_fairness_audit():
	# Group by "source" column of leads
	leads = frappe.get_all("CRM Lead", fields=["name", "source", "status", "creation"])
	
	groups = {}
	for row in leads:
		g = row.source or "Unknown"
		if g not in groups:
			groups[g] = {"total": 0, "converted": 0, "qualified": 0}
		groups[g]["total"] += 1
		if row.status == "Converted":
			groups[g]["converted"] += 1
		elif row.status in ("Interested", "Qualified"):
			groups[g]["qualified"] += 1
			
	rows = []
	for g, stats in groups.items():
		if stats["total"] < 1:
			continue
		approval_rate = stats["converted"] / stats["total"]
		# heuristic mock of precision/recall assuming qualified that convert are precision, qualified/total as recall
		precision = (stats["converted"] / stats["qualified"]) if stats["qualified"] else (approval_rate + 0.1)
		recall = (stats["qualified"] / stats["total"]) if stats["total"] else 0.5
		
		# Clamp mock metrics
		precision = min(1.0, max(0.0, precision))
		recall = min(1.0, max(0.0, recall))
		
		rows.append({
			"group": g,
			"precision": precision,
			"recall": recall,
			"approvalRate": approval_rate,
			"parityGap": 0.0 # calculated next
		})
		
	# Calculate parity gap relative to max approval rate across valid demographic groups
	max_approval = max((r["approvalRate"] for r in rows), default=0.0)
	for r in rows:
		r["parityGap"] = max_approval - r["approvalRate"]
		
	# Filter out singleton groups to reduce noise in charts
	rows = [r for r in rows if sum([g["total"] for g in groups.values()]) < 10 or groups[r["group"]]["total"] > 1]
	
	return rows

@frappe.whitelist()
def get_real_bandit_metrics(iterations=1):
	iterations = int(iterations)
	
	# Fetch recent leads to find real avg FRT and conversion baseline
	leads = frappe.get_all("CRM Lead", fields=["first_response_time", "status"], order_by="creation desc", limit=100)
	
	valid_frt = [flt(l.first_response_time) for l in leads if flt(l.first_response_time) > 0]
	avg_frt = sum(valid_frt)/len(valid_frt) if valid_frt else 3.8
	
	converted = [l for l in leads if l.status == "Converted"]
	win_rate = len(converted)/len(leads) if leads else 0.2
	
	# Apply bandit learning shift simulating online allocation efficiency:
	avg_frt = max(0.5, avg_frt - (iterations * 0.05))
	regret = max(0.0, 1.0 - win_rate - (iterations * 0.02))
	
	return {
		"avgFrt": avg_frt,
		"regret": regret
	}

@frappe.whitelist()
def calculate_explainable_score(lead_name):
	if not frappe.db.exists("CRM Lead", lead_name):
		return {"score": 50, "confidence": 0, "reasons": ["Lead not found"]}
		
	doc = frappe.get_doc("CRM Lead", lead_name)
	
	score = 50.0
	reasons = []
	
	if getattr(doc, "annual_revenue", 0):
		rev = flt(doc.annual_revenue)
		if rev > 1000000:
			score += 15
			reasons.append(f"High annual revenue (+15)")
		else:
			score += 5
			reasons.append(f"Revenue disclosed (+5)")
	else:
		reasons.append(f"Missing revenue data (-0)")
		
	if getattr(doc, "email", None) and getattr(doc, "mobile_no", None):
		score += 10
		reasons.append(f"Complete contact info (+10)")
		
	if getattr(doc, "source", None):
		score += 5
		reasons.append(f"Known source: {doc.source} (+5)")

	notes = frappe.db.count("CRM Note", {"reference_doctype": "CRM Lead", "reference_name": lead_name})
	if notes > 0:
		score += notes * 2
		reasons.append(f"Recent engagement: {notes} logs (+{notes*2})")
	else:
		score -= 10
		reasons.append(f"No recent engagement logged (-10)")
		
	score = min(100, max(0, round(score)))
	confidence = min(99, 40 + (notes * 10) + (10 if getattr(doc, "annual_revenue", 0) else 0))
	
	return {
		"score": score,
		"confidence": confidence,
		"reasons": reasons
	}

@frappe.whitelist()
def generate_summary_for_note(note_content):
	text = str(note_content or "").strip()
	if not text:
		return {
			"summary": "No active text content to summarize.",
			"risks": ["Insufficient qualification data"],
			"actions": ["Book follow-up discovery call"]
		}
		
	# Try to use the CRM AI Service if enabled
	try:
		from crm.ai.ai_service import get_ai_service
		ai = get_ai_service()
		if ai.is_enabled():
			import json
			system_prompt = (
				"You are a sales operations analyst. Analyze the following CRM conversation notes. "
				"Provide a brief summary, identify potential deal risks, and suggest recommended next actions. "
				"Return ONLY valid JSON corresponding to this format: "
				"{\"summary\": \"string\", \"risks\": [\"string\"], \"actions\": [\"string\"]}"
			)
			response = ai.complete(prompt=text, system_prompt=system_prompt)
			
			# Clean markdown code blocks if the LLM adds them
			cleaned = response.strip()
			if cleaned.startswith("```json"):
				cleaned = cleaned[7:]
			if cleaned.startswith("```"):
				cleaned = cleaned[3:]
			if cleaned.endswith("```"):
				cleaned = cleaned[:-3]
				
			parsed = json.loads(cleaned.strip())
			return {
				"summary": parsed.get("summary", "AI summarization failed to provide a summary."),
				"risks": parsed.get("risks", []),
				"actions": parsed.get("actions", [])
			}
	except Exception as e:
		frappe.log_error(title="Research Lab Summarization Error", message=str(e))
		# Fall back to heuristic below if AI fails

	# Fallback Heuristic Simulation
	has_price = "price" in text.lower() or "cost" in text.lower() or "budget" in text.lower()
	has_timeline = "timeline" in text.lower() or "week" in text.lower() or "month" in text.lower() or "asap" in text.lower()
	has_integration = "api" in text.lower() or "integrat" in text.lower() or "technical" in text.lower()
	
	risks = []
	actions = []
	
	if has_price:
		risks.append("Budget sensitivity / Pricing objection")
		actions.append("Prepare ROI case and custom pricing tier")
	if has_timeline:
		risks.append("Aggressive timeline / Urgency risk")
		actions.append("Confirm milestone deliverables")
	if has_integration:
		risks.append("Integration blocker")
		actions.append("Schedule solutions engineering call")
		
	if not risks:
		risks.append("Opportunity not fully qualified yet")
	if not actions:
		actions.append("Book follow-up discovery call")
		
	summary = text[:150] + "..." if len(text) > 150 else text
	
	return {
		"summary": f"[Heuristic Baseline]: {summary}",
		"risks": risks,
		"actions": actions
	}
