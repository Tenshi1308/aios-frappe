import frappe

def create_doctype(name, module, fields, naming_rule="autoincrement", **kwargs):
    if frappe.db.exists("DocType", name):
        print(f"DocType {name} already exists.")
        return

    doc = frappe.new_doc("DocType")
    doc.name = name
    doc.module = module
    doc.custom = 0
    doc.autoname = naming_rule
    
    for f in fields:
        doc.append("fields", f)
        
    for k, v in kwargs.items():
        setattr(doc, k, v)
        
    doc.insert(ignore_permissions=True)
    print(f"Created DocType: {name}")

def main():
    frappe.init('aios.localhost')
    frappe.connect()
    
    # 1. AIOS Tenant
    create_doctype("AIOS Tenant", "AIOS V1", [
        {"fieldname": "tenant_name", "fieldtype": "Data", "label": "Tenant Name", "reqd": 1, "unique": 1},
        {"fieldname": "email", "fieldtype": "Data", "label": "Email", "reqd": 1},
        {"fieldname": "role", "fieldtype": "Select", "label": "Role", "options": "CLIENT\nDEVELOPER", "default": "CLIENT"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "PENDING_PAYMENT\nACTIVE", "default": "PENDING_PAYMENT"}
    ])
    
    # 2. AIOS Conversation
    create_doctype("AIOS Conversation", "AIOS V1", [
        {"fieldname": "tenant", "fieldtype": "Link", "label": "Tenant", "options": "AIOS Tenant", "reqd": 1},
        {"fieldname": "branch", "fieldtype": "Data", "label": "Branch", "reqd": 1},
        {"fieldname": "title", "fieldtype": "Data", "label": "Title", "default": "New conversation"}
    ])
    
    # 3. AIOS Message
    create_doctype("AIOS Message", "AIOS V1", [
        {"fieldname": "conversation", "fieldtype": "Link", "label": "Conversation", "options": "AIOS Conversation", "reqd": 1},
        {"fieldname": "role", "fieldtype": "Select", "label": "Role", "options": "user\nmanager\nworker", "reqd": 1},
        {"fieldname": "worker_key", "fieldtype": "Data", "label": "Worker Key"},
        {"fieldname": "content", "fieldtype": "Text Editor", "label": "Content", "reqd": 1},
        {"fieldname": "input_tokens", "fieldtype": "Int", "label": "Input Tokens", "default": 0},
        {"fieldname": "output_tokens", "fieldtype": "Int", "label": "Output Tokens", "default": 0}
    ])
    
    # 4. AIOS Agent State (PluginConfig di Prisma)
    create_doctype("AIOS Agent State", "AIOS V1", [
        {"fieldname": "tenant", "fieldtype": "Link", "label": "Tenant", "options": "AIOS Tenant", "reqd": 1},
        {"fieldname": "scope", "fieldtype": "Data", "label": "Scope", "reqd": 1},
        {"fieldname": "enabled", "fieldtype": "Check", "label": "Enabled", "default": 1},
        {"fieldname": "value", "fieldtype": "Code", "label": "Value"}
    ])
    
    frappe.db.commit()
    print("Migrasi Database Selesai!")

if __name__ == "__main__":
    main()
