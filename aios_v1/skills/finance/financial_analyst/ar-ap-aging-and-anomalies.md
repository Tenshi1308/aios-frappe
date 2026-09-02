---
name: "AR/AP Aging and Expense Anomalies Workflow"
slug: "ar-ap-aging-and-anomalies"
version: "1.0.0"
branch: "finance"
role: "financial_analyst"
tools_required:
  - "get_ar_aging_summary"
  - "get_ap_aging_summary"
  - "flag_anomalous_expenses"
triggers:
  - "umur piutang ar"
  - "umur hutang ap"
  - "anomali biaya"
  - "pengeluaran janggal"
  - "audit transaksi mencurigakan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Financial Analyst, skill ini mengatur analisis umur piutang usaha (*AR Aging*) dan hutang dagang (*AP Aging*), serta penyaringan anomali transaksi biaya operasional untuk memitigasi kebocoran anggaran dan kredit macet.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Umur Piutang & Hutang**:
   * Panggil `get_ar_aging_summary(as_of_date)` untuk melihat sebaran piutang macet.
   * Panggil `get_ap_aging_summary(as_of_date)` untuk melihat kewajiban hutang jatuh tempo.
2. **Audit Anomali Biaya (`flag_anomalous_expenses`)**:
   * Panggil `flag_anomalous_expenses(threshold_amount, department)` untuk menyaring transaksi pengeluaran outlier di atas batas wajar.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Cut-off tanggal analisis harus valid.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Transaksi yang terdeteksi anomali wajib dilaporkan ke auditor internal untuk verifikasi fisik faktur.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Cek apakah ada transaksi pengeluaran janggal di atas Rp 25.000.000 bulan ini."
**Tool Call:** `flag_anomalous_expenses(threshold_amount=25000000, department="All")`
**Respon AI:** "Ditemukan 2 transaksi anomali yang melebihi batas rata-rata historis departemen."
