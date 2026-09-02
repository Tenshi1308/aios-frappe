"""
Demo CLI untuk Sub-tahap 6F: Katalog Tools Cabang Manufacturing (16 Tools) & Role-Scoping.
Memperagakan isolasi tools Planner vs Supervisor, kalkulasi HPP Produksi, OEE Mesin, dan Pembuatan Draf MO.
"""

import json
from aios_v1.lib.tool_registry import execute_tool, get_tools_schema_for_worker
import aios_v1.lib.tools.manufacturing_tools

def run_demo():
    print("\n" + "="*72)
    print("🚀 DEMO SUB-TAHAP 6F: TOOLS MANUFACTURING / PRODUCTION PLANNING (16 TOOLS)")
    print("="*72)

    # 1. Peragaan Role-Scoping
    print("\n[1] PERAGAAN ROLE-SCOPING (ISOLASI HAK AKSES TOOLS):")
    planner_tools = get_tools_schema_for_worker(branch="manufacturing", worker_key="production_planner")
    supervisor_tools = get_tools_schema_for_worker(branch="manufacturing", worker_key="production_supervisor")
    
    print(f" • Production Planner    : Memiliki {len(planner_tools)} tools (Hanya Perencanaan MRP/HPP/Takt)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in planner_tools[:2]]}")
    print(f" • Production Supervisor : Memiliki {len(supervisor_tools)} tools (Hanya Lantai Pabrik/Scrap/OEE)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in supervisor_tools[:2]]}")

    # 2. Peragaan Tool Planner: calculate_production_cost
    print("\n[2] EKSEKUSI TOOL PLANNER: calculate_production_cost")
    args_cost = {
        "raw_materials_cost": 45000000,
        "direct_labor_hours": 120,
        "hourly_labor_rate": 50000,
        "overhead_cost": 14000000,
        "batch_quantity": 100
    }
    res_cost = json.loads(execute_tool("calculate_production_cost", json.dumps(args_cost)))
    print(f" -> Bahan Baku    : Rp {res_cost['raw_materials_cost']:,.0f}")
    print(f" -> Tenaga Kerja  : Rp {res_cost['direct_labor_cost']:,.0f}")
    print(f" -> Overhead      : Rp {res_cost['overhead_cost']:,.0f}")
    print(f" -> Total HPP     : Rp {res_cost['total_manufacturing_cost']:,.0f} (Rp {res_cost['unit_production_cost']:,.0f}/unit)")
    print(f" -> Pesan         : {res_cost['message']}")

    # 3. Peragaan Tool Supervisor: analyze_oee_metrics
    print("\n[3] EKSEKUSI TOOL SUPERVISOR: analyze_oee_metrics")
    args_oee = {
        "planned_operating_time_mins": 480,
        "actual_operating_time_mins": 440,
        "ideal_cycle_time_mins": 0.5,
        "total_count": 820,
        "good_count": 800
    }
    res_oee = json.loads(execute_tool("analyze_oee_metrics", json.dumps(args_oee)))
    print(f" -> Availability  : {res_oee['availability_pct']}%")
    print(f" -> Performance   : {res_oee['performance_pct']}%")
    print(f" -> Quality Rate  : {res_oee['quality_pct']}%")
    print(f" -> Overall OEE   : {res_oee['overall_oee_pct']}% (Rating: {res_oee['rating']})")

    # 4. Peragaan Tool Action: create_draft_production_order
    print("\n[4] EKSEKUSI TOOL ACTION: create_draft_production_order")
    args_mo = {
        "product_id": "Mesin Bubut Otomatis CNC-V4",
        "quantity": 10,
        "start_date": "2026-09-10",
        "target_completion_date": "2026-09-30",
        "tenant_id": 1
    }
    res_mo = json.loads(execute_tool("create_draft_production_order", json.dumps(args_mo)))
    print(f" -> Draft MO ID   : {res_mo['draft_id']}")
    print(f" -> Kartu UI Link : {res_mo['card_markdown']}")
    print(f" -> Status        : {res_mo['status']}")

    print("\n" + "="*72)
    print("✅ HASIL: 16 Tools Cabang Manufacturing siap dipanggil dengan isolasi role.")
    print("="*72 + "\n")

    return {
        "status": "success",
        "planner_tools_count": len(planner_tools),
        "supervisor_tools_count": len(supervisor_tools),
        "draft_mo": res_mo["draft_id"]
    }

if __name__ == "__main__":
    run_demo()
