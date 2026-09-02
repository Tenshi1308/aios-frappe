---
name: "Vendor Disbursement and Dunning Letter Workflow"
slug: "vendor-disbursement-and-dunning"
version: "1.0.0"
branch: "finance"
role: "treasurer"
tools_required:
  - "process_vendor_payment_batch"
  - "generate_dunning_letter"
triggers:
  - "pembayaran vendor batch"
  - "disbursement hutang"
  - "surat penagihan dunning"
  - "penagihan piutang macet"
  - "pembayaran tagihan pemasok"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Treasurer, skill ini mengatur eksekusi batch pencairan dana pembayaran hutang pemasok (*Vendor Disbursement Batch*) dan penerbitan surat peringatan penagihan piutang pelanggan yang menunggak (*Dunning Letter*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pemrosesan Batch Pembayaran Tagihan (`process_vendor_payment_batch`)**:
   * Kumpulkan daftar invoice yang telah jatuh tempo.
   * Panggil `process_vendor_payment_batch(invoice_ids, total_payment_amount)`.
   * Terbitkan Draf Persetujuan Pencairan Dana untuk otorisasi otorisator bank.
2. **Penerbitan Surat Penagihan Piutang (`generate_dunning_letter`)**:
   * Untuk piutang menunggak, panggil `generate_dunning_letter(customer_id, overdue_amount, days_overdue)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Tagihan vendor harus memiliki dokumen pendukung valid (3-Way Matching selesai).

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** mencairkan pembayaran pihak ketiga tanpa persetujuan otorisator bank (*Draft Card mandatory*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buat surat dunning untuk CV Maju yang menunggak Rp 35.000.000 selama 45 hari."
**Tool Call:** `generate_dunning_letter(customer_id="CUST-055", overdue_amount=35000000, days_overdue=45)`
**Respon AI:** "Surat Penagihan Level 2 (Dunning Formal) berhasil diterbitkan dengan tenggat waktu pelunasan 7 hari."
