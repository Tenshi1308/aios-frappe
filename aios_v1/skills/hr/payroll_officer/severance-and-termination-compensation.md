---
name: "Severance and Termination Compensation Workflow"
slug: "severance-and-termination-compensation"
version: "1.0.0"
branch: "hr"
role: "payroll_officer"
tools_required:
  - "calculate_severance_pay"
triggers:
  - "hitung uang pesangon"
  - "kompensasi phk karyawan"
  - "penghargaan masa kerja upmk"
  - "hak pesangon pensiun"
  - "severance calculation pp 35"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Payroll Officer, skill ini mengatur simulasi dan penghitungan hak pesangon karyawan (*Severance Pay*), Uang Penghargaan Masa Kerja (UPMK), dan Uang Penggantian Hak (UPH) berdasarkan masa kerja dan alasan pengakhiran hubungan kerja (Pensiun, Efisiensi, atau Pengunduran Diri) sesuai PP No. 35 Tahun 2021.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Identifikasi Status & Alasan Terminasi**:
   * Kumpulkan data masa kerja (`years_of_service`), upah bulanan terakhir (`monthly_salary`), dan alasan penghentian (`termination_reason`).
2. **Kalkulasi Kompensasi Pesangon (`calculate_severance_pay`)**:
   * Panggil `calculate_severance_pay(years_of_service, monthly_salary, termination_reason)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Masa kerja dalam tahun harus valid (integer non-negatif).

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Perhitungan hak terminasi wajib mematuhi formula batas kelipatan minimum perundang-undangan.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung simulasi pesangon pensiun untuk karyawan dengan masa kerja 8 tahun dan upah bulanan terakhir Rp 12.000.000."
**Tool Call:** `calculate_severance_pay(years_of_service=8, monthly_salary=12000000, termination_reason="Pensiun")`
**Respon AI:** "Simulasi Pesangon (Pensiun 8 thn): Total paket kompensasi Rp 156.000.000 (Pesangon 9x + UPMK 4x)."
