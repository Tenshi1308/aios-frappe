---
name: "Bank Reconciliation Operations Workflow"
slug: "bank-reconciliation-operations"
version: "1.0.0"
branch: "finance"
role: "treasurer"
tools_required:
  - "run_bank_reconciliation"
triggers:
  - "rekonsiliasi bank"
  - "rekening koran"
  - "pencocokan saldo bank"
  - "selisih buku kas"
  - "bank statement"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Treasurer, skill ini mengatur pencocokan berkala antara saldo buku besar kas/bank internal perusahaan dengan rekening koran bank (*Bank Statement*) untuk memastikan tidak ada transaksi gantung atau biaya perbankan yang terlewat.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pencocokan Saldo & Mutasi Bank (`run_bank_reconciliation`)**:
   * Panggil `run_bank_reconciliation(bank_account, closing_balance)`.
   * Evaluasi selisih (*variance*) antara saldo buku dan rekening koran.
2. **Identifikasi Pos Penyesuaian**:
   * Catat pos belum terkredit (*deposit in transit*) atau cek beredar (*outstanding checks*).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Nama/nomor rekening bank harus terdaftar di bagan akun kas.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Selisih yang tidak terjelaskan wajib dilaporkan sebagai suspensi dan diaudit.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Jalankan rekonsiliasi Bank BCA Utama dengan saldo koran Rp 250.000.000."
**Tool Call:** `run_bank_reconciliation(bank_account="BCA Utama - 12345", closing_balance=250000000)`
**Respon AI:** "Rekonsiliasi Bank BCA Utama berhasil dicocokkan 100% (Status: Balanced)."
