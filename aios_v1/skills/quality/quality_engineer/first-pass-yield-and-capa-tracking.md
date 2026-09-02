---
name: "First Pass Yield and CAPA Tracking Workflow"
slug: "first-pass-yield-and-capa-tracking"
version: "1.0.0"
branch: "quality"
role: "quality_engineer"
tools_required:
  - "analyze_first_pass_yield"
  - "track_corrective_action"
triggers:
  - "first pass yield fpy"
  - "tindakan korektif capa"
  - "analisis akar masalah 5 why fishbone"
  - "efisiensi lolos uji pertama"
  - "8d report corrective action"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Quality Engineer, skill ini mengatur pemantauan efisiensi lolos uji pertama kali (*First Pass Yield / FPY*) tanpa pengerjaan ulang (*Zero Rework Benchmark*), serta penyusunan dan pelacakan draf Tindakan Korektif dan Pencegahan (*Corrective and Preventive Action / CAPA*) menggunakan metodologi analisis akar masalah (5 Why / Fishbone).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Analisis Rasio Lolos Pertama Kali (`analyze_first_pass_yield`)**:
   * Panggil `analyze_first_pass_yield(total_units_started, rework_units, scrap_units)`.
   * Bandingkan dengan standar World Class ($\ge 95.0\%$).
2. **Penyusunan Rencana Tindakan Perbaikan Permanen (`track_corrective_action`)**:
   * Jika FPY rendah atau terjadi insiden berulang, panggil `track_corrective_action(capa_title, root_cause, corrective_action, target_date)`.
   * Terbitkan Action Draft Card untuk komitmen implementasi perbaikan.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Jumlah unit rework dan scrap tidak boleh melebihi total unit yang diproduksi.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Seluruh rencana CAPA wajib memiliki PIC penanggung jawab dan tanggal target penyelesaian yang realistis.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung FPY untuk 500 unit produksi di mana 20 unit di-rework dan 5 unit di-scrap, lalu buatkan CAPA jika FPY < 96%."
**Tool Call:** `analyze_first_pass_yield(total_units_started=500, rework_units=20, scrap_units=5)`
**Tool Call:** `track_corrective_action(capa_title="Optimasi Setting Tekanan Mesin Press", root_cause="Tekanan hidrolik berfluktuasi pada shift malam", corrective_action="Pasang sensor regulator tekanan otomatis", target_date="2026-09-30")`
**Respon AI:** "First Pass Yield: 95.0% (475/500 unit lolos langsung). Draf Tindakan CAPA berhasil dibuat: [Review Draf](/draft/DRF-CAPA-001)."
