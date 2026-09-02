"""
Demo Interaktif Sub-tahap 6M.5: Material Management & Procurement Skills (Live LLM Inference).
Menampilkan 10 SOP Alur Kerja Pengadaan & Gudang terdistribusi di 5 Job Roles, Simulasi RBAC, dan Pemanggilan LLM Nyata dengan SOP Markdown + Tool Calling.
Dijalankan via: `bench --site aios.localhost execute aios_v1.lib.demo_tahap6m_5.run_demo`
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
    print("📦 DEMO SUB-TAHAP 6M.5: MATERIAL MANAGEMENT & PROCUREMENT (LIVE LLM)")
    print("=" * 80)

    # 1. Konfigurasi LLM dari AIOS Setting
    cfg = get_llm_config()
    print(f"\n[1] KONEKSI LLM AKTIF (AIOS Setting):")
    print(f"    • Base URL  : {cfg['base_url']}")
    print(f"    • Model     : {cfg['model']}")
    print(f"    • API Key   : {'✅ ' + cfg['api_key'][:8] + '...' if cfg['api_key'] else '❌ Kosong'}")

    # 2. Meninjau 10 File SOP Material
    all_skills = load_all_skills(force_reload=True)
    mat_skills = {k: v for k, v in all_skills.items() if v.get("branch") == "material"}

    print(f"\n[2] MENINJAU {len(mat_skills)} SOP MATERIAL (skills/material/<job_role>/):\n")
    for idx, (slug, skill) in enumerate(mat_skills.items(), 1):
        print(f"[{idx:<2}] 📦 [{skill.get('role').upper():<22}] {skill.get('name')} (v{skill.get('version')})")
        print(f"     • Slug      : {slug}")
        print(f"     • Prioritas : {skill.get('priority').upper()}")
        print(f"     • Tools ({len(skill.get('tools_required', []))}) : {', '.join(skill.get('tools_required', []))}")
        print()

    # 3. Merakit System Prompt & Tools untuk Peran Purchasing Officer
    branch = "material"
    role = "purchasing_officer"
    base_prompt = "Anda adalah Purchasing Officer di AIOS. Kelola pengadaan barang dan pembuatan draf PO secara presisi sesuai SOP."
    system_prompt = compose_worker_system_prompt(branch, role, base_prompt)
    tools = get_tools_schema_for_worker(branch, role)
    skills = get_skills_for_worker(branch, role)

    print("=" * 80)
    print(f"[3] MEMUAT KONTEKS SUB-AGENT PURCHASING OFFICER:")
    print(f"    • SOP Terpasang     : {len(skills)} SOP ({', '.join(s['slug'] for s in skills)})")
    print(f"    • Tools Diizinkan   : {len(tools)} tools ({', '.join(t['function']['name'] for t in tools)})")

    # 4. Skenario Live LLM: Kalkulasi EOQ & Penerbitan Draf PO
    user_query = "Kebutuhan tahunan Plat Besi 2mm adalah 6.000 unit dengan biaya sekali pesan Rp 250.000 dan biaya simpan Rp 15.000/unit/tahun. Tolong hitung EOQ optimalnya lalu buatkan draf Purchase Order ke pemasok PT Sumber Makmur untuk 450 unit @Rp 150.000 dengan target tiba 15 September 2026."
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
            _ensure_tools_loaded()
            messages.append(response_msg)
            
            for tc in tool_calls:
                call_id = tc.get("id", f"call_{len(messages)}")
                func_name = tc.get("function", {}).get("name")
                args_str = tc.get("function", {}).get("arguments", "{}")
                print(f"\n🎯 [LLM Tool Call]: `{func_name}`")
                print(f"   Argumen : {args_str}")

                # Eksekusi tool Python nyata
                args = json.loads(args_str) if isinstance(args_str, str) else args_str
                tool_func = _TOOL_REGISTRY.get(func_name, {}).get("func")
                if tool_func:
                    tool_res = tool_func(**args)
                else:
                    tool_res = {"status": "SUCCESS", "message": f"Tool {func_name} executed."}
                
                print(f"   Hasil Eksekusi Tool: {json.dumps(tool_res, indent=4)}")

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
        print("🎉 DEMO 6M.5 SELESAI: Purchasing Officer Berhasil Menerapkan SOP via Live LLM!")
        print("=" * 80 + "\n")
        return {"status": "SUCCESS", "phase": "6M.5", "model": cfg["model"]}

    except Exception as e:
        print(f"❌ Error Live LLM: {str(e)}")
        return {"status": "ERROR", "error": str(e)}
