"""Document event hooks for AI functionality"""

import frappe


def on_lead_insert(doc, method=None):
    """
    Hook called after a CRM Lead is inserted
    Automatically queues lead scoring if AI is enabled
    """
    try:
        # Check if AI is enabled and auto-scoring is configured
        settings = frappe.get_single("CRM AI Settings")
        if not settings.enabled:
            return
        
        # Queue background job to score the lead
        frappe.enqueue(
            "crm.ai.jobs.auto_score_lead",
            lead_name=doc.name,
            queue="default",
            timeout=300
        )
        
    except Exception as e:
        # Don't fail lead creation if scoring fails
        frappe.log_error(
            title="Lead Auto-Scoring Hook Failed",
            message=f"Error queuing score job for lead {doc.name}: {str(e)}"
        )


def on_deal_insert(doc, method=None):
    """
    Hook called after a CRM Deal is inserted
    Automatically queues deal analysis if AI is enabled
    """
    try:
        # Check if AI is enabled
        settings = frappe.get_single("CRM AI Settings")
        if not settings.enabled:
            return
        
        # Queue background job to analyze the deal
        frappe.enqueue(
            "crm.ai.jobs.auto_score_deal",
            deal_name=doc.name,
            queue="default",
            timeout=300
        )
        
    except Exception as e:
        # Don't fail deal creation if analysis fails
        frappe.log_error(
            title="Deal Auto-Analysis Hook Failed",
            message=f"Error queuing analysis job for deal {doc.name}: {str(e)}"
        )
