"""
Demo CLI untuk Sub-tahap 6B: Katalog Tools Cabang Finance & Accounting (15 Tools).
Memperagakan eksekusi tool Laba/Rugi, Rasio Finansial, dan Pembuatan Draf Invoice.
"""

import json
from aios_v1.lib.tool_registry import execute_tool
import aios_v1.lib.tools.finance_tools

def run_demo():
    print("\n" + "="*70)
    print("🚀 DEMO SUB-TAHAP 6B: TOOLS FINANCE & ACCOUNTING (15 TOOLS)")
    print("="*70)

    # 1. Peragaan Tool Laporan P&L
    print("\n[1] EKSEKUSI TOOL: generate_pnl_statement")
    args_pnl = {"period_start": "2026-01-01", "period_end": "2026-08-31", "tenant_id": 1}
    res_pnl = json.loads(execute_tool("generate_pnl_statement", json.dumps(args_pnl)))
    print(f" -> Revenue      : Rp {res_pnl['total_revenue']:,.0f}")
    print(f" -> Gross Profit : Rp {res_pnl['gross_profit']:,.0f} ({res_pnl['gross_margin_pct']}%)")
    print(f" -> Net Profit   : Rp {res_pnl['net_profit']:,.0f} ({res_pnl['net_margin_pct']}%)")
    print(f" -> Pesan        : {res_pnl['message']}")

    # 2. Peragaan Tool Rasio Likuiditas & Profitabilitas
    print("\n[2] EKSEKUSI TOOL: calculate_financial_ratios")
    args_ratio = {
        "revenue": 1000000000,
        "cogs": 600000000,
        "net_profit": 150000000,
        "current_assets": 450000000,
        "current_liabilities": 200000000,
        "total_assets": 1200000000
    }
    res_ratio = json.loads(execute_tool("calculate_financial_ratios", json.dumps(args_ratio)))
    print(f" -> Current Ratio : {res_ratio['current_ratio']}x (Status: {res_ratio['liquidity_health']})")
    print(f" -> ROA           : {res_ratio['roa_pct']}%")
    print(f" -> Pesan         : {res_ratio['message']}")

    # 3. Peragaan Tool Action: create_draft_customer_invoice
    print("\n[3] EKSEKUSI TOOL ACTION: create_draft_customer_invoice")
    args_inv = {
        "customer_id": "PT Graha Multi Solusi",
        "items": [
            {"item": "Implementasi Modul ERP Finance", "qty": 1, "price": 80000000},
            {"item": "Annual Cloud Maintenance", "qty": 1, "price": 20000000}
        ],
        "due_date": "2026-09-30",
        "tenant_id": 1
    }
    res_inv = json.loads(execute_tool("create_draft_customer_invoice", json.dumps(args_inv)))
    print(f" -> Draft ID     : {res_inv['draft_id']}")
    print(f" -> Total Nilai  : Rp {res_inv['total_amount']:,.0f} (termasuk PPN 11%)")
    print(f" -> Kartu UI Link: {res_inv['card_markdown']}")
    print(f" -> Status       : {res_inv['status']}")

    print("\n" + "="*70)
    print("✅ HASIL: 15 Tools Cabang Finance & Accounting siap dipanggil AI Manager.")
    print("="*70 + "\n")

    return {
        "status": "success",
        "pnl_sample": res_pnl["net_profit"],
        "draft_sample": res_inv["draft_id"]
    }

if __name__ == "__main__":
    run_demo()
