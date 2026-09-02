import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_pending_action_draft():
    doctype_name = "Pending Action Draft"
    
    if not frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "module": "Aios V1",
            "custom": 1,
            "name": doctype_name,
            "naming_rule": "Expression",
            "autoname": "DRF-.YYYY.-.MM.-.#####",
            "fields": [
                {"fieldname": "task_id", "fieldtype": "Data", "label": "Task ID", "reqd": 1, "in_list_view": 1},
                {"fieldname": "type", "fieldtype": "Data", "label": "Action Type", "reqd": 1, "in_list_view": 1},
                {"fieldname": "branch", "fieldtype": "Data", "label": "Branch", "in_list_view": 1},
                {"fieldname": "created_by_agent", "fieldtype": "Data", "label": "Created By Agent"},
                {"fieldname": "payload", "fieldtype": "Code", "options": "JSON", "label": "Payload", "reqd": 1},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "PENDING_APPROVAL\nAPPROVED\nREJECTED\nEXPIRED\nCOMPLETED", "default": "PENDING_APPROVAL", "in_list_view": 1},
                {"fieldname": "expires_at", "fieldtype": "Datetime", "label": "Expires At", "reqd": 1, "in_list_view": 1}
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "read": 1,
                    "write": 1,
                    "create": 1,
                    "delete": 1
                }
            ]
        })
        doc.insert(ignore_permissions=True)
        print(f"✅ DocType {doctype_name} berhasil dibuat!")
    else:
        print(f"ℹ️ DocType {doctype_name} sudah ada.")
    frappe.db.commit()

if __name__ == "__main__":
    setup_pending_action_draft()
