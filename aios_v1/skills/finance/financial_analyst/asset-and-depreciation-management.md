---
name: "Asset and Depreciation Management Workflow"
slug: "asset-and-depreciation-management"
version: "1.0.0"
branch: "finance"
role: "financial_analyst"
tools_required:
  - "calculate_fixed_asset_depreciation"
  - "calculate_multi_tier_tax"
triggers:
  - "depresiasi aset tetap"
  - "penyusutan mesin"
  - "amortisasi"
  - "pajak aset"
  - "nilai buku aset"
priority: "medium"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Financial Analyst, skill ini mengatur tata kelola nilai buku aset tetap perusahaan, perhitungan beban penyusutan periodik (garis lurus/saldo menurun), serta evaluasi dampak perpajakan atas perolehan dan pelepasan aset.

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Kalkulasi Penyusutan Aset Tetap (`calculate_fixed_asset_depreciation`)**:
   * Panggil `calculate_fixed_asset_depreciation(asset_name, cost, salvage_value, useful_life_years)` untuk menghitung beban penyusutan bulanan dan tahunan.
2. **Kalkulasi Pajak Terkait (`calculate_multi_tier_tax`)**:
   * Panggil `calculate_multi_tier_tax(base_amount, tax_type)` untuk menghitung PPN masukan atau PPh atas transaksi aset.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Nilai perolehan (`cost`) dan masa manfaat (`useful_life_years`) harus bernilai > 0.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Metode penyusutan harus konsisten dengan kebijakan PSAK dan ketentuan fiskal pajak.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung beban depresiasi untuk Truk Operasional baru seharga Rp 350.000.000 dengan masa manfaat 5 tahun."
**Tool Call:** `calculate_fixed_asset_depreciation(asset_name="Truk Operasional Isuzu", cost=350000000, salvage_value=50000000, useful_life_years=5)`
**Respon AI:** "Penyusutan tahunan Truk Operasional adalah Rp 60.000.000 (Rp 5.000.000/bulan)."
