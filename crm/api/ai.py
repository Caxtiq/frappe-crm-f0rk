"""AI API endpoints for Frappe CRM"""

import frappe
from frappe import _
from typing import Optional, Dict, Any, List

from crm.ai.ai_service import get_ai_service
from crm.ai.prompts import (
	SYSTEM_PROMPTS,
	email_composer_prompt,
	lead_scoring_prompt,
	deal_analysis_prompt,
	activity_summary_prompt,
	sentiment_analysis_prompt,
)
from crm.ai.utils import (
	get_lead_context,
	get_deal_context,
	format_ai_response,
	save_ai_conversation,
	save_ai_suggestion,
)


@frappe.whitelist()
def chat(message: str, reference_doctype: Optional[str] = None, reference_name: Optional[str] = None):
	"""
	General chat with AI assistant
	
	Args:
		message: User message
		reference_doctype: Optional doctype for context (CRM Lead, CRM Deal, etc.)
		reference_name: Optional document name for context
	"""
	ai = get_ai_service()
	
	if not ai.is_enabled():
		frappe.throw(_("AI is not enabled. Please configure AI settings in CRM AI Settings."))
	
	# Get context if reference is provided
	context = None
	if reference_doctype and reference_name:
		if reference_doctype == "CRM Lead":
			context = get_lead_context(reference_name)
		elif reference_doctype == "CRM Deal":
			context = get_deal_context(reference_name)
	
	# Send message to AI
	messages = [{"role": "user", "content": message}]
	response = ai.chat(messages, system_prompt=SYSTEM_PROMPTS["assistant"], context=context)
	
	# Save conversation
	if reference_doctype and reference_name:
		save_ai_conversation(reference_doctype, reference_name, message, response, "chat")
	
	return format_ai_response(response)


@frappe.whitelist()
def compose_email(
	recipient_name: str,
	company: str,
	purpose: str,
	tone: str = "professional",
	reference_doctype: Optional[str] = None,
	reference_name: Optional[str] = None,
):
	"""
	AI-powered email composition
	
	Args:
		recipient_name: Name of the email recipient
		company: Company name
		purpose: Purpose of the email
		tone: Email tone (professional, friendly, urgent, etc.)
		reference_doctype: Optional reference doctype for context
		reference_name: Optional reference name for context
	"""
	ai = get_ai_service()
	
	if not ai.is_enabled():
		frappe.throw(_("AI is not enabled. Please configure AI settings."))
	
	# Get context if available
	context = None
	if reference_doctype and reference_name:
		if reference_doctype == "CRM Lead":
			context = get_lead_context(reference_name)
		elif reference_doctype == "CRM Deal":
			context = get_deal_context(reference_name)
	
	# Generate prompt
	prompt = email_composer_prompt(recipient_name, company, purpose, tone, context)
	
	# Get AI response
	response = ai.complete(prompt, system_prompt=SYSTEM_PROMPTS["email_composer"])
	
	# Save as conversation
	if reference_doctype and reference_name:
		save_ai_conversation(reference_doctype, reference_name, prompt, response, "email_compose")
	
	return format_ai_response(response, "email")


@frappe.whitelist()
def score_lead(lead_name: str):
	"""
	AI-powered lead scoring and qualification
	
	Args:
		lead_name: Name of the CRM Lead document
	"""
	ai = get_ai_service()
	
	if not ai.is_enabled():
		frappe.throw(_("AI is not enabled. Please configure AI settings."))
	
	# Get lead data
	lead = frappe.get_doc("CRM Lead", lead_name)
	
	lead_data = {
		"name": lead.lead_name,
		"organization": lead.organization,
		"industry": lead.industry,
		"annual_revenue": lead.annual_revenue,
		"no_of_employees": lead.no_of_employees,
		"source": lead.source,
		"email": lead.email,
		"status": lead.status,
	}
	
	# Generate scoring prompt
	prompt = lead_scoring_prompt(lead_data)
	
	# Get AI analysis
	response = ai.complete(prompt, system_prompt=SYSTEM_PROMPTS["lead_scorer"])
	
	# Save as suggestion
	save_ai_suggestion("CRM Lead", lead_name, "Lead Score", response)
	
	return format_ai_response(response, "analysis")


@frappe.whitelist()
def analyze_deal(deal_name: str):
	"""
	AI-powered deal analysis and recommendations
	
	Args:
		deal_name: Name of the CRM Deal document
	"""
	ai = get_ai_service()
	
	if not ai.is_enabled():
		frappe.throw(_("AI is not enabled. Please configure AI settings."))
	
	# Get deal data
	deal = frappe.get_doc("CRM Deal", deal_name)
	
	deal_data = {
		"organization": deal.organization_name or deal.organization,
		"deal_value": deal.deal_value,
		"status": deal.status,
		"probability": deal.probability,
		"expected_closure_date": deal.expected_closure_date,
		"next_step": deal.next_step,
		"industry": deal.industry,
		"deal_owner": deal.deal_owner,
	}
	
	# Generate analysis prompt
	prompt = deal_analysis_prompt(deal_data)
	
	# Get AI analysis
	response = ai.complete(prompt, system_prompt=SYSTEM_PROMPTS["deal_analyzer"])
	
	# Save as suggestion
	save_ai_suggestion("CRM Deal", deal_name, "Deal Analysis", response)
	
	return format_ai_response(response, "analysis")


