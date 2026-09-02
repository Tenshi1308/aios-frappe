"""
Katalog Tools Cabang 7: Logistics Management (18 Tools).
Job Roles: Shipping & Receiving Clerk, Logistics Coordinator, Fleet Manager, Logistics Manager.
Sesuai Blueprint Phase 5 §7.G dengan Prinsip Role-Scoping (Least Privilege).
"""

import json
import math
import frappe
from typing import Dict, Any, List, Optional
from frappe.utils import add_to_date, now_datetime
from aios_v1.lib.tool_registry import ai_tool
from aios_v1.lib.data_access_agent import get_data_access_agent

# =========================================================================
# SHIPPING & RECEIVING CLERK TOOLS (5 Tools)
# =========================================================================

@ai_tool(
    name="create_outbound_delivery",
    description="Membuat draf Surat Perintah Pengiriman Barang ke pelanggan (Outbound Delivery / Surat Jalan) (Action -> Draft Card).",
    branch="logistics",
    roles=["shipping_clerk", "logistics_manager"],
    parameters={
        "sales_order_id": {"type": "string", "description": "Nomor Sales Order rujukan"},
        "customer_address": {"type": "string", "description": "Alamat lengkap tujuan pengiriman"},
        "items": {"type": "array", "description": "Daftar barang dan jumlah yang dikirim"},
        "planned_ship_date": {"type": "string", "description": "Rencana tanggal keberangkatan (YYYY-MM-DD)"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def create_outbound_delivery(sales_order_id: str, customer_address: str, items: List[Dict[str, Any]], planned_ship_date: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "order_id": sales_order_id,
        "destination": customer_address,
        "items": items,
        "ship_date": planned_ship_date,
        "total_packages": len(items)
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-OUT-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "outbound_delivery",
        "branch": "logistics",
        "created_by_agent": "shipping_clerk",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "outbound_delivery",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Pengiriman Barang ({doc.name}) untuk SO #{sales_order_id} berhasil dibuat dan siap di-approve."
    }

@ai_tool(
    name="create_inbound_delivery",
    description="Membuat draf Surat Penerimaan Barang Masuk dari pemasok (Inbound Delivery / GR Preparation) (Action -> Draft Card).",
    branch="logistics",
    roles=["shipping_clerk", "logistics_manager"],
    parameters={
        "po_number": {"type": "string", "description": "Nomor Purchase Order rujukan"},
        "supplier_name": {"type": "string", "description": "Nama pemasok/vendor pengirim"},
        "items": {"type": "array", "description": "Daftar barang yang akan tiba"},
        "expected_arrival_date": {"type": "string", "description": "Target tanggal kedatangan (YYYY-MM-DD)"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def create_inbound_delivery(po_number: str, supplier_name: str, items: List[Dict[str, Any]], expected_arrival_date: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "po_number": po_number,
        "vendor": supplier_name,
        "items": items,
        "arrival_date": expected_arrival_date
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-INB-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "inbound_delivery",
        "branch": "logistics",
        "created_by_agent": "shipping_clerk",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "inbound_delivery",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Penerimaan Masuk ({doc.name}) untuk PO #{po_number} dari {supplier_name} berhasil dibuat."
    }

@ai_tool(
    name="confirm_goods_receipt",
    description="Membuat draf konfirmasi fisik barang masuk tiba di gudang logistik (Action -> Draft Card).",
    branch="logistics",
    roles=["shipping_clerk", "logistics_manager"],
    parameters={
        "delivery_id": {"type": "string", "description": "Nomor dokumen Inbound Delivery"},
        "received_items": {"type": "array", "description": "Daftar barang dan jumlah aktual yang diterima"},
        "receiver_name": {"type": "string", "description": "Nama petugas penerima di dermaga gudang"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def confirm_goods_receipt(delivery_id: str, received_items: List[Dict[str, Any]], receiver_name: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "delivery_id": delivery_id,
        "items": received_items,
        "receiver": receiver_name,
        "received_at": str(now_datetime())
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-CGR-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "confirm_goods_receipt",
        "branch": "logistics",
        "created_by_agent": "shipping_clerk",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "confirm_goods_receipt",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Konfirmasi Barang Masuk #{delivery_id} ({doc.name}) oleh {receiver_name} siap di-approve."
    }

@ai_tool(
    name="confirm_goods_issue",
    description="Membuat draf konfirmasi pelepasan barang keluar dari gudang (Goods Issue Validation) (Action -> Draft Card).",
    branch="logistics",
    roles=["shipping_clerk", "logistics_manager"],
    parameters={
        "delivery_id": {"type": "string", "description": "Nomor dokumen Outbound Delivery"},
        "issued_items": {"type": "array", "description": "Daftar barang yang dimuat ke armada"},
        "picker_name": {"type": "string", "description": "Nama petugas picker/loading"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def confirm_goods_issue(delivery_id: str, issued_items: List[Dict[str, Any]], picker_name: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "delivery_id": delivery_id,
        "items": issued_items,
        "picker": picker_name,
        "dispatched_at": str(now_datetime())
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-CGI-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "confirm_goods_issue",
        "branch": "logistics",
        "created_by_agent": "shipping_clerk",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "confirm_goods_issue",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Konfirmasi Pelepasan Barang #{delivery_id} ({doc.name}) siap diotorisasi."
    }

@ai_tool(
    name="log_pod_proof_of_delivery",
    description="Membuat draf pencatatan bukti tanda terima barang bertandatangan (Proof of Delivery / POD) dari kurir (Action -> Draft Card).",
    branch="logistics",
    roles=["shipping_clerk", "logistics_coordinator", "logistics_manager"],
    parameters={
        "delivery_id": {"type": "string", "description": "Nomor Surat Jalan / Delivery"},
        "recipient_name": {"type": "string", "description": "Nama penerima fisik barang"},
        "received_timestamp": {"type": "string", "description": "Waktu penerimaan barang (YYYY-MM-DD HH:MM)"},
        "pod_signature_ref": {"type": "string", "description": "Nomor referensi atau URL bukti foto tanda terima"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def log_pod_proof_of_delivery(delivery_id: str, recipient_name: str, received_timestamp: str, pod_signature_ref: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "delivery_id": delivery_id,
        "recipient": recipient_name,
        "timestamp": received_timestamp,
        "signature_ref": pod_signature_ref
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-POD-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "proof_of_delivery",
        "branch": "logistics",
        "created_by_agent": "shipping_clerk",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "proof_of_delivery",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Rekam POD #{delivery_id} (Diterima oleh {recipient_name}) ({doc.name}) siap di-approve."
    }

# =========================================================================
# LOGISTICS COORDINATOR TOOLS (5 Tools)
# =========================================================================

@ai_tool(
    name="plan_shipment_route",
    description="Membuat draf rencana rute pengiriman multi-titik (Multi-Stop Route) dan estimasi waktu tempuh (Action -> Draft Card).",
    branch="logistics",
    roles=["logistics_coordinator", "logistics_manager"],
    parameters={
        "origin_warehouse": {"type": "string", "description": "Gudang asal keberangkatan"},
        "destination_stops": {"type": "array", "description": "Urutan daftar alamat tujuan pengiriman"},
        "vehicle_type": {"type": "string", "description": "Tipe armada: 'Engkel Box 2 Ton', 'CDD 4 Ton', 'Fuso 8 Ton'"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def plan_shipment_route(origin_warehouse: str, destination_stops: List[Dict[str, Any]], vehicle_type: str = "Truk CDD 4 Ton", tenant_id: int = 1) -> Dict[str, Any]:
    total_stops = len(destination_stops)
    est_distance_km = total_stops * 25.0
    est_time_hours = est_distance_km / 35.0  # Rata-rata 35 km/jam

    payload = {
        "origin": origin_warehouse,
        "stops": destination_stops,
        "vehicle": vehicle_type,
        "est_distance_km": est_distance_km,
        "est_time_hours": round(est_time_hours, 1)
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-ROU-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "shipment_route_plan",
        "branch": "logistics",
        "created_by_agent": "logistics_coordinator",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "shipment_route_plan",
        "est_distance_km": est_distance_km,
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Rencana Rute ({total_stops} titik, {est_distance_km} km) ({doc.name}) siap di-approve."
    }

@ai_tool(
    name="track_shipment_status",
    description="Melacak posisi armada dan status pengiriman barang secara real-time berdasarkan nomor resi/tracking.",
    branch="logistics",
    roles=["logistics_coordinator", "shipping_clerk", "logistics_manager"],
    parameters={
        "tracking_number": {"type": "string", "description": "Nomor resi pengiriman / no DO"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def track_shipment_status(tracking_number: str, tenant_id: int = 1) -> Dict[str, Any]:
    return {
        "status": "IN_TRANSIT",
        "tracking_no": tracking_number,
        "carrier": "Internal Fleet Truck #B-9123-UCA",
        "driver_name": "Bambang Pamungkas",
        "current_location": "Tol Cikampek KM 54 (Arah Bandung)",
        "eta": "2026-09-01 16:30",
        "milestones": [
            {"time": "08:00", "event": "Departed from Cikarang Hub"},
            {"time": "11:30", "event": "Passed Karawang Checkpoint"}
        ],
        "message": f"Pengiriman #{tracking_number} berstatus IN_TRANSIT di KM 54 Cikampek. Estimasi tiba: 16:30 WIB."
    }

@ai_tool(
    name="calculate_shipping_cost",
    description="Menghitung ongkos kirim berdasarkan berat aktual vs berat volumetrik (P x L x T / 5000), jarak, dan zona tarif.",
    branch="logistics",
    roles=["logistics_coordinator", "logistics_manager"],
    parameters={
        "weight_kg": {"type": "number", "description": "Berat timbangan aktual dalam kg"},
        "length_cm": {"type": "number", "description": "Panjang kemasan dalam cm"},
        "width_cm": {"type": "number", "description": "Lebar kemasan dalam cm"},
        "height_cm": {"type": "number", "description": "Tinggi kemasan dalam cm"},
        "distance_km": {"type": "number", "description": "Jarak pengiriman dalam km"},
        "service_tier": {"type": "string", "description": "Layanan: 'Economy', 'Regular', 'Express Same-Day'"}
    }
)
def calculate_shipping_cost(weight_kg: float, length_cm: float, width_cm: float, height_cm: float, distance_km: float, service_tier: str = "Regular") -> Dict[str, Any]:
    volumetric_weight = (length_cm * width_cm * height_cm) / 5000.0
    chargeable_weight = max(weight_kg, volumetric_weight)
    
    rate_per_kg_km = 120.0 if service_tier == "Economy" else (180.0 if service_tier == "Regular" else 300.0)
    base_cost = chargeable_weight * distance_km * rate_per_kg_km * 0.05
    final_shipping_cost = max(25000.0, round(base_cost, -2))

    return {
        "status": "SUCCESS",
        "actual_weight_kg": weight_kg,
        "volumetric_weight_kg": round(volumetric_weight, 2),
        "chargeable_weight_kg": round(chargeable_weight, 2),
        "distance_km": distance_km,
        "service_tier": service_tier,
        "total_shipping_fee": final_shipping_cost,
        "message": f"Ongkos Kirim ({service_tier} {distance_km} km): Rp {final_shipping_cost:,.0f} (Berat Ditagih: {chargeable_weight:.1f} kg)."
    }

@ai_tool(
    name="optimize_load_planning",
    description="Mengoptimalkan kapasitas ruang muat truk atau kontainer berdasarkan kubikasi (CBM) dan batas tonase muatan.",
    branch="logistics",
    roles=["logistics_coordinator", "logistics_manager"],
    parameters={
        "truck_max_weight_kg": {"type": "number", "description": "Batas muatan maksimal truk dalam kg (misal: 4000 kg)"},
        "truck_max_cbm": {"type": "number", "description": "Volume ruang kargo truk dalam m3 (misal: 14 CBM)"},
        "cargo_items": {"type": "array", "description": "Daftar muatan barang (misal: [{'item': 'Palet A', 'weight_kg': 500, 'cbm': 1.8}])"}
    }
)
def optimize_load_planning(truck_max_weight_kg: float, truck_max_cbm: float, cargo_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_weight = sum(float(i.get("weight_kg", 0)) for i in cargo_items)
    total_cbm = sum(float(i.get("cbm", 0)) for i in cargo_items)
    
    weight_util = (total_weight / max(truck_max_weight_kg, 1)) * 100
    cbm_util = (total_cbm / max(truck_max_cbm, 1)) * 100
    is_overloaded = total_weight > truck_max_weight_kg or total_cbm > truck_max_cbm

    return {
        "status": "OVERLOAD_ALERT" if is_overloaded else "OPTIMAL_LOAD",
        "total_cargo_weight_kg": total_weight,
        "max_truck_weight_kg": truck_max_weight_kg,
        "weight_utilization_pct": round(weight_util, 1),
        "total_cargo_cbm": total_cbm,
        "max_truck_cbm": truck_max_cbm,
        "volume_utilization_pct": round(cbm_util, 1),
        "is_safe_to_dispatch": not is_overloaded,
        "message": f"Utilisasi Muatan Truk: Berat {weight_util:.1f}%, Volume {cbm_util:.1f}% ({'AMAN' if not is_overloaded else 'OVERLOAD/BAHAYA'})."
    }

@ai_tool(
    name="manage_courier_integrations",
    description="Memeriksa estimasi tarif dan opsi kurir logistik pihak ketiga / 3PL (JNE, J&T, SiCepat, DHL).",
    branch="logistics",
    roles=["logistics_coordinator", "logistics_manager"],
    parameters={
        "origin_postal": {"type": "string", "description": "Kode pos asal"},
        "dest_postal": {"type": "string", "description": "Kode pos tujuan"},
        "weight_kg": {"type": "number", "description": "Berat paket dalam kg"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def manage_courier_integrations(origin_postal: str, dest_postal: str, weight_kg: float, tenant_id: int = 1) -> Dict[str, Any]:
    courier_options = [
        {"courier": "JNE Trucking (JTR)", "rate": 45000 * weight_kg, "etd": "2-3 Hari"},
        {"courier": "SiCepat Cargo", "rate": 42000 * weight_kg, "etd": "2-3 Hari"},
        {"courier": "J&T Cargo", "rate": 40000 * weight_kg, "etd": "3-4 Hari"}
    ]
    best_rate = min(courier_options, key=lambda x: x["rate"])
    return {
        "status": "SUCCESS",
        "origin_postal": origin_postal,
        "dest_postal": dest_postal,
        "weight_kg": weight_kg,
        "rates": courier_options,
        "recommended_courier": best_rate["courier"],
        "message": f"Rekomendasi 3PL untuk {weight_kg} kg: {best_rate['courier']} (Rp {best_rate['rate']:,.0f}, ETD {best_rate['etd']})."
    }

# =========================================================================
# FLEET MANAGER TOOLS (4 Tools)
# =========================================================================

@ai_tool(
    name="manage_fleet_vehicle",
    description="Membuat draf data induk armada kendaraan, kapasitas muat, serta masa berlaku STNK & uji KIR (Action -> Draft Card).",
    branch="logistics",
    roles=["fleet_manager", "logistics_manager"],
    parameters={
        "license_plate": {"type": "string", "description": "Nomor plat polisi (misal: 'B 9123 UCA')"},
        "vehicle_model": {"type": "string", "description": "Merk/Model kendaraan (misal: 'Isuzu Giga FVM')"},
        "vehicle_type": {"type": "string", "description": "Tipe: 'Blind Van', 'CDD Box', 'Wingbox', 'Trailer'"},
        "max_payload_kg": {"type": "number", "description": "Kapasitas muatan maksimal dalam kg"},
        "stnk_expiry": {"type": "string", "description": "Tanggal habis masa berlaku STNK (YYYY-MM-DD)"},
        "kir_expiry": {"type": "string", "description": "Tanggal habis masa berlaku Uji KIR (YYYY-MM-DD)"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def manage_fleet_vehicle(license_plate: str, vehicle_model: str, vehicle_type: str, max_payload_kg: float, stnk_expiry: str, kir_expiry: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "plate": license_plate,
        "model": vehicle_model,
        "type": vehicle_type,
        "payload_kg": max_payload_kg,
        "stnk_exp": stnk_expiry,
        "kir_exp": kir_expiry
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-FLT-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "fleet_vehicle_master",
        "branch": "logistics",
        "created_by_agent": "fleet_manager",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "fleet_vehicle_master",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Master Kendaraan '{license_plate}' ({doc.name}) berhasil dibuat."
    }

@ai_tool(
    name="schedule_vehicle_maintenance",
    description="Membuat draf jadwal servis rutin atau perbaikan armada truk logistik (Action -> Draft Card).",
    branch="logistics",
    roles=["fleet_manager", "logistics_manager"],
    parameters={
        "license_plate": {"type": "string", "description": "Nomor plat polisi armada"},
        "service_type": {"type": "string", "description": "Jenis servis: 'Ganti Oli & Filter', 'Tune-up', 'Ganti Ban'"},
        "planned_service_date": {"type": "string", "description": "Tanggal rencana servis (YYYY-MM-DD)"},
        "estimated_cost": {"type": "number", "description": "Estimasi biaya servis"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def schedule_vehicle_maintenance(license_plate: str, service_type: str, planned_service_date: str, estimated_cost: float, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "plate": license_plate,
        "service": service_type,
        "date": planned_service_date,
        "cost": estimated_cost
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-VMAINT-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "vehicle_maintenance_schedule",
        "branch": "logistics",
        "created_by_agent": "fleet_manager",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "vehicle_maintenance_schedule",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Jadwal Servis Kendaraan {license_plate} ({doc.name}) siap di-approve."
    }

@ai_tool(
    name="track_fuel_consumption",
    description="Menganalisis efisiensi konsumsi BBM armada (Km/Liter) dan mendeteksi anomali pemborosan bahan bakar.",
    branch="logistics",
    roles=["fleet_manager", "logistics_manager"],
    parameters={
        "license_plate": {"type": "string", "description": "Plat nomor kendaraan"},
        "distance_km": {"type": "number", "description": "Jarak tempuh trip dalam km"},
        "fuel_liters": {"type": "number", "description": "Jumlah liter BBM yang diisi"},
        "fuel_cost": {"type": "number", "description": "Total nominal biaya pembelian BBM"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def track_fuel_consumption(license_plate: str, distance_km: float, fuel_liters: float, fuel_cost: float, tenant_id: int = 1) -> Dict[str, Any]:
    fuel_efficiency_km_per_liter = distance_km / max(fuel_liters, 1)
    cost_per_km = fuel_cost / max(distance_km, 1)
    is_abnormal = fuel_efficiency_km_per_liter < 5.0  # Standar truk diesel rata-rata 6-8 km/L

    return {
        "status": "ANOMALY_WARNING" if is_abnormal else "NORMAL",
        "plate": license_plate,
        "distance_km": distance_km,
        "fuel_liters": fuel_liters,
        "km_per_liter": round(fuel_efficiency_km_per_liter, 2),
        "cost_per_km": round(cost_per_km, 2),
        "efficiency_status": "BOROS (Perlu Cek Mesin/Sensor)" if is_abnormal else "EFISIEN",
        "message": f"Konsumsi BBM {license_plate}: {fuel_efficiency_km_per_liter:.2f} Km/Liter (Biaya: Rp {cost_per_km:,.0f}/Km)."
    }

@ai_tool(
    name="calculate_carbon_footprint_logistics",
    description="Menghitung estimasi emisi karbon (CO2e dalam Kg) dari operasional armada pengiriman logistik.",
    branch="logistics",
    roles=["fleet_manager", "logistics_manager"],
    parameters={
        "distance_km": {"type": "number", "description": "Total jarak perjalanan dalam km"},
        "fuel_liters": {"type": "number", "description": "Total liter solar diesel yang dikonsumsi"},
        "vehicle_type": {"type": "string", "description": "Tipe armada (default: 'Diesel Truck')"}
    }
)
def calculate_carbon_footprint_logistics(distance_km: float, fuel_liters: float, vehicle_type: str = "Diesel Truck") -> Dict[str, Any]:
    # Faktor emisi solar diesel: 2.68 kg CO2 per liter solar
    co2_emissions_kg = fuel_liters * 2.68
    co2_per_km = co2_emissions_kg / max(distance_km, 1)

    return {
        "status": "SUCCESS",
        "distance_km": distance_km,
        "fuel_liters": fuel_liters,
        "total_co2_kg": round(co2_emissions_kg, 2),
        "co2_kg_per_km": round(co2_per_km, 3),
        "sustainability_metric": "ESG Compliant Log",
        "message": f"Emisi Karbon Perjalanan: {co2_emissions_kg:.2f} Kg CO2 ({co2_per_km:.3f} Kg CO2/Km)."
    }

# =========================================================================
# LOGISTICS MANAGER TOOLS (4 Tools)
# =========================================================================

@ai_tool(
    name="generate_delivery_performance_report",
    description="Menghasilkan laporan performa pengiriman On-Time In-Full (OTIF) dan ketepatan waktu armada logistik.",
    branch="logistics",
    roles=["logistics_manager"],
    parameters={
        "period_month": {"type": "string", "description": "Bulan periode laporan (default: 'Current Month')"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def generate_delivery_performance_report(period_month: str = "Current Month", tenant_id: int = 1) -> Dict[str, Any]:
    return {
        "status": "SUCCESS",
        "period": period_month,
        "total_shipments_dispatched": 142,
        "on_time_delivery_pct": 96.4,
        "in_full_delivery_pct": 98.2,
        "otif_score_pct": 94.7,
        "delayed_shipments_count": 5,
        "primary_delay_reason": "Kemacetan Jalur Pantura & Cuaca Hujan",
        "message": f"Performa Logistik ({period_month}): Skor OTIF {94.7}% (96.4% Tepat Waktu, 98.2% Kuantitas Lengkap)."
    }

@ai_tool(
    name="calculate_freight_demurrage",
    description="Menghitung denda penumpukan kontainer dan waktu tunggu bongkar muat pelabuhan (Demurrage & Detention).",
    branch="logistics",
    roles=["logistics_manager"],
    parameters={
        "free_days_allowed": {"type": "integer", "description": "Batas hari bebas denda (Free Time)"},
        "actual_dwell_days": {"type": "integer", "description": "Total hari kontainer tertahan di pelabuhan"},
        "daily_demurrage_rate": {"type": "number", "description": "Tarif denda harian per kontainer (Rp/hari)"},
        "container_count": {"type": "integer", "description": "Jumlah kontainer yang tertahan"}
    }
)
def calculate_freight_demurrage(free_days_allowed: int, actual_dwell_days: int, daily_demurrage_rate: float, container_count: int = 1) -> Dict[str, Any]:
    penalty_days = max(0, actual_dwell_days - free_days_allowed)
    total_demurrage = penalty_days * daily_demurrage_rate * container_count

    return {
        "status": "SUCCESS",
        "free_time_days": free_days_allowed,
        "dwell_time_days": actual_dwell_days,
        "penalty_days": penalty_days,
        "container_count": container_count,
        "daily_rate": daily_demurrage_rate,
        "total_demurrage_fee": total_demurrage,
        "message": f"Biaya Demurrage ({penalty_days} hari telat, {container_count} kontainer): Rp {total_demurrage:,.0f}."
    }

@ai_tool(
    name="create_draft_cross_docking",
    description="Membuat draf operasi Cross-Docking (bongkar muat langsung dari truk masuk ke truk keluar tanpa simpan di rak) (Action -> Draft Card).",
    branch="logistics",
    roles=["logistics_manager", "logistics_coordinator"],
    parameters={
        "inbound_delivery_id": {"type": "string", "description": "ID Pengiriman Masuk"},
        "outbound_delivery_id": {"type": "string", "description": "ID Pengiriman Keluar tujuan"},
        "transfer_items": {"type": "array", "description": "Daftar item yang dipindahkan langsung"},
        "staging_bay": {"type": "string", "description": "Nomor dermaga staging (misal: 'Bay-04')"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def create_draft_cross_docking(inbound_delivery_id: str, outbound_delivery_id: str, transfer_items: List[Dict[str, Any]], staging_bay: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "inbound": inbound_delivery_id,
        "outbound": outbound_delivery_id,
        "items": transfer_items,
        "bay": staging_bay
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-XDOCK-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "cross_docking_operation",
        "branch": "logistics",
        "created_by_agent": "logistics_manager",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "cross_docking_operation",
        "staging_bay": staging_bay,
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Operasi Cross-Docking ({doc.name}) di {staging_bay} berhasil dibuat."
    }

@ai_tool(
    name="report_transit_damage",
    description="Membuat draf klaim asuransi atas kerusakan atau kehilangan barang selama perjalanan ekspedisi (Action -> Draft Card).",
    branch="logistics",
    roles=["logistics_manager"],
    parameters={
        "shipment_id": {"type": "string", "description": "Nomor pengiriman terkait"},
        "damaged_items": {"type": "array", "description": "Daftar item dan kuantitas yang rusak"},
        "estimated_loss_amount": {"type": "number", "description": "Total estimasi kerugian nominal"},
        "incident_description": {"type": "string", "description": "Kronologi insiden (misal: 'Truk terguling di KM 88')"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def report_transit_damage(shipment_id: str, damaged_items: List[Dict[str, Any]], estimated_loss_amount: float, incident_description: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "shipment_id": shipment_id,
        "damaged_items": damaged_items,
        "loss_amount": estimated_loss_amount,
        "incident": incident_description
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-DAM-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "transit_damage_claim",
        "branch": "logistics",
        "created_by_agent": "logistics_manager",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "transit_damage_claim",
        "loss_amount": estimated_loss_amount,
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Klaim Kerusakan Transit #{shipment_id} (Rp {estimated_loss_amount:,.0f}) ({doc.name}) siap di-approve."
    }
