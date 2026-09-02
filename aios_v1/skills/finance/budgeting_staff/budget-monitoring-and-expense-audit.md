---
name: "Budget Monitoring and Expense Audit Workflow"
slug: "budget-monitoring-and-expense-audit"
version: "1.0.0"
branch: "finance"
role: "budgeting_staff"
tools_required:
  - "check_department_budget"
  - "flag_anomalous_expenses"
triggers:
  - "cek anggaran divisi"
  - "monitoring budget"
  - "sisa anggaran"
  - "audit pengeluaran"
  - "kontrol anggaran biaya"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Budgeting Staff, skill ini mengatur pengendalian anggaran belanja divisi (*Budgetary Control*), pemeriksaan ketersediaan pagu sebelum persetujuan pengadaan, dan audit penyimpangan biaya yang melampaui batas toleransi.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pemeriksaan Pagu Anggaran Departemen (`check_department_budget`)**:
   * Panggil `check_department_budget(department)` untuk mengevaluasi total alokasi, realisasi belanja, dan sisa pagu tersedia.
2. **Audit Pengeluaran Outlier (`flag_anomalous_expenses`)**:
   * Panggil `flag_anomalous_expenses(threshold_amount, department)` untuk mendeteksi transaksi yang melebihi batas rata-rata.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Nama departemen harus terdaftar di bagan pusat biaya (*Cost Center*).

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** menyetujui pengajuan belanja jika sisa pagu anggaran departemen bernilai negatif ($\le 0$).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Berapa sisa anggaran Divisi Operasional untuk pengadaan alat baru?"
**Tool Call:** `check_department_budget(department="Operations")`
**Respon AI:** "Anggaran Divisi Operations terpantau aman dengan sisa pagu Rp 180.000.000 (Utilisasi 64%)."
