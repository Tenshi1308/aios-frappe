import frappe
from aios_v1.lib.auth import hash_password

def update_tenant_doctype():
    doc = frappe.get_doc("DocType", "AIOS Tenant")
    has_field = any(f.fieldname == "password_hash" for f in doc.fields)
    if not has_field:
        doc.append("fields", {
            "fieldname": "password_hash",
            "fieldtype": "Data",
            "label": "Password Hash",
            "hidden": 1
        })
        doc.save(ignore_permissions=True)
        print("Added password_hash to AIOS Tenant DocType")

def seed_accounts():
    # 1. Developer Account
    dev_email = "dev@ekasa.id"
    if not frappe.db.exists("AIOS Tenant", {"email": dev_email}):
        dev = frappe.new_doc("AIOS Tenant")
        dev.tenant_name = "Ekasa Developer"
        dev.email = dev_email
        dev.role = "DEVELOPER"
        dev.status = "ACTIVE"
        dev.password_hash = hash_password("admin123")
        dev.insert(ignore_permissions=True)
        print("Created Developer account: dev@ekasa.id / admin123")
    else:
        dev = frappe.get_doc("AIOS Tenant", {"email": dev_email})
        dev.password_hash = hash_password("admin123")
        dev.role = "DEVELOPER"
        dev.status = "ACTIVE"
        dev.save(ignore_permissions=True)
        print("Updated Developer account")

    # 2. Client Account
    client_email = "client@demo.id"
    if not frappe.db.exists("AIOS Tenant", {"email": client_email}):
        cli = frappe.new_doc("AIOS Tenant")
        cli.tenant_name = "PT Maju Bersama"
        cli.email = client_email
        cli.role = "CLIENT"
        cli.status = "ACTIVE"
        cli.password_hash = hash_password("client123")
        cli.insert(ignore_permissions=True)
        print("Created Client account: client@demo.id / client123")
    else:
        cli = frappe.get_doc("AIOS Tenant", {"email": client_email})
        cli.password_hash = hash_password("client123")
        cli.role = "CLIENT"
        cli.status = "ACTIVE"
        cli.save(ignore_permissions=True)
        print("Updated Client account")

    frappe.db.commit()

def main():
    update_tenant_doctype()
    seed_accounts()

if __name__ == "__main__":
    main()
