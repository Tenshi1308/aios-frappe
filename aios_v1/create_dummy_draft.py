import frappe
import json
from frappe.utils import add_to_date, now_datetime
def run():
    doc = frappe.get_doc({
        'doctype': 'Pending Action Draft',
        'task_id': 'TASK-DEMO-123',
        'type': 'purchase_order',
        'branch': 'material_management',
        'created_by_agent': 'purchasing_officer',
        'payload': json.dumps({'vendor': 'PT Sumber Makmur', 'items': [{'product': 'Bolt M8x20', 'qty': 50, 'unit_price': 1500}], 'total': 75000}),
        'status': 'PENDING_APPROVAL',
        'expires_at': add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print('CREATED:', doc.name)
