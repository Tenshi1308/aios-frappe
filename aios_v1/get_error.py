import frappe
def main():
    frappe.init("aios.localhost")
    frappe.connect()
    logs = frappe.get_list("Error Log", limit=1, order_by="creation desc")
    if logs:
        print(frappe.get_doc("Error Log", logs[0].name).error)
    else:
        print("No errors found")
if __name__ == "__main__":
    main()
