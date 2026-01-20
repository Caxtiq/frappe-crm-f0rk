"""Background jobs for AI functionality"""

import frappe
from frappe import _
import json


def auto_score_lead(lead_name):
    """
    Background job to automatically score a lead using AI
    
    Args:
        lead_name: Name of the CRM Lead to score
    """
    try:
        from crm.api.ai import score_lead
        
        # Check if AI is enabled
        settings = frappe.get_single("CRM AI Settings")
        if not settings.enabled:
            return
        
        # Check if lead exists
        if not frappe.db.exists("CRM Lead", lead_name):
            frappe.log_error(
                title="Auto Score Lead Failed",
                message=f"Lead {lead_name} does not exist"
            )
            return
        
        # Score the lead
        result = score_lead(lead_name)
        
        if result and result.get("score") is not None:
            # Update lead with score
            lead = frappe.get_doc("CRM Lead", lead_name)
            lead.db_set("ai_score", result.get("score"), update_modified=False)
            lead.db_set("ai_score_data", json.dumps(result), update_modified=False)
            
            frappe.db.commit()
            
    except Exception as e:
        frappe.log_error(
            title="Auto Score Lead Failed",
            message=f"Error scoring lead {lead_name}: {str(e)}"
        )


def auto_score_deal(deal_name):
    """
    Background job to automatically score a deal using AI
    
    Args:
        deal_name: Name of the CRM Deal to score
    """
    try:
        from crm.api.ai import analyze_deal
        
        # Check if AI is enabled
        settings = frappe.get_single("CRM AI Settings")
        if not settings.enabled:
            return
        
        # Check if deal exists
        if not frappe.db.exists("CRM Deal", deal_name):
            frappe.log_error(
                title="Auto Score Deal Failed",
                message=f"Deal {deal_name} does not exist"
            )
            return
        
        # Analyze the deal
        result = analyze_deal(deal_name)
        
        if result:
            # Update deal with analysis
            deal = frappe.get_doc("CRM Deal", deal_name)
            deal.db_set("ai_analysis", json.dumps(result), update_modified=False)
            
            frappe.db.commit()
            
    except Exception as e:
        frappe.log_error(
            title="Auto Score Deal Failed",
            message=f"Error analyzing deal {deal_name}: {str(e)}"
        )


def batch_score_leads(filters=None):
    """
    Background job to score multiple leads in batch
    
    Args:
        filters: Optional filters to select leads
    """
    try:
        # Get leads without AI score
        filters = filters or {}
        filters["ai_score"] = ["in", [None, ""]]
        
        leads = frappe.get_all(
            "CRM Lead",
            filters=filters,
            fields=["name"],
            limit=50  # Process 50 at a time
        )
        
        for lead in leads:
            # Queue individual scoring jobs
            frappe.enqueue(
                "crm.ai.jobs.auto_score_lead",
                lead_name=lead.name,
                queue="long"
            )
        
        return len(leads)
        
    except Exception as e:
        frappe.log_error(
            title="Batch Score Leads Failed",
            message=str(e)
        )
        return 0
