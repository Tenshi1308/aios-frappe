import frappe
def run():
    result = frappe.call("aios_v1.lib.draft_manager.get_draft", draft_id="DRF-2026-09-00001")
    print("RESULT:", result)
