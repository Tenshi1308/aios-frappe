import frappe
def run():
    doc = frappe.get_doc('DocType', 'Pending Action Draft')
    doc.permissions = []
    doc.append('permissions', {
        'role': 'All',
        'read': 1,
        'write': 1,
        'create': 1,
        'delete': 0
    })
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print('Permissions updated to All!')
