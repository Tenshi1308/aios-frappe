import frappe

def main():
    frappe.init('aios.localhost')
    frappe.connect()
    
    doctypes = ['AIOS Tenant', 'AIOS Conversation', 'AIOS Message', 'AIOS Agent State']
    
    for dt in doctypes:
        doc = frappe.get_doc('DocType', dt)
        
        # Cek apakah permission kosong
        if len(doc.permissions) == 0:
            doc.append('permissions', {
                'role': 'System Manager',
                'read': 1,
                'write': 1,
                'create': 1,
                'delete': 1,
                'email': 1,
                'export': 1,
                'print': 1,
                'report': 1
            })
            doc.save(ignore_permissions=True)
            print(f'Fixed permissions for {dt}')
            
    frappe.db.commit()

if __name__ == '__main__':
    main()
