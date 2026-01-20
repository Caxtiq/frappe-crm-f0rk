"""Add AI score fields to CRM Lead and CRM Deal"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    """Create custom fields for AI scoring"""
    
    custom_fields = {
        "CRM Lead": [
            {
                "fieldname": "ai_section",
                "label": "AI Insights",
                "fieldtype": "Section Break",
                "insert_after": "sla_tab",
                "collapsible": 1,
            },
            {
                "fieldname": "ai_score",
                "label": "AI Score",
                "fieldtype": "Int",
                "insert_after": "ai_section",
                "read_only": 1,
                "description": "AI-generated lead quality score (0-100)",
            },
            {
                "fieldname": "ai_score_column",
                "fieldtype": "Column Break",
                "insert_after": "ai_score",
            },
            {
                "fieldname": "ai_score_updated_on",
                "label": "Score Updated On",
                "fieldtype": "Datetime",
                "insert_after": "ai_score_column",
                "read_only": 1,
            },
            {
                "fieldname": "ai_score_data",
                "label": "Score Breakdown",
                "fieldtype": "Long Text",
                "insert_after": "ai_score_updated_on",
                "read_only": 1,
                "hidden": 1,
                "description": "Detailed AI score breakdown (JSON)",
            },
        ],
        "CRM Deal": [
            {
                "fieldname": "ai_section",
                "label": "AI Insights",
                "fieldtype": "Section Break",
                "insert_after": "response_details_section",
                "collapsible": 1,
            },
            {
                "fieldname": "ai_win_probability",
                "label": "Win Probability",
                "fieldtype": "Percent",
                "insert_after": "ai_section",
                "read_only": 1,
                "description": "AI-predicted probability of winning this deal",
            },
            {
                "fieldname": "ai_analysis_column",
                "fieldtype": "Column Break",
                "insert_after": "ai_win_probability",
            },
            {
                "fieldname": "ai_analysis_updated_on",
                "label": "Analysis Updated On",
                "fieldtype": "Datetime",
                "insert_after": "ai_analysis_column",
                "read_only": 1,
            },
            {
                "fieldname": "ai_analysis",
                "label": "AI Analysis",
                "fieldtype": "Long Text",
                "insert_after": "ai_analysis_updated_on",
                "read_only": 1,
                "hidden": 1,
                "description": "Detailed AI deal analysis (JSON)",
            },
        ],
    }
    
    create_custom_fields(custom_fields, update=True)
    
    frappe.db.commit()
    print("AI score fields created successfully")
