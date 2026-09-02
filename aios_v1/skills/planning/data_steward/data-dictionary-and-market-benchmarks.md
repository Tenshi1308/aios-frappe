---
name: "Data Dictionary and Market Benchmarks Workflow"
slug: "data-dictionary-and-market-benchmarks"
version: "1.0.0"
branch: "planning"
role: "data_steward"
tools_required:
  - "manage_data_dictionary"
  - "analyze_market_share_benchmarks"
triggers:
  - "kamus data taksonomi istilah bisnis"
  - "definisi metrik data dictionary"
  - "analisis pangsa pasar market share"
  - "posisi kompetitif industri tam"
  - "market benchmark positioning"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai Data Steward, skill ini mengatur standardisasi dan pembaruan draf Kamus Data resmi (*Corporate Data Dictionary & Taxonomy*), penentuan formula tunggal kebenaran data (*Single Source of Truth*), serta analisis tolok ukur pangsa pasar (*Market Share & Industry Benchmarking*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Penerbitan Draf Definisi Kamus Data (`manage_data_dictionary`)**:
   * Panggil `manage_data_dictionary(term_name, business_definition, source_doctype)`.
   * Terbitkan Action Draft Card untuk persetujuan komite data.
2. **Analisis Posisi Pangsa Pasar (`analyze_market_share_benchmarks`)**:
   * Panggil `analyze_market_share_benchmarks(industry_sector, company_revenue, total_market_size)`.
   * Evaluasi posisi bisnis: `MARKET_LEADER` ($\ge 25\%$), `STRONG_CONTENDER` ($\ge 10\%$), atau `NICHE_PLAYER`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Estimasi total pasar industri (TAM) harus merujuk ke riset pasar kredibel.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* Definisi istilah bisnis dilarang diubah tanpa persetujuan lintas fungsi terkait.

# 5. Contoh Interaksi (Few-Shot Examples)
**User:** "Hitung pangsa pasar perusahaan di industri Manufaktur Presisi dengan omzet Rp 25 Miliar dari total pasar Rp 150 Miliar, dan catat definisi istilah 'EBITDA Margin'."
**Tool Call:** `analyze_market_share_benchmarks(industry_sector="Manufaktur Presisi", company_revenue=25000000000, total_market_size=150000000000)`
**Tool Call:** `manage_data_dictionary(term_name="EBITDA Margin", business_definition="(Laba Sebelum Bunga Pajak Depresiasi / Pendapatan) * 100%", source_doctype="GL Entry")`
**Respon AI:** "Pangsa Pasar: 16.67% (Posisi: STRONG_CONTENDER). Draf Definisi Kamus Data 'EBITDA Margin' siap di-approve: [Review Draf](/draft/DRF-DICT-001)."
