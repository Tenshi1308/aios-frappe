---
name: "Attendance and Leave Administration Workflow"
slug: "attendance-and-leave-administration"
version: "1.0.0"
branch: "hr"
role: "hr_staff"
tools_required:
  - "manage_leave_request"
  - "track_attendance_summary"
triggers:
  - "proses pengajuan cuti"
  - "rekap absensi bulanan"
  - "cuti tahunan karyawan"
  - "tingkat kehadiran pegawai"
  - "izin dan absensi kantor"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai HR Staff, skill ini mengatur alur pemrosesan draf persetujuan permohonan cuti pegawai (*Leave Request Approval*) dan kompilasi rekapitulasi data kehadiran, keterlambatan, serta absensi bulanan seluruh departemen.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pemrosesan Draf Pengajuan Cuti (`manage_leave_request`)**:
   * Panggil `manage_leave_request(employee_id, leave_type, days_count, reason)`.
   * Terbitkan Action Draft Card untuk otorisasi atasan langsung/HR.
2. **Pemantauan Tingkat Kehadiran Departemen (`track_attendance_summary`)**:
   * Panggil `track_attendance_summary(department, period_month)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Karyawan harus memiliki sisa saldo cuti yang mencukupi.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh persetujuan cuti wajib terdata rapi dan sinkron dengan sistem payroll.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Proses pengajuan cuti tahunan 3 hari untuk karyawan EMP-088 alasan keperluan keluarga."
**Tool Call:** `manage_leave_request(employee_id="EMP-088", leave_type="Tahunan", days_count=3, reason="Keperluan keluarga mendesak")`
**Respon AI:** "Draf Pengajuan Cuti #EMP-088 (3 hari) berhasil dibuat: [Review Draf](/draft/DRF-LEAVE-001)."
