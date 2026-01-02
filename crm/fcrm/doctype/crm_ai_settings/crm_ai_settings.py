# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMAISettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		api_key: DF.Password | None
		enabled: DF.Check
		max_tokens: DF.Int
		model: DF.Data | None
		provider: DF.Literal["openai", "anthropic", "ollama", "litellm"]
		temperature: DF.Float
	# end: auto-generated types

	pass
