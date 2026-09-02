import frappe
from frappe.utils import now_datetime

def expire_old_drafts():
    """Cron job: Ubah status draft yang melewati batas expires_at jadi EXPIRED."""
    now = now_datetime()
    drafts = frappe.get_all(
        "Pending Action Draft", 
        filters={"status": "PENDING_APPROVAL", "expires_at": ["<", now]}
    )
    for d in drafts:
        frappe.db.set_value("Pending Action Draft", d.name, "status", "EXPIRED")
    
    if drafts:
        frappe.db.commit()
        frappe.log_error(f"{len(drafts)} drafts expired.", "AIOS Draft Manager")

@frappe.whitelist(allow_guest=True)
def get_draft(draft_id: str) -> dict:
    """API untuk mengambil detail draf dari UI tanpa kena masalah Permission."""
    if not frappe.db.exists("Pending Action Draft", draft_id):
        frappe.throw("Draft tidak ditemukan.")
    
    doc = frappe.get_doc("Pending Action Draft", draft_id)
    return doc.as_dict()

@frappe.whitelist(allow_guest=True)
def approve_draft(draft_id: str) -> dict:
    """API untuk meng-approve draft dari UI."""
    if not frappe.db.exists("Pending Action Draft", draft_id):
        frappe.throw("Draft tidak ditemukan.")
    
    doc = frappe.get_doc("Pending Action Draft", draft_id)
    if doc.status != "PENDING_APPROVAL":
        frappe.throw(f"Draft tidak bisa di-approve karena berstatus {doc.status}.")
    
    # Ubah status
    doc.status = "APPROVED"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    
    # TODO: Panggil fungsi eksekusi sebenarnya (di tahap 4/6)
    
    return {"status": "success", "message": f"Draft {draft_id} telah di-approve."}

@frappe.whitelist(allow_guest=True)
def reject_draft(draft_id: str, reason: str = "") -> dict:
    """API untuk me-reject draft dari UI."""
    if not frappe.db.exists("Pending Action Draft", draft_id):
        frappe.throw("Draft tidak ditemukan.")
    
    doc = frappe.get_doc("Pending Action Draft", draft_id)
    if doc.status != "PENDING_APPROVAL":
        frappe.throw(f"Draft tidak bisa di-reject karena berstatus {doc.status}.")
    
    doc.status = "REJECTED"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    
    # TODO: Beritahu AI Manager terkait penolakan ini agar AI mencari alternatif
    
    return {"status": "success", "message": f"Draft {draft_id} telah di-reject."}
