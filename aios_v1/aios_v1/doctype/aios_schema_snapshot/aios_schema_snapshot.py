# Copyright (c) 2026, Tenshi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIOSSchemaSnapshot(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		connection: DF.Link
		extracted_at: DF.Datetime | None
		hash: DF.Data
		name: DF.Int | None
		schema_json: DF.LongText | None
		tables_count: DF.Int
	# end: auto-generated types

	_DOCTYPE_NAME = "AIOS Schema Snapshot"
