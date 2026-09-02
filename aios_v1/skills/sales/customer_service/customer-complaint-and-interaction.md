---
name: "Customer Complaint and CRM Interaction Workflow"
slug: "customer-complaint-and-interaction"
version: "1.0.0"
branch: "sales"
role: "customer_service"
tools_required:
  - "log_customer_interaction"
  - "check_order_fulfillment_status"
triggers:
  - "komplain pelanggan"
  - "keluhan pembeli"
  - "cek pesanan komplain"
  - "catat tiket crm"
  - "layanan pelanggan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Customer Service, skill ini mengatur penanganan keluhan pelanggan, pencatatan tiket interaksi pada sistem CRM, dan pelacakan status pesanan terkait guna memberikan respon cepat dan solutif.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pengecekan Status Pesanan Terkait (`check_order_fulfillment_status`)**:
   * Panggil `check_order_fulfillment_status(order_id)` untuk memverifikasi riwayat pengiriman.
2. **Pencatatan Log Komplain ke CRM (`log_customer_interaction`)**:
   * Panggil `log_customer_interaction(customer_id, interaction_type="Chat", notes=keluhan, next_followup_date=jadwal)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter keluhan dan identitas pelanggan harus jelas.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh komplain pelanggan wajib ditindaklanjuti sesuai batas waktu SLA maksimal 24 jam.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Pelanggan #CUST-044 mengeluhkan paket belum tiba untuk SO #SO-2026-088."
**Tool Call:** `check_order_fulfillment_status(order_id="SO-2026-088")`
**Tool Call:** `log_customer_interaction(customer_id="CUST-044", interaction_type="Call", notes="Menanyakan keterlambatan paket", next_followup_date="2026-09-03")`
**Respon AI:** "Status pesanan telah selesai dikirim. Log keluhan berhasil dicatat ke CRM dengan jadwal follow-up besok."
