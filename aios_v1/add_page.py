import frappe

def main():
    frappe.init('aios.localhost')
    frappe.connect()
    page_name = 'aios-portals'
    if not frappe.db.exists('Page', page_name):
        page = frappe.new_doc('Page')
        page.page_name = page_name
        page.title = 'AIOS Portals'
        page.module = 'AIOS V1'
        page.standard = 'No'
        page.content = """
        <div style="padding: 30px; display: flex; gap: 20px;">
            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 8px; width: 300px; text-align: center; background: white;">
                <h3 style="margin-top: 0;">Client Portal</h3>
                <p>Akses portal utama Next.js untuk user/klien.</p>
                <a href="/" target="_blank" class="btn btn-primary" style="width: 100%">Buka Client Portal</a>
            </div>
            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 8px; width: 300px; text-align: center; background: white;">
                <h3 style="margin-top: 0;">Developer Portal</h3>
                <p>Akses portal monitoring untuk Ekasa Developer.</p>
                <a href="http://developer.aios.localhost:8000/developer" target="_blank" class="btn btn-success" style="width: 100%">Buka Developer Portal</a>
            </div>
        </div>
        """
        page.insert(ignore_permissions=True)
        frappe.db.commit()
        print('Page added!')
    else:
        print('Page already exists')

if __name__ == '__main__':
    main()
