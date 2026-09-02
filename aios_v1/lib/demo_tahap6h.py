"""
Demo CLI untuk Sub-tahap 6H: Katalog Tools Cabang Logistics Management (18 Tools) & Role-Scoping.
Memperagakan isolasi Shipping Clerk vs Coordinator vs Fleet Manager, kalkulasi ongkir volumetrik, efisiensi BBM, dan Draf Outbound Delivery.
"""

import json
from aios_v1.lib.tool_registry import execute_tool, get_tools_schema_for_worker
import aios_v1.lib.tools.logistic_tools

def run_demo():
    print("\n" + "="*72)
    print("🚀 DEMO SUB-TAHAP 6H: TOOLS LOGISTICS MANAGEMENT (18 TOOLS)")
    print("="*72)

    # 1. Peragaan Role-Scoping
    print("\n[1] PERAGAAN ROLE-SCOPING (ISOLASI HAK AKSES TOOLS):")
    shipping_tools = get_tools_schema_for_worker(branch="logistics", worker_key="shipping_clerk")
    coordinator_tools = get_tools_schema_for_worker(branch="logistics", worker_key="logistics_coordinator")
    fleet_tools = get_tools_schema_for_worker(branch="logistics", worker_key="fleet_manager")
    
    print(f" • Shipping & Receiving Clerk : Memiliki {len(shipping_tools)} tools (Hanya Surat Jalan/GR/GI/POD)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in shipping_tools[:2]]}")
    print(f" • Logistics Coordinator      : Memiliki {len(coordinator_tools)} tools (Hanya Rute/Tracking/Ongkir/Load/3PL)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in coordinator_tools[:2]]}")
    print(f" • Fleet Manager              : Memiliki {len(fleet_tools)} tools (Hanya Master Truk/Servis/BBM/Emisi CO2)")
    print(f"   -> Contoh Tools: {[s['function']['name'] for s in fleet_tools[:2]]}")

    # 2. Peragaan Tool Coordinator: calculate_shipping_cost
    print("\n[2] EKSEKUSI TOOL COORDINATOR: calculate_shipping_cost")
    args_cost = {
        "weight_kg": 15,
        "length_cm": 60,
        "width_cm": 50,
        "height_cm": 40,
        "distance_km": 150,
        "service_tier": "Regular"
    }
    res_cost = json.loads(execute_tool("calculate_shipping_cost", json.dumps(args_cost)))
    print(f" -> Berat Aktual  : {res_cost['actual_weight_kg']} kg")
    print(f" -> Berat Volume  : {res_cost['volumetric_weight_kg']} kg (Dimensi: 60x50x40 cm)")
    print(f" -> Berat Ditagih : {res_cost['chargeable_weight_kg']} kg")
    print(f" -> Total Ongkir  : Rp {res_cost['total_shipping_fee']:,.0f} (Layanan {res_cost['service_tier']} {res_cost['distance_km']} km)")
    print(f" -> Pesan         : {res_cost['message']}")

    # 3. Peragaan Tool Fleet Manager: track_fuel_consumption & CO2
    print("\n[3] EKSEKUSI TOOL FLEET: track_fuel_consumption & calculate_carbon_footprint_logistics")
    args_fuel = {
        "license_plate": "B 9123 UCA",
        "distance_km": 420,
        "fuel_liters": 60,
        "fuel_cost": 408000,
        "tenant_id": 1
    }
    res_fuel = json.loads(execute_tool("track_fuel_consumption", json.dumps(args_fuel)))
    print(f" -> Efisiensi BBM : {res_fuel['km_per_liter']} Km/Liter (Status: {res_fuel['efficiency_status']})")
    
    args_co2 = {"distance_km": 420, "fuel_liters": 60, "vehicle_type": "Diesel Truck"}
    res_co2 = json.loads(execute_tool("calculate_carbon_footprint_logistics", json.dumps(args_co2)))
    print(f" -> Emisi Karbon  : {res_co2['total_co2_kg']} Kg CO2 ({res_co2['co2_kg_per_km']} Kg CO2/Km)")

    # 4. Peragaan Tool Action: create_outbound_delivery
    print("\n[4] EKSEKUSI TOOL ACTION: create_outbound_delivery")
    args_out = {
        "sales_order_id": "SO-2026-0988",
        "customer_address": "Kawasan Industri MM2100 Blok C-4, Cibitung, Bekasi",
        "items": [
            {"product": "Baut Baja Grade 8.8 M8x20", "qty": 2000, "unit": "Pcs"},
            {"product": "Plat Besi 3mm Lembaran", "qty": 20, "unit": "Lembar"}
        ],
        "planned_ship_date": "2026-09-03",
        "tenant_id": 1
    }
    res_out = json.loads(execute_tool("create_outbound_delivery", json.dumps(args_out)))
    print(f" -> Draft DO ID   : {res_out['draft_id']}")
    print(f" -> Kartu UI Link : {res_out['card_markdown']}")
    print(f" -> Status        : {res_out['status']}")

    print("\n" + "="*72)
    print("✅ HASIL: 18 Tools Cabang Logistics Management siap dipanggil dengan isolasi role.")
    print("="*72 + "\n")

    return {
        "status": "success",
        "shipping_tools_count": len(shipping_tools),
        "coordinator_tools_count": len(coordinator_tools),
        "fleet_tools_count": len(fleet_tools),
        "draft_do": res_out["draft_id"]
    }

if __name__ == "__main__":
    run_demo()
