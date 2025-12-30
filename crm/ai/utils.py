"""Utility functions for AI module"""

import frappe
from typing import Dict, Any, Optional, List
import json


def get_lead_context(lead_name: str) -> Dict[str, Any]:
	"""Get context for a lead"""
	lead = frappe.get_doc("CRM Lead", lead_name)
	
	context = {
		"lead_name": lead.lead_name,
		"organization": lead.organization,
		"email": lead.email,
		"mobile_no": lead.mobile_no,
		"status": lead.status,
		"source": lead.source,
		"industry": lead.industry,
		"annual_revenue": lead.annual_revenue,
		"no_of_employees": lead.no_of_employees,
	}
	
	# Get recent activities
	activities = frappe.get_all(
		"Comment",
		filters={
			"reference_doctype": "CRM Lead",
			"reference_name": lead_name,
			"comment_type": "Comment",
		},
		fields=["content", "creation", "owner"],
		order_by="creation desc",
		limit=5,
	)
	context["recent_activities"] = activities
	
	return context


def get_deal_context(deal_name: str) -> Dict[str, Any]:
	"""Get context for a deal"""
	deal = frappe.get_doc("CRM Deal", deal_name)
	
	context = {
		"organization": deal.organization_name or deal.organization,
		"deal_value": deal.deal_value,
		"currency": deal.currency,
		"status": deal.status,
		"deal_owner": deal.deal_owner,
		"probability": deal.probability,
		"expected_closure_date": deal.expected_closure_date,
		"next_step": deal.next_step,
		"source": deal.source,
		"industry": deal.industry,
	}
	
	# Get recent activities
	activities = frappe.get_all(
		"Comment",
		filters={
			"reference_doctype": "CRM Deal",
			"reference_name": deal_name,
			"comment_type": "Comment",
		},
		fields=["content", "creation", "owner"],
		order_by="creation desc",
		limit=5,
	)
	context["recent_activities"] = activities
	
	return context


def get_contact_context(contact_name: str) -> Dict[str, Any]:
	"""Get context for a contact"""
	contact = frappe.get_doc("Contact", contact_name)
	
	context = {
		"full_name": contact.first_name + " " + (contact.last_name or ""),
		"email_id": contact.email_id,
		"mobile_no": contact.mobile_no,
		"company_name": contact.company_name,
		"designation": contact.designation,
	}
	
	return context


def format_ai_response(response: str, response_type: str = "text") -> Dict[str, Any]:
	"""Format AI response for frontend consumption"""
	return {
		"type": response_type,
		"content": response,
		"timestamp": frappe.utils.now(),
	}


def extract_action_items(text: str) -> List[str]:
	"""Extract action items from AI response"""
	# Simple extraction - look for numbered lists or bullet points
	lines = text.split("\n")
	action_items = []
	
	for line in lines:
		line = line.strip()
		# Look for lines starting with numbers or bullets
		if line and (
			line[0].isdigit() or 
			line.startswith("-") or 
			line.startswith("•") or
			line.startswith("*")
		):
			# Clean up the line
			cleaned = line.lstrip("0123456789.-•* ").strip()
			if cleaned:
				action_items.append(cleaned)
	
	return action_items


def save_ai_conversation(
	reference_doctype: str,
	reference_name: str,
	user_message: str,
	ai_response: str,
	conversation_type: str = "chat",
) -> str:
	"""Save AI conversation to database"""
	conversation = frappe.get_doc({
		"doctype": "CRM AI Conversation",
		"reference_doctype": reference_doctype,
		"reference_name": reference_name,
		"user_message": user_message,
		"ai_response": ai_response,
		"conversation_type": conversation_type,
		"user": frappe.session.user,
	})
	conversation.insert(ignore_permissions=True)
	return conversation.name


def save_ai_suggestion(
	reference_doctype: str,
	reference_name: str,
	suggestion_type: str,
	suggestion: str,
	metadata: Optional[Dict[str, Any]] = None,
) -> str:
	"""Save AI suggestion to database"""
	doc = frappe.get_doc({
		"doctype": "CRM AI Suggestion",
		"reference_doctype": reference_doctype,
		"reference_name": reference_name,
		"suggestion_type": suggestion_type,
		"suggestion": suggestion,
		"metadata": json.dumps(metadata) if metadata else None,
		"status": "Pending",
	})
	doc.insert(ignore_permissions=True)
	return doc.name


def log_ai_usage(
	operation: str,
	tokens_used: Optional[int] = None,
	cost: Optional[float] = None,
	metadata: Optional[Dict[str, Any]] = None,
):
	"""Log AI usage for monitoring and cost tracking"""
	# This would ideally be logged to a separate table
	frappe.log_error(
		title=f"AI Usage: {operation}",
		message=json.dumps({
			"operation": operation,
			"tokens_used": tokens_used,
			"cost": cost,
			"metadata": metadata,
			"user": frappe.session.user,
			"timestamp": frappe.utils.now(),
		}),
	)
