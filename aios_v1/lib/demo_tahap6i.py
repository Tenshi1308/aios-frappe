"""
Demo CLI untuk Sub-tahap 6I: Katalog Tools Cabang Maintenance Management (17 Tools) & Role-Scoping.
Memperagakan isolasi Technician vs Planner vs Reliability Engineer, kalkulasi MTBF/MTTR, Prediksi Kerusakan Sensor, dan Draf Work Order.
"""

import json
from aios_v1.lib.tool_registry import execute_tool, get_tools_schema_for_worker
import aios_v1.lib.tools.maintenance_tools

def run_demo():
    print("\n" + "="*72)
    print("🚀 DEMO SUB-TAHAP 6I: TOOLS MAINTENANCE MANAGEMENT (17 TOOLS)")
    print("="*72)

    # 1. Peragaan Role-Scoping
    print("\n[1] PERAGAAN ROLE-SCOPING (ISOLASI HAK AKSES TOOLS):")
    tech_tools = get_tools_schema_for_worker(branch="maintenance", worker_key="maintenance_technician")
    planner_tools = get_tools_schema_for_worker(branch="maintenance", worker_key="maintenance_planner")
    reliability_tools = get_tools_schema_for_worker(branch="maintenance", worker_key="reliability_engineer")
    
    print(f" • Maintenance Technician   : Memiliki {len(tech_tools)} tools (Hanya Request/Log Kondisi/Jam/Parts)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in tech_tools[:2]]}")
    print(f" • Maintenance Planner      : Memiliki {len(planner_tools)} tools (Hanya Work Order/Jadwal PM/Backlog/Biaya)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in planner_tools[:2]]}")
    print(f" • Reliability Engineer     : Memiliki {len(reliability_tools)} tools (Hanya MTBF-MTTR/Prediktif/FMEA/RCM)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in reliability_tools[:2]]}")

    # 2. Peragaan Tool Reliability: calculate_mtbf_mttr & predict_equipment_failure
    print("\n[2] EKSEKUSI TOOL RELIABILITY: calculate_mtbf_mttr & predict_equipment_failure")
    args_mtbf = {
        "total_operating_hours": 2400,
        "number_of_breakdowns": 3,
        "total_repair_downtime_hours": 6
    }
    res_mtbf = json.loads(execute_tool("calculate_mtbf_mttr", json.dumps(args_mtbf)))
    print(f" -> MTBF (Rata-rata bebas rusak) : {res_mtbf['mtbf_hours']} Jam")
    print(f" -> MTTR (Rata-rata waktu servis): {res_mtbf['mttr_hours']} Jam")
    print(f" -> Inherent Availability        : {res_mtbf['inherent_availability_pct']}% (Rating: {res_mtbf['benchmark_rating']})")

    args_pred = {
        "equipment_id": "PUMP-CENTRIFUGAL-01",
        "current_temp_c": 79.5,
        "current_vibration_mms": 5.2,
        "normal_max_temp": 75.0,
        "normal_max_vibration": 4.5
    }
    res_pred = json.loads(execute_tool("predict_equipment_failure", json.dumps(args_pred)))
    print(f" -> Prediksi Mesin PUMP-01       : {res_pred['health_state']}")
    print(f" -> Rekomendasi Tindakan         : {res_pred['recommended_action']}")

    # 3. Peragaan Tool Planner: create_draft_maintenance_order
    print("\n[3] EKSEKUSI TOOL PLANNER: create_draft_maintenance_order")
    args_wo = {
        "equipment_id": "PUMP-CENTRIFUGAL-01",
        "order_type": "Condition-based Urgent Servis",
        "task_description": "Inspeksi dini bearing dan penggantian pelumas sintetis akibat alert vibrasi",
        "assigned_team": "Tim Pemeliharaan Mekanikal Pabrik",
        "target_start_date": "2026-09-02",
        "tenant_id": 1
    }
    res_wo = json.loads(execute_tool("create_draft_maintenance_order", json.dumps(args_wo)))
    print(f" -> Draft WO ID   : {res_wo['draft_id']}")
    print(f" -> Kartu UI Link : {res_wo['card_markdown']}")
    print(f" -> Status        : {res_wo['status']}")

    print("\n" + "="*72)
    print("✅ HASIL: 17 Tools Cabang Maintenance Management siap dipanggil dengan isolasi role.")
    print("="*72 + "\n")

    return {
        "status": "success",
        "tech_tools_count": len(tech_tools),
        "planner_tools_count": len(planner_tools),
        "reliability_tools_count": len(reliability_tools),
        "draft_wo": res_wo["draft_id"]
    }

if __name__ == "__main__":
    run_demo()
