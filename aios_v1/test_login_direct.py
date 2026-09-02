import frappe
from aios_v1.lib.auth import verify_password, portal_from_request

def main():
    frappe.init(site='aios.localhost', sites_path='sites')
    frappe.connect()
    tenant = frappe.db.get_value("AIOS Tenant", {"email": "client@demo.id"}, ["name", "tenant_name", "email", "role", "status", "password_hash"], as_dict=True)
    print("Tenant in DB:", tenant)
    if tenant:
        pw_ok = verify_password("client123", tenant.password_hash)
        print("Password check:", pw_ok)

if __name__ == '__main__':
    main()
