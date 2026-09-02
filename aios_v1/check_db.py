import frappe

def main():
    frappe.init(site='aios.localhost', sites_path='sites')
    frappe.connect()
    convs = frappe.get_all('AIOS Conversation', fields=['name', 'tenant', 'branch', 'title'])
    msgs = frappe.get_all('AIOS Message', fields=['name', 'conversation', 'role', 'content'])
    print("=== CONVERSATIONS IN DB ===")
    for c in convs:
        print(c)
    print("\n=== MESSAGES IN DB ===")
    for m in msgs:
        print(f"[{m.role}] {m.content[:80]}...")

if __name__ == '__main__':
    main()
