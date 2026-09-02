---
name: "Machine OEE and Downtime Incident Workflow"
slug: "machine-oee-and-downtime-incident"
version: "1.0.0"
branch: "manufacturing"
role: "production_supervisor"
tools_required:
  - "analyze_oee_metrics"
  - "log_downtime_event"
  - "generate_production_variance_report"
triggers:
  - "hitung oee efektivitas mesin"
  - "catat insiden mesin mogok downtime"
  - "breakdown mesin pabrik"
  - "kalkulasi availability performance quality oee"
  - "laporan downtime lini produksi"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Production Supervisor, skill ini mengatur evaluasi efektivitas menyeluruh mesin pabrik (*Overall Equipment Effectiveness / OEE*) dengan mengalikan skor Ketersediaan (*Availability*), Performa (*Performance*), dan Mutu Produk (*Quality Rate*), serta pencatatan resmi insiden mesin mogok (*Downtime Incident Logging*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Pencatatan Insiden Mesin Mogok (`log_downtime_event`)**:
   * Jika terjadi kendala mesin, panggil `log_downtime_event(work_center_id, downtime_duration_mins, breakdown_cause)`.
   * Terbitkan Action Draft Card untuk eskalasi ke divisi Maintenance.
2. **Kalkulasi Metrik OEE Mesin (`analyze_oee_metrics`)**:
   * Panggil `analyze_oee_metrics(planned_operating_time_mins, actual_operating_time_mins, ideal_cycle_time_mins, total_count, good_count)`.
   * Evaluasi standar World Class ($\ge 85\%$), Acceptable ($70-85\%$), atau Needs Improvement ($< 70\%$).

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter waktu operasi dan jumlah produk harus bernilai non-negatif.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Jika skor OEE $< 70\%$ atau terjadi downtime $> 60$ menit, wajib diterbitkan notifikasi investigasi teknis.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung skor OEE mesin CNC jika waktu terencana 480 menit, waktu aktual 432 menit, siklus ideal 0.5 menit/unit, total produk 800 unit dengan 780 unit bagus."
**Tool Call:** `analyze_oee_metrics(planned_operating_time_mins=480, actual_operating_time_mins=432, ideal_cycle_time_mins=0.5, total_count=800, good_count=780)`
**Respon AI:** "Skor OEE Mesin: 81.2% (Availability 90.0%, Performance 92.6%, Quality 97.5%) — Kategori ACCEPTABLE."
