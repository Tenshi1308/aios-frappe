"""
Demo CLI untuk Sub-tahap 6A: 7 Tools Orkestrasi AI Manager.
Memperagakan delegasi sub-agent, eskalasi draf manusia, dan koordinasi lintas cabang.
"""

import json
from aios_v1.lib.tool_registry import get_all_tools_schema, execute_tool
import aios_v1.lib.ai_manager_tools

def run_demo():
    print("\n" + "="*68)
    print("🚀 DEMO SUB-TAHAP 6A: 7 TOOLS ORKESTRASI AI MANAGER")
    print("="*68)

    # 1. Tampilkan Daftar Tools Terdaftar
    schemas = get_all_tools_schema()
    print(f"\n[1] TOTAL TOOLS TERDAFTAR DI REGISTRY: {len(schemas)} tools")
    for s in schemas:
        fn = s["function"]
        print(f" • {fn['name']:35} : {fn['description'][:60]}...")

    # 2. Peragaan Tool 1: Delegasi ke Sub-Agent
    print("\n[2] PERAGAAN TOOL: orchestrator_delegate_to_subagent")
    args_del = {
        "branch": "finance",
        "worker_key": "cfo",
        "task_instruction": "Lakukan analisis rasio likuiditas Q3",
        "context_data": {"period": "Q3-2026"}
    }
    res_del = execute_tool("orchestrator_delegate_to_subagent", json.dumps(args_del))
    print(f" -> Output: {res_del}")

    # 3. Peragaan Tool 3: Eskalasi Draf ke Manusia
    print("\n[3] PERAGAAN TOOL: escalate_to_human_approval")
    args_esc = {
        "task_id": "TSK-DEMO-6A-01",
        "action_type": "purchase_order",
        "branch": "material_management",
        "created_by_agent": "purchasing_officer",
        "payload": {"vendor": "PT Maju Bersama", "total": 150000000},
        "reason": "Nilai transaksi > 100 Juta memerlukan otorisasi Direktur"
    }
    res_esc = execute_tool("escalate_to_human_approval", json.dumps(args_esc))
    parsed_esc = json.loads(res_esc)
    print(f" -> Draft Dibuat: {parsed_esc.get('draft_id')}")
    print(f" -> Kartu Markdown UI: {parsed_esc.get('card_markdown')}")
    print(f" -> Status: {parsed_esc.get('status')}")

    print("\n" + "="*68)
    print("✅ HASIL: 7 Tools Orkestrasi AI Manager siap digunakan oleh LLM.")
    print("="*68 + "\n")

    return {
        "status": "success",
        "total_tools": len(schemas),
        "sample_draft": parsed_esc.get("draft_id")
    }

if __name__ == "__main__":
    run_demo()
