import frappe
from aios_v1.managers import get_manager

def main():
    frappe.init(site='aios.localhost', sites_path='sites')
    frappe.connect()
    mgr = get_manager('finance')
    for chunk in mgr.handle_stream(company_id=2, user_message='buatkan template tabel 3x3 sederhana'):
        print(chunk, end='')

if __name__ == '__main__':
    main()
