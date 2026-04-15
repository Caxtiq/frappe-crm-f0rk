"""API endpoints for AI settings - accessible to all users"""

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_ai_settings():
	"""Get AI settings for frontend - only returns public info"""
	try:
		if frappe.session.user == "Guest":
			# Guests can't see AI settings
			return {
				"enabled": False,
				"provider": None,
				"model": None,
			}
		settings = frappe.get_single("CRM AI Settings")
		return {
			"enabled": settings.enabled,
			"provider": settings.provider if settings.enabled else None,
			"model": settings.model if settings.enabled else None,
		}
	except Exception:
		# Return defaults if settings don't exist
		return {
			"enabled": False,
			"provider": None,
			"model": None,
		}
