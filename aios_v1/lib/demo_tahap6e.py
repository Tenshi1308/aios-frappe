"""
Demo CLI untuk Sub-tahap 6E: Katalog Tools Cabang Human Resource (19 Tools) & Role-Scoping.
Memperagakan isolasi tools per job role, kalkulasi lembur & pesangon, dan draf rekrutmen.
"""

import json
from aios_v1.lib.tool_registry import execute_tool, get_tools_schema_for_worker
import aios_v1.lib.tools.hr_tools

def run_demo():
    print("\n" + "="*72)
    print("🚀 DEMO SUB-TAHAP 6E: TOOLS HUMAN RESOURCE MANAGEMENT (19 TOOLS)")
    print("="*72)

    # 1. Peragaan Role-Scoping (Least Privilege)
    print("\n[1] PERAGAAN ROLE-SCOPING (ISOLASI HAK AKSES TOOLS):")
    recruiter_tools = get_tools_schema_for_worker(branch="hr", worker_key="recruiter")
    payroll_tools = get_tools_schema_for_worker(branch="hr", worker_key="payroll_officer")
    
    print(f" • Sub-Agent Recruiter : Memiliki {len(recruiter_tools)} tools terotorisasi (Hanya Rekrutmen)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in recruiter_tools[:2]]}")
    print(f" • Sub-Agent Payroll   : Memiliki {len(payroll_tools)} tools terotorisasi (Hanya Penggajian/BPJS)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in payroll_tools[:2]]}")

    # 2. Peragaan Tool Recruiter: screen_applicant_profile
    print("\n[2] EKSEKUSI TOOL RECRUITER: screen_applicant_profile")
    args_screen = {
        "candidate_name": "Samuel Aditia",
        "skills": ["Python", "Frappe Framework", "AI Multi-Agent", "Next.js"],
        "years_of_experience": 5,
        "applied_position": "Senior AI Systems Architect"
    }
    res_screen = json.loads(execute_tool("screen_applicant_profile", json.dumps(args_screen)))
    print(f" -> Kandidat     : {res_screen['candidate_name']}")
    print(f" -> Skor Match   : {res_screen['match_score_pct']}%")
    print(f" -> Rekomendasi  : {res_screen['status_recommendation']}")
    print(f" -> Pesan        : {res_screen['message']}")

    # 3. Peragaan Tool Payroll: calculate_overtime_hours & severance
    print("\n[3] EKSEKUSI TOOL PAYROLL: calculate_overtime_hours & calculate_severance_pay")
    args_ot = {"employee_id": "EMP-088", "hourly_rate": 50000, "workday_overtime_hours": 4, "weekend_overtime_hours": 0}
    res_ot = json.loads(execute_tool("calculate_overtime_hours", json.dumps(args_ot)))
    print(f" -> Upah Lembur  : Rp {res_ot['total_overtime_pay']:,.0f} ({res_ot['workday_hours']} jam lembur)")

    args_sev = {"years_of_service": 6, "monthly_salary": 12000000, "termination_reason": "Pensiun"}
    res_sev = json.loads(execute_tool("calculate_severance_pay", json.dumps(args_sev)))
    print(f" -> Pesangon     : Rp {res_sev['total_severance_package']:,.0f} (Masa kerja {res_sev['years_of_service']} tahun)")

    # 4. Peragaan Tool Action: post_job_vacancy
    print("\n[4] EKSEKUSI TOOL ACTION: post_job_vacancy")
    args_job = {
        "position_title": "Lead Fullstack Engineer (Frappe/Next.js)",
        "department": "Engineering",
        "requirements": ["5+ tahun Python/TypeScript", "Paham Frappe Framework", "Next.js 15+"],
        "employment_type": "Full-time",
        "tenant_id": 1
    }
    res_job = json.loads(execute_tool("post_job_vacancy", json.dumps(args_job)))
    print(f" -> Draft ID     : {res_job['draft_id']}")
    print(f" -> Kartu UI Link: {res_job['card_markdown']}")
    print(f" -> Status       : {res_job['status']}")

    print("\n" + "="*72)
    print("✅ HASIL: 19 Tools Cabang Human Resource siap dipanggil dengan isolasi role.")
    print("="*72 + "\n")

    return {
        "status": "success",
        "recruiter_tools_count": len(recruiter_tools),
        "payroll_tools_count": len(payroll_tools),
        "draft_job": res_job["draft_id"]
    }

if __name__ == "__main__":
    run_demo()
