---
name: "Employee Benefits and Claims Workflow"
slug: "employee-benefits-and-claims"
version: "1.0.0"
branch: "hr"
role: "hr_staff"
tools_required:
  - "manage_employee_benefits"
triggers:
  - "klaim reimbursement medis"
  - "manfaat tunjangan karyawan"
  - "klaim kacamata pegawai"
  - "tunjangan fasilitas kesehatan"
  - "proses reimbursement hr"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai HR Staff, skill ini mengatur alur verifikasi bukti kuitansi dan penerbitan draf persetujuan klaim fasilitas tunjangan karyawan (*Benefits & Medical Reimbursement*) sesuai pagu hak tahunan masing-masing pegawai.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Verifikasi Bukti Kuitansi & Plafon Tunjangan**:
   * Periksa keabsahan bukti tagihan/kuitansi medis atau kacamata.
2. **Penerbitan Draf Klaim Tunjangan (`manage_employee_benefits`)**:
   * Panggil `manage_employee_benefits(employee_id, benefit_type, claim_amount)`.
   * Terbitkan Action Draft Card untuk otorisasi manajer sebelum diteruskan ke bagian keuangan.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Nominal klaim tidak melebihi sisa pagu tahunan yang dialokasikan.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** menyetujui klaim tanpa kuitansi asli/sah (*Anti-fraud compliance*).

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Proses klaim reimbursement kacamata untuk karyawan EMP-025 sebesar Rp 1.500.000."
**Tool Call:** `manage_employee_benefits(employee_id="EMP-025", benefit_type="Kacamata", claim_amount=1500000)`
**Respon AI:** "Draf Klaim Tunjangan #EMP-025 senilai Rp 1.500.000 siap di-approve: [Review Draf](/draft/DRF-BNF-001)."
