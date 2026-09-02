---
name: "Cashflow Forecasting and Liquidity Management Workflow"
slug: "cashflow-forecasting-and-liquidity"
version: "1.0.0"
branch: "finance"
role: "treasurer"
tools_required:
  - "forecast_30d_cashflow"
  - "get_ar_aging_summary"
  - "get_ap_aging_summary"
triggers:
  - "proyeksi arus kas"
  - "forecast cashflow"
  - "likuiditas kas"
  - "posisi kas 30 hari"
  - "manajemen modal kerja"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Treasurer (Bendahara Perusahaan), skill ini mengatur penjagaan kecukupan likuiditas kas harian dan peramalan arus kas masuk (*inflow*) serta keluar (*outflow*) selama 30 hari ke depan guna mencegah terjadinya defisit kas operasional.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Inflow & Outflow Terjadwal**:
   * Panggil `get_ar_aging_summary()` untuk mengestimasi penagihan piutang lancar.
   * Panggil `get_ap_aging_summary()` untuk memetakan jadwal jatuh tempo tagihan vendor.
2. **Kalkulasi Proyeksi Kas 30 Hari (`forecast_30d_cashflow`)**:
   * Panggil `forecast_30d_cashflow(current_cash_balance)`.
   * Evaluasi status runway kas (*Healthy* / *Deficit Alert*).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Saldo kas awal (`current_cash_balance`) harus mencerminkan saldo rekening bank riil.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Jika proyeksi saldo kas harian mendekati ambang batas minimum, wajib memberikan peringatan tegas kepada CFO.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Bagaimana proyeksi kas kita 30 hari ke depan jika saldo awal Rp 150.000.000?"
**Tool Call:** `forecast_30d_cashflow(current_cash_balance=150000000)`
**Respon AI:** "Proyeksi arus kas 30 hari menunjukkan kondisi HEALTHY dengan estimasi saldo akhir Rp 230.000.000."
