# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMAIConversation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		ai_response: DF.LongText | None
		conversation_type: DF.Literal["chat", "email_compose", "summary", "sentiment", "other"]
		reference_doctype: DF.Link | None
		reference_name: DF.DynamicLink | None
		user: DF.Link | None
		user_message: DF.LongText | None
	# end: auto-generated types

	pass
