"""
Demo Interaktif Sub-tahap 6M.8: Quality Management Skills (Live LLM Inference).
Menampilkan 9 SOP Alur Kerja Mutu terdistribusi di 5 Job Roles, Simulasi RBAC, dan Pemanggilan LLM Nyata dengan SOP Markdown + Tool Calling.
Dijalankan via: `bench --site aios.localhost execute aios_v1.lib.demo_tahap6m_8.run_demo`
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
    print("🔬 DEMO SUB-TAHAP 6M.8: QUALITY MANAGEMENT SKILLS (LIVE LLM)")
    print("=" * 80)

    # 1. Konfigurasi LLM dari AIOS Setting
    cfg = get_llm_config()
    print(f"\n[1] KONEKSI LLM AKTIF (AIOS Setting):")
    print(f"    • Base URL  : {cfg['base_url']}")
    print(f"    • Model     : {cfg['model']}")
    print(f"    • API Key   : {'✅ ' + cfg['api_key'][:8] + '...' if cfg['api_key'] else '❌ Kosong'}")

    # 2. Meninjau 9 File SOP Quality
    all_skills = load_all_skills(force_reload=True)
    qa_skills = {k: v for k, v in all_skills.items() if v.get("branch") == "quality"}

    print(f"\n[2] MENINJAU {len(qa_skills)} SOP QUALITY MANAGEMENT (skills/quality/<job_role>/):\n")
    for idx, (slug, skill) in enumerate(qa_skills.items(), 1):
        print(f"[{idx:<2}] 🔬 [{skill.get('role').upper():<24}] {skill.get('name')} (v{skill.get('version')})")
        print(f"     • Slug      : {slug}")
        print(f"     • Prioritas : {skill.get('priority').upper()}")
        print(f"     • Tools ({len(skill.get('tools_required', []))}) : {', '.join(skill.get('tools_required', []))}")
        print()

    # 3. Simulasi RBAC Hak Akses Peran Kerja Sub-Agent
    print("=" * 80)
    print("[3] SIMULASI PEMBAGIAN HAK AKSES PERAN KERJA SUB-AGENT (RBAC QUALITY OPSI C):")

    qa_roles = [
        ("quality_inspector", "🔍 Quality Inspector (Inspeksi Lot & Sampling AQL)"),
        ("quality_control_officer", "📋 Quality Control Officer (Usage Decision, CoA & NCR)"),
        ("quality_engineer", "⚙️ Quality Engineer (SPC, Cpk & CAPA Tracking)"),
        ("quality_auditor", "📑 Quality Auditor (Audit ISO 9001 & Laporan Temuan)"),
        ("quality_manager", "👑 Quality Manager (Tata Kelola Mutu, COQ & Pareto)")
    ]

    for role_key, label in qa_roles:
        skills = get_skills_for_worker(branch="quality", worker_key=role_key)
        print(f"\n👉 Peran: {label} (Key: '{role_key}')")
        print(f"   Jumlah SOP yang Dikuasai: {len(skills)} Skill(s)")
        for s in skills:
            print(f"   • [{s.get('branch').upper()}/{s.get('role')}] {s.get('name')}")

    # 4. Merakit System Prompt & Tools untuk Peran Quality Engineer
    branch = "quality"
    role = "quality_engineer"
    base_prompt = "Anda adalah Quality Engineer di AIOS. Analisis statistik proses (SPC / Cpk), susun rencana inspeksi, dan terbitkan CAPA perbaikan sesuai SOP."
    system_prompt = compose_worker_system_prompt(branch, role, base_prompt)
    tools = get_tools_schema_for_worker(branch, role)
    skills = get_skills_for_worker(branch, role)

    print("\n" + "=" * 80)
    print(f"[4] MEMUAT KONTEKS SUB-AGENT QUALITY ENGINEER:")
    print(f"    • SOP Terpasang     : {len(skills)} SOP ({', '.join(s['slug'] for s in skills)})")
    print(f"    • Tools Diizinkan   : {len(tools)} tools ({', '.join(t['function']['name'] for t in tools)})")

    # 5. Skenario Live LLM: Analisis Kapabilitas Proses SPC (Cpk)
    user_query = "Dari 10 sampel pengukuran ketebalan plat presisi diperoleh data: [3.02, 3.01, 3.03, 2.99, 3.02, 3.00, 2.98, 3.01, 3.02, 2.99] mm. Batas toleransi atas (USL) adalah 3.08 mm dan batas toleransi bawah (LSL) adalah 2.92 mm. Tolong hitung indeks kapabilitas proses (Cp, Cpk, Mean, StDev), evaluasi stabilitas prosesnya terhadap standar, dan berikan rekomendasi sesuai SOP."
    print("\n" + "=" * 80)
    print("[5] EKSEKUSI NYATA LIVE LLM DENGAN SOP & TOOL CALLING:")
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
            final_text = final_response.get("content") or final_response.get("reasoning_content") or json.dumps(final_response, indent=2)
            print(final_text)
            print("-" * 80)
        else:
            print(response_msg.get("content"))

        print("\n" + "=" * 80)
        print("🎉 DEMO 6M.8 SELESAI: Quality Engineer Berhasil Menerapkan SOP via Live LLM!")
        print("=" * 80 + "\n")
        return {"status": "SUCCESS", "phase": "6M.8", "qa_skills": len(qa_skills), "model": cfg["model"]}

    except Exception as e:
        print(f"❌ Error Live LLM: {str(e)}")
        return {"status": "ERROR", "error": str(e)}
