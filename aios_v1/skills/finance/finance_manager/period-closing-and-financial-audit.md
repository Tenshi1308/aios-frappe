---
name: "Period Closing and Financial Audit Workflow"
slug: "period-closing-and-financial-audit"
version: "1.0.0"
branch: "finance"
role: "finance_manager"
tools_required:
  - "run_bank_reconciliation"
  - "generate_pnl_statement"
  - "generate_balance_sheet"
  - "check_department_budget"
triggers:
  - "tutup buku akhir bulan"
  - "period closing"
  - "audit keuangan divisi"
  - "penutupan buku besar"
  - "evaluasi manajer keuangan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Finance Manager, skill ini mengatur orkestrasi proses tutup buku bulanan/tahunan (*Period End Closing*), rekonsiliasi akhir buku kas, pengesahan laporan laba rugi divisi, dan audit kepatuhan anggaran departemen.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Verifikasi Rekonsiliasi Bank (`run_bank_reconciliation`)**:
   * Pastikan seluruh rekening operasional berstatus seimbang (*balanced*).
2. **Penyusunan & Validasi Laporan Keuangan Periodik**:
   * Panggil `generate_pnl_statement(...)` dan `generate_balance_sheet(...)`.
3. **Pemeriksaan Realisasi Anggaran Divisi (`check_department_budget`)**:
   * Evaluasi sisa pagu dan realisasi belanja sebelum mengunci periode buku.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Seluruh entri jurnal penyesuaian (*Adjustment Vouchers*) telah disetujui.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Periode pembukuan tidak boleh ditutup jika terdapat selisih rekonsiliasi bank yang belum diselesaikan.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Jalankan checklist tutup buku akhir bulan Agustus 2026."
**Tool Call:** `run_bank_reconciliation(bank_account="BCA Operasional", closing_balance=250000000)`
**Tool Call:** `generate_pnl_statement(period_start="2026-08-01", period_end="2026-08-31")`
**Respon AI:** "Checklist tutup buku Agustus 2026 selesai: Rekonsiliasi bank 100% balance dan P&L berhasil dikompilasi."
