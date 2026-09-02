import frappe

def main():
    frappe.init(site='aios.localhost', sites_path='sites')
    frappe.connect()
    doctypes = frappe.get_all('DocType', filters={'name': ['like', '%AIOS Set%']})
    print("Found DocTypes:", doctypes)
    for dt in doctypes:
        name = dt.name
        meta = frappe.get_meta(name)
        fields = [(f.fieldname, f.fieldtype, f.label) for f in meta.fields]
        print(f"\nFields of {name}:", fields)
        try:
            doc = frappe.get_single(name) if meta.issingle else frappe.get_all(name, fields=['*'])
            print(f"Data in {name}:", doc)
        except Exception as e:
            print("Error getting data:", e)

if __name__ == '__main__':
    main()
