---
name: "Journal Voucher Entry and Tax Accounting Workflow"
slug: "journal-voucher-entry"
version: "1.0.0"
branch: "finance"
role: "finance_staff"
tools_required:
  - "create_draft_journal_voucher"
  - "calculate_multi_tier_tax"
triggers:
  - "buat jurnal umum"
  - "journal voucher"
  - "entri pembukuan"
  - "hitung pajak ppn pph"
  - "jurnal penyesuaian"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Finance Staff, skill ini mengatur pencatatan entri voucher jurnal umum seimbang (*balanced journal voucher*), penyesuaian saldo buku besar, dan penghitungan pajak transaksi (PPN/PPh) sesuai ketentuan perpajakan.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Perhitungan Pajak Transaksi (`calculate_multi_tier_tax`)**:
   * Jika transaksi memuat komponen pajak, hitung besaran pajak dan total nilai transaksi.
2. **Pembuatan Draf Voucher Jurnal (`create_draft_journal_voucher`)**:
   * Pastikan akun debit dan kredit seimbang ($\text{Debit} = \text{Kredit}$).
   * Panggil `create_draft_journal_voucher(voucher_type, account_debit, account_credit, amount, description)`.
   * Terbitkan Draf Persetujuan Jurnal untuk supervisor.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Akun debit dan kredit harus valid di bagan akun (*Chart of Accounts*).

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** memposting jurnal langsung tanpa draf persetujuan (*Pending Action Draft mandatory*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Buatkan jurnal pembayaran beban listrik operasional kantor Rp 4.500.000 dari Bank Mandiri."
**Tool Call:** `create_draft_journal_voucher(voucher_type="Payment Entry", account_debit="6102 - Beban Listrik", account_credit="1112 - Bank Mandiri Operasional", amount=4500000, description="Beban listrik kantor operasional Sep 2026")`
**Respon AI:** "Draf Journal Voucher berhasil dibuat: [Review Draf](/draft/DRF-JV-001)."
