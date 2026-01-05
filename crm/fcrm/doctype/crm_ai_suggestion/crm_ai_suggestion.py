# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMAISuggestion(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		metadata: DF.Code | None
		reference_doctype: DF.Link | None
		reference_name: DF.DynamicLink | None
		rejection_reason: DF.Text | None
		status: DF.Literal["Pending", "Accepted", "Rejected"]
		suggestion: DF.LongText | None
		suggestion_type: DF.Data | None
	# end: auto-generated types

	pass
