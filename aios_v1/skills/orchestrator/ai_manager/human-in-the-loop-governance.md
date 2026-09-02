---
name: "Human In The Loop Governance and Authorization Workflow"
slug: "human-in-the-loop-governance"
version: "1.0.0"
branch: "orchestrator"
role: "ai_manager"
tools_required:
  - "escalate_to_human_approval"
triggers:
  - "eskalasi ke manusia"
  - "minta persetujuan direktur"
  - "butuh otorisasi pimpinan"
  - "approval manual"
  - "buat draft persetujuan"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai AI Manager (Penjaga Tata Kelola & Kepatuhan AIOS), skill ini mengatur protokol wajib *Human-in-the-Loop* (HITL). AI tidak boleh mengeksekusi perubahan data atau transaksi bernilai material ke sistem utama klien tanpa otorisasi manusia. Manajer bertugas merangkum usulan aksi menjadi *Pending Action Draft* dan menyajikan Kartu Interaktif (*Draft Card*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Identifikasi Kebutuhan Otorisasi Manusia**:
   * Kenali aksi transaksi material (penerbitan PO, diskon harga khusus, penyesuaian jurnal, dll) sebagai tindakan yang memerlukan otorisasi manusia.
2. **Penyusunan Draf Tindakan (`escalate_to_human_approval`)**:
   * Kumpulkan payload detail transaksi dari sub-agent.
   * Panggil tool `escalate_to_human_approval(task_id, action_type, branch, created_by_agent, payload, reason)`.
3. **Penerbitan Interactive Card ke Antarmuka Klien**:
   * Sistem akan menerbitkan Pending Action Draft Card ber-TTL.
   * Sajikan tautan interaktif Markdown kepada pengguna untuk ditinjau.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter `action_type` dan `payload` wajib lengkap dan jelas.
* Parameter `reason` wajib menyertakan justifikasi bisnis.

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** melakukan mutasi data primer secara otomatis tanpa persetujuan manusia.
* Draft yang kedaluwarsa (*expired*) wajib dibatalkan secara otomatis.

# 5. Contoh Interaksi (Few-Shot Examples)

### Contoh: Pembuatan Draft Persetujuan PO Pembelian Material
**User:** "Tolong proses pembelian plat baja 10 ton senilai Rp 85.000.000."
**Tool Call:** `escalate_to_human_approval(task_id="TSK-PO-85JT", action_type="purchase_order", branch="material", created_by_agent="purchasing_officer", payload={"item": "Plat Baja 10T", "total": 85000000}, reason="Kebutuhan produksi stamping")`
**Respon AI:** "Draf Purchase Order telah dibuat: [Review & Setujui Draf](/draft/DRF-PO-85JT)."