@frappe.whitelist()
def summarize_activities(reference_doctype: str, reference_name: str, limit: int = 10):
	"""
	AI-powered activity summarization
	
	Args:
		reference_doctype: Doctype (CRM Lead, CRM Deal, etc.)
		reference_name: Document name
		limit: Number of recent activities to summarize
	"""
	ai = get_ai_service()
	
	if not ai.is_enabled():
		frappe.throw(_("AI is not enabled. Please configure AI settings."))
	
	# Get recent activities
	activities = frappe.get_all(
		"Comment",
		filters={
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"comment_type": "Comment",
		},
		fields=["content", "creation", "owner", "comment_type"],
		order_by="creation desc",
		limit=limit,
	)
	
	# Also get tasks
	tasks = frappe.get_all(
		"CRM Task",
		filters={"reference_doctype": reference_doctype, "reference_name": reference_name},
		fields=["title", "description", "status", "due_date"],
		limit=limit,
	)
	
	# Format activities for summarization
	activity_list = []
	for activity in activities:
		activity_list.append({
			"type": "Comment",
			"description": activity.content,
			"date": str(activity.creation),
		})
	
	for task in tasks:
		activity_list.append({
			"type": "Task",
			"description": f"{task.title}: {task.description or ''}",
			"date": str(task.due_date) if task.due_date else "",
		})
	
	# Generate summary prompt
	prompt = activity_summary_prompt(activity_list)
	
	# Get AI summary
	response = ai.complete(prompt, system_prompt=SYSTEM_PROMPTS["activity_summarizer"])
	
	# Save conversation
	save_ai_conversation(reference_doctype, reference_name, "Summarize activities", response, "summary")
	
	return format_ai_response(response, "summary")


@frappe.whitelist()
def analyze_sentiment(text: str, reference_doctype: Optional[str] = None, reference_name: Optional[str] = None):
	"""
	AI-powered sentiment analysis
	
	Args:
		text: Text to analyze
		reference_doctype: Optional reference doctype
		reference_name: Optional reference name
	"""
	ai = get_ai_service()
	
	if not ai.is_enabled():
		frappe.throw(_("AI is not enabled. Please configure AI settings."))
	
	# Generate sentiment analysis prompt
	prompt = sentiment_analysis_prompt(text)
	
	# Get AI analysis
	response = ai.complete(prompt, system_prompt=SYSTEM_PROMPTS["sentiment_analyzer"])
	
	# Save if reference is provided
	if reference_doctype and reference_name:
		save_ai_conversation(reference_doctype, reference_name, f"Analyze sentiment: {text[:100]}", response, "sentiment")
	
	return format_ai_response(response, "sentiment")


@frappe.whitelist()
def get_conversation_history(reference_doctype: str, reference_name: str, limit: int = 20):
	"""
	Get AI conversation history for a document
	
	Args:
		reference_doctype: Doctype (CRM Lead, CRM Deal, etc.)
		reference_name: Document name
		limit: Number of conversations to fetch
	"""
	conversations = frappe.get_all(
		"CRM AI Conversation",
		filters={
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
		},
		fields=["name", "user_message", "ai_response", "conversation_type", "creation", "user"],
		order_by="creation desc",
		limit=limit,
	)
	
	return conversations


@frappe.whitelist()
def get_suggestions(reference_doctype: str, reference_name: str, suggestion_type: Optional[str] = None):
	"""
	Get AI suggestions for a document
	
	Args:
		reference_doctype: Doctype (CRM Lead, CRM Deal, etc.)
		reference_name: Document name
		suggestion_type: Optional filter by suggestion type
	"""
	filters = {
		"reference_doctype": reference_doctype,
		"reference_name": reference_name,
	}
	
	if suggestion_type:
		filters["suggestion_type"] = suggestion_type
	
	suggestions = frappe.get_all(
		"CRM AI Suggestion",
		filters=filters,
		fields=["name", "suggestion_type", "suggestion", "status", "creation", "metadata"],
		order_by="creation desc",
	)
	
	return suggestions


@frappe.whitelist()
def accept_suggestion(suggestion_name: str):
	"""Accept an AI suggestion"""
	suggestion = frappe.get_doc("CRM AI Suggestion", suggestion_name)
	suggestion.status = "Accepted"
	suggestion.save(ignore_permissions=True)
	return {"success": True}


@frappe.whitelist()
def reject_suggestion(suggestion_name: str, reason: Optional[str] = None):
	"""Reject an AI suggestion"""
	suggestion = frappe.get_doc("CRM AI Suggestion", suggestion_name)
	suggestion.status = "Rejected"
	if reason:
		suggestion.rejection_reason = reason
	suggestion.save(ignore_permissions=True)
	return {"success": True}
