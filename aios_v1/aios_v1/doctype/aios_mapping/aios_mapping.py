# Copyright (c) 2026, Tenshi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIOSMapping(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		connection: DF.Link
		name: DF.Int | None
		notes: DF.SmallText | None
		overall_confidence: DF.Float
		status: DF.Literal["NEEDS_REVIEW", "VALIDATED", "REJECTED"]
		validated_at: DF.Datetime | None
		version: DF.Int
	# end: auto-generated types

	_DOCTYPE_NAME = "AIOS Mapping"
