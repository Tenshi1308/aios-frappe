"""
Demo CLI untuk Sub-tahap 6J: Katalog Tools Cabang Strategic Planning & BI (16 Tools) & Role-Scoping.
Memperagakan isolasi BI Analyst vs Report Developer vs Strategist, simulasi Skenario What-If, KPI Dashboard, dan Draf Template Laporan.
"""

import json
from aios_v1.lib.tool_registry import execute_tool, get_tools_schema_for_worker
import aios_v1.lib.tools.planning_tools

def run_demo():
    print("\n" + "="*72)
    print("🚀 DEMO SUB-TAHAP 6J: TOOLS STRATEGIC PLANNING & BI (16 TOOLS)")
    print("="*72)

    # 1. Peragaan Role-Scoping
    print("\n[1] PERAGAAN ROLE-SCOPING (ISOLASI HAK AKSES TOOLS):")
    bi_tools = get_tools_schema_for_worker(branch="planning", worker_key="bi_analyst")
    dev_tools = get_tools_schema_for_worker(branch="planning", worker_key="report_developer")
    steward_tools = get_tools_schema_for_worker(branch="planning", worker_key="data_steward")
    
    print(f" • BI Analyst      : Memiliki {len(bi_tools)} tools (Hanya KPI Dashboard/Tren/Forecast/Cross-Report)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in bi_tools[:2]]}")
    print(f" • Report Developer: Memiliki {len(dev_tools)} tools (Hanya Template/Budget vs Actual/Summary/Schedule)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in dev_tools[:2]]}")
    print(f" • Data Steward    : Memiliki {len(steward_tools)} tools (Hanya Kualitas Data/Anomali/Kamus Data/Pangsa Pasar)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in steward_tools[:2]]}")

    # 2. Peragaan Tool Strategist: run_what_if_scenario
    print("\n[2] EKSEKUSI TOOL STRATEGIST: run_what_if_scenario")
    args_sim = {
        "scenario_name": "Kenaikan Harga Jual +5% dan Efisiensi Biaya -3%",
        "base_revenue": 10000000000,
        "base_cost": 6500000000,
        "price_change_pct": 5.0,
        "cost_change_pct": -3.0,
        "volume_change_pct": 2.0
    }
    res_sim = json.loads(execute_tool("run_what_if_scenario", json.dumps(args_sim)))
    print(f" -> Skenario         : {res_sim['scenario']}")
    print(f" -> Proyeksi Revenue : Rp {res_sim['projected_revenue']:,.0f}")
    print(f" -> Proyeksi Biaya   : Rp {res_sim['projected_cost']:,.0f}")
    print(f" -> Dampak Laba      : +Rp {res_sim['profit_impact_delta']:,.0f} (Rekomendasi: {res_sim['recommendation']})")
    print(f" -> Pesan            : {res_sim['message']}")

    # 3. Peragaan Tool BI: generate_kpi_dashboard
    print("\n[3] EKSEKUSI TOOL BI ANALYST: generate_kpi_dashboard")
    res_kpi = json.loads(execute_tool("generate_kpi_dashboard", json.dumps({"tenant_id": 1})))
    print(f" -> Metrik Finansial : Margin Kotor {res_kpi['kpis']['financial']['gross_margin_pct']}%, Net Profit Margin {res_kpi['kpis']['financial']['net_profit_margin_pct']}%")
    print(f" -> Metrik Operasi   : Logistik OTIF {res_kpi['kpis']['operations']['on_time_delivery_otif_pct']}%, Mutu FPY {res_kpi['kpis']['operations']['first_pass_yield_fpy_pct']}%")
    print(f" -> Status Korporat  : {res_kpi['executive_health_grade']}")

    # 4. Peragaan Tool Action: build_custom_report_template
    print("\n[4] EKSEKUSI TOOL ACTION: build_custom_report_template")
    args_tmpl = {
        "template_name": "Executive C-Level Flash Deck Q4",
        "target_audience": "Dewan Direksi & Komisaris",
        "metrics_included": ["Revenue", "EBITDA", "OTIF", "OEE", "Turnover"],
        "layout_format": "Executive Brief Summary",
        "tenant_id": 1
    }
    res_tmpl = json.loads(execute_tool("build_custom_report_template", json.dumps(args_tmpl)))
    print(f" -> Draft Template ID: {res_tmpl['draft_id']}")
    print(f" -> Kartu UI Link    : {res_tmpl['card_markdown']}")
    print(f" -> Status           : {res_tmpl['status']}")

    print("\n" + "="*72)
    print("✅ HASIL: 16 Tools Cabang Strategic Planning & BI siap dipanggil dengan isolasi role.")
    print("="*72 + "\n")

    return {
        "status": "success",
        "bi_tools_count": len(bi_tools),
        "dev_tools_count": len(dev_tools),
        "steward_tools_count": len(steward_tools),
        "draft_template": res_tmpl["draft_id"]
    }

if __name__ == "__main__":
    run_demo()
