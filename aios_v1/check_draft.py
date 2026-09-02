import frappe
def run():
    print(frappe.get_all('Pending Action Draft'))
