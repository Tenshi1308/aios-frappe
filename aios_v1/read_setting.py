import frappe

def main():
    frappe.init(site='aios.localhost', sites_path='sites')
    frappe.connect()
    try:
        setting = frappe.get_single("AIOS Setting")
        print("Base URL:", setting.base_url)
        print("Model Name:", setting.model_name)
        print("Has API Key:", bool(setting.get_password("api_key")))
        print("Temperature:", setting.temperature)
    except Exception as e:
        print("Error reading AIOS Setting:", e)

if __name__ == '__main__':
    main()
