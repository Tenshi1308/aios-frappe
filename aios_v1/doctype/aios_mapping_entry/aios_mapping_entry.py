# Copyright (c) 2026, Tenshi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIOSMappingEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		canonical_entity: DF.Data
		canonical_field: DF.Data
		confidence: DF.Float
		is_confirmed: DF.Check
		mapping: DF.Link
		name: DF.Int | None
		notes: DF.Data | None
		source_column: DF.Data | None
		source_table: DF.Data | None
	# end: auto-generated types

	_DOCTYPE_NAME = "AIOS Mapping Entry"
