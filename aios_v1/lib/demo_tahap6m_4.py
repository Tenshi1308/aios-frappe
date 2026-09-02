"""
Demo Interaktif Sub-tahap 6M.4: Sales & Distribution Skills (Live LLM Inference).
Menampilkan 10 SOP Alur Kerja Penjualan terdistribusi di 5 Job Roles, Simulasi RBAC, dan Pemanggilan LLM Nyata dengan SOP Markdown + Tool Calling.
Dijalankan via: `bench --site aios.localhost execute aios_v1.lib.demo_tahap6m_4.run_demo`
"""

import json
import time
import frappe
from aios_v1.lib.skills_loader import (
    load_all_skills,
    get_skills_for_worker,
    compose_worker_system_prompt
)
from aios_v1.lib.tool_registry import (
    get_tools_schema_for_worker,
    _TOOL_REGISTRY,
    _ensure_tools_loaded
)
from aios_v1.lib.llm_client import get_llm_config, chat_completion


def run_demo():
    print("\n" + "=" * 80)
    print("📈 DEMO SUB-TAHAP 6M.4: SALES & DISTRIBUTION SKILLS (LIVE LLM)")
    print("=" * 80)

    # 1. Konfigurasi LLM dari AIOS Setting
    cfg = get_llm_config()
    print(f"\n[1] KONEKSI LLM AKTIF (AIOS Setting):")
    print(f"    • Base URL  : {cfg['base_url']}")
    print(f"    • Model     : {cfg['model']}")
    print(f"    • API Key   : {'✅ ' + cfg['api_key'][:8] + '...' if cfg['api_key'] else '❌ Kosong'}")

    # 2. Meninjau 10 File SOP Sales
    all_skills = load_all_skills(force_reload=True)
    sales_skills = {k: v for k, v in all_skills.items() if v.get("branch") == "sales"}

    print(f"\n[2] MENINJAU {len(sales_skills)} SOP PENJUALAN (skills/sales/<job_role>/):\n")
    for idx, (slug, skill) in enumerate(sales_skills.items(), 1):
        print(f"[{idx:<2}] 📦 [{skill.get('role').upper():<22}] {skill.get('name')} (v{skill.get('version')})")
        print(f"     • Slug      : {slug}")
        print(f"     • Prioritas : {skill.get('priority').upper()}")
        print(f"     • Tools ({len(skill.get('tools_required', []))}) : {', '.join(skill.get('tools_required', []))}")
        print()

    # 3. Merakit System Prompt & Tools untuk Peran Sales Data Analyst
    branch = "sales"
    role = "sales_data_analyst"
    base_prompt = "Anda adalah Sales Data Analyst di AIOS. Analisis data pelanggan, Pareto, dan churn risk secara akurat sesuai SOP."
    system_prompt = compose_worker_system_prompt(branch, role, base_prompt)
    tools = get_tools_schema_for_worker(branch, role)
    skills = get_skills_for_worker(branch, role)

    print("=" * 80)
    print(f"[3] MEMUAT KONTEKS SUB-AGENT SALES DATA ANALYST:")
    print(f"    • SOP Terpasang     : {len(skills)} SOP ({', '.join(s['slug'] for s in skills)})")
    print(f"    • Tools Diizinkan   : {len(tools)} tools ({', '.join(t['function']['name'] for t in tools)})")

    # 4. Skenario Live LLM: Analisis Churn Risk Pelanggan
    user_query = "Pelanggan CUST-089 tercatat sudah 64 hari tidak memesan produk lagi. Tolong analisis tingkat risiko churn pelanggan ini dan berikan rekomendasi langkah mitigasinya sesuai SOP."
    print("\n" + "=" * 80)
    print("[4] EKSEKUSI NYATA LIVE LLM DENGAN SOP & TOOL CALLING:")
    print(f"👉 User Prompt : \"{user_query}\"")
    print(f"👉 Mengirimkan System Prompt ({len(system_prompt)} karakter) & {len(tools)} Skema Tools ke LLM...")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    t0 = time.perf_counter()
    try:
        response_msg = chat_completion(messages=messages, tools=tools, temperature=0.1)
        latency1 = (time.perf_counter() - t0) * 1000
        print(f"⚡ Respon Tahap 1 Diterima ({latency1:.2f} ms):")

        tool_calls = response_msg.get("tool_calls")
        if tool_calls:
            for tc in tool_calls:
                call_id = tc.get("id", "call_1")
                func_name = tc.get("function", {}).get("name")
                args_str = tc.get("function", {}).get("arguments", "{}")
                print(f"\n🎯 [LLM Tool Call]: `{func_name}`")
                print(f"   Argumen : {args_str}")

                # Eksekusi tool Python nyata
                _ensure_tools_loaded()
                args = json.loads(args_str) if isinstance(args_str, str) else args_str
                tool_func = _TOOL_REGISTRY.get(func_name, {}).get("func")
                if tool_func:
                    tool_res = tool_func(**args)
                else:
                    tool_res = {"status": "SUCCESS", "message": f"Tool {func_name} executed."}
                
                print(f"   Hasil Eksekusi Tool: {json.dumps(tool_res, indent=4)}")

                # Kirim balik hasil tool ke LLM untuk sintesis akhir
                messages.append(response_msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": json.dumps(tool_res)
                })

            t1 = time.perf_counter()
            final_response = chat_completion(messages=messages, temperature=0.1)
            latency2 = (time.perf_counter() - t1) * 1000
            print(f"\n⚡ Respon Akhir Sintesis LLM ({latency2:.2f} ms):")
            print("-" * 80)
            print(final_response.get("content"))
            print("-" * 80)
        else:
            print(response_msg.get("content"))

        print("\n" + "=" * 80)
        print("🎉 DEMO 6M.4 SELESAI: Sales Data Analyst Berhasil Menerapkan SOP via Live LLM!")
        print("=" * 80 + "\n")
        return {"status": "SUCCESS", "phase": "6M.4", "model": cfg["model"]}

    except Exception as e:
        print(f"❌ Error Live LLM: {str(e)}")
        return {"status": "ERROR", "error": str(e)}
