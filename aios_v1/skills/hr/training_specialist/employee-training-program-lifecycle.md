---
name: "Employee Training Program Lifecycle Workflow"
slug: "employee-training-program-lifecycle"
version: "1.0.0"
branch: "hr"
role: "training_specialist"
tools_required:
  - "schedule_training_program"
  - "evaluate_training_effectiveness"
triggers:
  - "jadwalkan program pelatihan"
  - "training karyawan"
  - "evaluasi efektivitas training"
  - "anggaran pelatihan kompetensi"
  - "sertifikasi keahlian pegawai"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Training Specialist, skill ini mengatur perancangan siklus hidup program pelatihan dan pengembangan kompetensi karyawan (*Training Lifecycle*), estimasi alokasi anggaran pelatihan, penerbitan draf jadwal kursus/sertifikasi, dan evaluasi kepuasan serta kelulusan peserta pasca-pelatihan.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Perancangan Jadwal & Anggaran Pelatihan (`schedule_training_program`)**:
   * Panggil `schedule_training_program(training_title, trainer_vendor, estimated_cost, target_participants_count)`.
   * Terbitkan Action Draft Card untuk persetujuan HR Manager.
2. **Evaluasi Efektivitas Pelatihan (`evaluate_training_effectiveness`)**:
   * Setelah modul selesai, panggil `evaluate_training_effectiveness(training_id, average_feedback_score, post_test_pass_rate_pct)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Estimasi biaya dan target peserta harus bernilai positif > 0.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Modul pelatihan wajib selaras dengan standar kompetensi operasional perusahaan.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Jadwalkan pelatihan ISO 9001:2015 dengan vendor TUV Rheinland untuk 15 peserta estimasi biaya Rp 22.500.000."
**Tool Call:** `schedule_training_program(training_title="ISO 9001:2015 Lead Auditor", trainer_vendor="TUV Rheinland", estimated_cost=22500000, target_participants_count=15)`
**Respon AI:** "Draf Pelatihan 'ISO 9001:2015 Lead Auditor' senilai Rp 22.500.000 berhasil dibuat: [Review Draf](/draft/DRF-TRN-001)."
