---
name: "Cross Branch Collaboration and Swarm Coordination Workflow"
slug: "cross-branch-collaboration"
version: "1.0.0"
branch: "orchestrator"
role: "ai_manager"
tools_required:
  - "cross_branch_consultation"
  - "monitor_global_task_ledger"
  - "resolve_agent_conflict"
triggers:
  - "konsultasi lintas cabang"
  - "tanya cabang lain"
  - "cek ledger global"
  - "atasi konflik agent"
  - "sinkronisasi antar divisi"
priority: "high"
---

# 1. Peran & Tujuan Bisnis (Role Context & Objective)
Sebagai AI Manager dalam jaringan multi-agent (*Swarm Coordination*), skill ini mengatur kolaborasi lintas cabang secara sinkron/asinkron, pemantauan status buku besar tugas global (*Global Task Ledger*), dan resolusi sengketa rekomendasi antar agen (*Conflict Resolution*).

# 2. Alur Kerja Eksekusi (Step-by-Step Decision Tree)
1. **Identifikasi Kebutuhan Data Lintas Cabang**:
   * Jika eksekusi suatu tugas memerlukan data dari cabang lain, susun payload permintaan.
2. **Konsultasi Antar Divisi (`cross_branch_consultation`)**:
   * Panggil tool `cross_branch_consultation(task_id, from_branch, to_branch, message_type, payload, priority)`.
3. **Pemantauan Status Ledger Global (`monitor_global_task_ledger`)**:
   * Panggil `monitor_global_task_ledger(task_id, status_filter)`.
4. **Penyelesaian Sengketa Keputusan (`resolve_agent_conflict`)**:
   * Jika ada usulan bertolak belakang antar sub-agent, panggil `resolve_agent_conflict(conflict_topic, proposals, selected_decision, rationale)`.

# 3. Pra-kondisi & Validasi (Pre-conditions)
* Parameter `from_branch` dan `to_branch` harus valid di antara 9 cabang ERP.
* Resolusi konflik wajib menyertakan dasar pemikiran logis (`rationale`).

# 4. Batasan Kepatuhan & Guardrails (Compliance & Safety)
* **DILARANG** melakukan transfer data sensitif yang tidak relevan dengan kebutuhan tugas antar divisi.
* Komunikasi antar cabang harus efisien dan tidak menimbulkan perulangan tanpa henti (*infinite ping-pong loop*).

# 5. Contoh Interaksi (Few-Shot Examples)

### Contoh: Manajer Sales Berkonsultasi Stok ke Manajer Material
**User:** "Apakah kita bisa terima pesanan 500 unit pompa air?"
**Tool Call:** `cross_branch_consultation(task_id="TSK-SO-500", from_branch="sales", to_branch="material", message_type="consultation", payload={"item": "Pompa Air", "qty": 500}, priority="URGENT")`
**Respon AI:** "Permintaan ketersediaan stok 500 unit pompa air telah dikirimkan ke Divisi Material Management."
