frappe.pages['aios-portals'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'AIOS Portals',
        single_column: true
    });
    
    page.main.html(`
        <div style="padding: 30px; display: flex; gap: 20px;">
            <div style="border: 1px solid var(--border-color); padding: 20px; border-radius: 8px; width: 300px; text-align: center; background: var(--card-bg);">
                <h3 style="margin-top: 0;">Client Portal</h3>
                <p>Akses portal utama Next.js untuk user/klien.</p>
                <a href="http://client.aios.localhost:8000/login" target="_blank" class="btn btn-primary" style="width: 100%">Buka Client Portal</a>
            </div>
            <div style="border: 1px solid var(--border-color); padding: 20px; border-radius: 8px; width: 300px; text-align: center; background: var(--card-bg);">
                <h3 style="margin-top: 0;">Developer Portal</h3>
                <p>Akses portal monitoring untuk Ekasa Developer.</p>
                <a href="http://developer.aios.localhost:8000/developer" target="_blank" class="btn btn-primary" style="width: 100%">Buka Developer Portal</a>
            </div>
        </div>
    `);
}
