import sys
sys.path.insert(0, '/home/samue/mybench/apps/aios_v1')
import frappe

def main():
    frappe.init(site='aios.localhost', sites_path='/home/samue/mybench/sites')
    frappe.connect()
    tenants = frappe.get_all('AIOS Tenant', fields=['name', 'tenant_name', 'role', 'status'])
    convs = frappe.get_all('AIOS Conversation', fields=['name', 'tenant', 'branch', 'title'])
    msgs = frappe.get_all('AIOS Message', fields=['name', 'role', 'worker_key', 'input_tokens', 'output_tokens'])
    print("=== TENANTS ===", len(tenants), tenants)
    print("=== CONVERSATIONS ===", len(convs))
    print("=== TOTAL MESSAGES ===", len(msgs))

if __name__ == '__main__':
    main()
