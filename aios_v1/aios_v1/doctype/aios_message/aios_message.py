# Copyright (c) 2026, Tenshi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIOSMessage(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		content: DF.TextEditor
		conversation: DF.Link
		input_tokens: DF.Int
		name: DF.Int | None
		output_tokens: DF.Int
		role: DF.Literal["user", "manager", "worker"]
		worker_key: DF.Data | None
	# end: auto-generated types

	_DOCTYPE_NAME = "AIOS Message"
