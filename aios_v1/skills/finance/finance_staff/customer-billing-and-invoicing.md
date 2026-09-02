---
name: "Customer Billing and Invoicing Workflow"
slug: "customer-billing-and-invoicing"
version: "1.0.0"
branch: "finance"
role: "finance_staff"
tools_required:
  - "create_draft_customer_invoice"
  - "generate_dunning_letter"
triggers:
  - "buat faktur pelanggan"
  - "customer invoice"
  - "penagihan faktur"
  - "tagihan piutang"
  - "surat tagihan piutang"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Finance Staff, skill ini mengatur penerbitan faktur tagihan resmi kepada pelanggan (*Customer Invoicing*) berdasarkan pesanan/berita acara serah terima jasa, serta penerbitan surat pengingat penagihan jika pelanggan mendekati jatuh tempo.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Faktur Tagihan (`create_draft_customer_invoice`)**:
   * Panggil `create_draft_customer_invoice(customer_name, invoice_amount, due_days)`.
   * Terbitkan draf faktur untuk ditinjau supervisor sebelum dikirim ke pelanggan.
2. **Penerbitan Pengingat Tagihan (`generate_dunning_letter`)**:
   * Jika faktur belum terlunasi hingga batas waktu, panggil `generate_dunning_letter(...)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Nama pelanggan dan nominal tagihan harus valid.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh faktur wajib mencantumkan klausul tanggal jatuh tempo dan ketentuan termin pembayaran yang jelas.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan draf invoice untuk PT Samudera Sentosa sebesar Rp 75.000.000 dengan termin 30 hari."
**Tool Call:** `create_draft_customer_invoice(customer_name="PT Samudera Sentosa", invoice_amount=75000000, due_days=30)`
**Respon AI:** "Draf Faktur Tagihan berhasil diterbitkan senilai Rp 75.000.000: [Review Draf](/draft/DRF-INV-001)."
