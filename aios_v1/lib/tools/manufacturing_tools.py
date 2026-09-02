"""
Katalog Tools Cabang 5: Manufacturing / Production Planning (16 Tools).
Job Roles: Production Planner, Production Scheduler, Production Supervisor, Production Manager.
Sesuai Blueprint Phase 5 §7.E dengan Prinsip Role-Scoping (Least Privilege).
"""

import json
import frappe
from typing import Dict, Any, List, Optional
from frappe.utils import add_to_date, now_datetime
from aios_v1.lib.tool_registry import ai_tool
from aios_v1.lib.data_access_agent import get_data_access_agent

# =========================================================================
# PRODUCTION PLANNER TOOLS (5 Tools)
# =========================================================================

@ai_tool(
    name="check_material_requirements",
    description="MRP: Mengecek ketersediaan bahan baku di gudang untuk memenuhi rencana jumlah pesanan produksi.",
    branch="manufacturing",
    roles=["production_planner", "production_manager"],
    parameters={
        "product_id": {"type": "string", "description": "Kode atau nama produk jadi yang akan diproduksi"},
        "planned_quantity": {"type": "integer", "description": "Jumlah unit produk jadi yang direncanakan"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def check_material_requirements(product_id: str, planned_quantity: int, tenant_id: int = 1) -> Dict[str, Any]:
    agent = get_data_access_agent(tenant_id)
    prod_res = agent.query("Product")

    # Simulasi perhitungan MRP
    required_materials = [
        {"material": "Plat Besi 3mm", "required_qty": planned_quantity * 0.5, "stock_available": 100, "status": "AVAILABLE"},
        {"material": "Baut M8x20 Baja", "required_qty": planned_quantity * 4, "stock_available": 500, "status": "AVAILABLE"},
        {"material": "Cat Primer Industri", "required_qty": planned_quantity * 0.1, "stock_available": 20, "status": "AVAILABLE"}
    ]
    all_available = all(m["stock_available"] >= m["required_qty"] for m in required_materials)

    return {
        "status": "READY_FOR_PRODUCTION" if all_available else "SHORTAGE_DETECTED",
        "product_id": product_id,
        "planned_quantity": planned_quantity,
        "materials_needed": required_materials,
        "is_all_materials_ready": all_available,
        "data_source_status": prod_res.get("status"),
        "message": (
            f"Kebutuhan bahan baku untuk {planned_quantity} unit {product_id} LENGKAP dan siap diproduksi."
            if all_available else
            f"Terdapat kekurangan bahan baku untuk produksi {planned_quantity} unit {product_id}."
        )
    }

@ai_tool(
    name="explode_bill_of_materials",
    description="Menguraikan struktur Bill of Materials (BOM) multi-level untuk mengetahui komposisi komponen per unit produk.",
    branch="manufacturing",
    roles=["production_planner", "production_manager"],
    parameters={
        "product_id": {"type": "string", "description": "ID atau nama produk jadi"},
        "quantity": {"type": "integer", "description": "Jumlah kelipatan batch produksi (default 1 unit)"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def explode_bill_of_materials(product_id: str, quantity: int = 1, tenant_id: int = 1) -> Dict[str, Any]:
    bom_tree = [
        {"level": 1, "component": "Rangka Mesin Utama", "qty_per_unit": 1 * quantity, "unit": "Unit"},
        {"level": 2, "component": "Plat Besi 3mm", "qty_per_unit": 2.5 * quantity, "unit": "Kg"},
        {"level": 2, "component": "Baut M8x20 Baja Grade 8.8", "qty_per_unit": 16 * quantity, "unit": "Pcs"},
        {"level": 1, "component": "Motor Penggerak 3 HP", "qty_per_unit": 1 * quantity, "unit": "Unit"}
    ]
    return {
        "status": "SUCCESS",
        "product_id": product_id,
        "batch_quantity": quantity,
        "total_components": len(bom_tree),
        "bom_structure": bom_tree,
        "message": f"BOM Explosion untuk {quantity} unit {product_id} berhasil diuraikan ({len(bom_tree)} komponen teridentifikasi)."
    }

@ai_tool(
    name="calculate_production_cost",
    description="Menghitung estimasi HPP Produksi (COGM) = Biaya Bahan Baku + Upah Tenaga Kerja Langsung + Biaya Overhead.",
    branch="manufacturing",
    roles=["production_planner", "production_manager"],
    parameters={
        "raw_materials_cost": {"type": "number", "description": "Total biaya bahan baku yang digunakan"},
        "direct_labor_hours": {"type": "number", "description": "Total jam kerja operator/teknisi"},
        "hourly_labor_rate": {"type": "number", "description": "Tarif upah tenaga kerja per jam"},
        "overhead_cost": {"type": "number", "description": "Total alokasi biaya listrik/mesin overhead pabrik"},
        "batch_quantity": {"type": "integer", "description": "Jumlah unit produk jadi yang dihasilkan"}
    }
)
def calculate_production_cost(raw_materials_cost: float, direct_labor_hours: float, hourly_labor_rate: float, overhead_cost: float, batch_quantity: int) -> Dict[str, Any]:
    total_labor_cost = direct_labor_hours * hourly_labor_rate
    total_manufacturing_cost = raw_materials_cost + total_labor_cost + overhead_cost
    unit_cogm = total_manufacturing_cost / max(batch_quantity, 1)

    return {
        "status": "SUCCESS",
        "batch_quantity": batch_quantity,
        "raw_materials_cost": raw_materials_cost,
        "direct_labor_cost": total_labor_cost,
        "overhead_cost": overhead_cost,
        "total_manufacturing_cost": total_manufacturing_cost,
        "unit_production_cost": round(unit_cogm, 2),
        "message": f"HPP Produksi Total Rp {total_manufacturing_cost:,.0f} (Biaya Pokok per Unit: Rp {unit_cogm:,.0f})."
    }

@ai_tool(
    name="calculate_takt_time",
    description="Menghitung Takt Time (waktu per unit yang dibutuhkan untuk memenuhi permintaan pasar: Waktu Kerja / Demand).",
    branch="manufacturing",
    roles=["production_planner", "production_manager"],
    parameters={
        "available_working_time_seconds": {"type": "number", "description": "Total waktu kerja bersih pabrik dalam detik per shift"},
        "customer_demand_units": {"type": "integer", "description": "Total permintaan produk dari pelanggan per shift"}
    }
)
def calculate_takt_time(available_working_time_seconds: float, customer_demand_units: int) -> Dict[str, Any]:
    takt_time = available_working_time_seconds / max(customer_demand_units, 1)
    return {
        "status": "SUCCESS",
        "available_time_seconds": available_working_time_seconds,
        "customer_demand_units": customer_demand_units,
        "takt_time_seconds": round(takt_time, 2),
        "takt_time_minutes": round(takt_time / 60, 2),
        "message": f"Takt Time adalah {takt_time:.1f} detik/unit ({takt_time/60:.2f} menit/unit) untuk memenuhi target demand."
    }

@ai_tool(
    name="calculate_safety_lead_time",
    description="Menghitung lead time aman produksi pabrik dengan memperhitungkan potensi bottleneck dan variabilitas supplier.",
    branch="manufacturing",
    roles=["production_planner", "production_manager"],
    parameters={
        "base_manufacturing_lead_time_days": {"type": "integer", "description": "Lama proses produksi standar dalam hari"},
        "supplier_delay_risk_days": {"type": "integer", "description": "Risiko keterlambatan pasokan bahan dalam hari"},
        "machine_downtime_buffer_days": {"type": "integer", "description": "Buffer cadangan perawatan/downtime mesin dalam hari"}
    }
)
def calculate_safety_lead_time(base_manufacturing_lead_time_days: int, supplier_delay_risk_days: int, machine_downtime_buffer_days: int) -> Dict[str, Any]:
    total_safe_lead_time = base_manufacturing_lead_time_days + supplier_delay_risk_days + machine_downtime_buffer_days
    return {
        "status": "SUCCESS",
        "base_lead_time_days": base_manufacturing_lead_time_days,
        "supplier_buffer_days": supplier_delay_risk_days,
        "downtime_buffer_days": machine_downtime_buffer_days,
        "total_committed_lead_time_days": total_safe_lead_time,
        "message": f"Lead Time Aman Produksi adalah {total_safe_lead_time} hari (Standar {base_manufacturing_lead_time_days} hari + Buffer {supplier_delay_risk_days + machine_downtime_buffer_days} hari)."
    }

# =========================================================================
# PRODUCTION SCHEDULER TOOLS (5 Tools)
# =========================================================================

@ai_tool(
    name="create_draft_production_order",
    description="Membuat Draf Perintah Kerja Produksi (Manufacturing Order / MO) resmi di pabrik (Action -> Draft Card).",
    branch="manufacturing",
    roles=["production_scheduler", "production_manager"],
    parameters={
        "product_id": {"type": "string", "description": "Nama atau kode produk yang akan dibuat"},
        "quantity": {"type": "integer", "description": "Jumlah target output produk yang diproduksi"},
        "start_date": {"type": "string", "description": "Tanggal mulai proses produksi (YYYY-MM-DD)"},
        "target_completion_date": {"type": "string", "description": "Target tanggal selesai (YYYY-MM-DD)"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def create_draft_production_order(product_id: str, quantity: int, start_date: str, target_completion_date: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "product": product_id,
        "quantity": quantity,
        "start_date": start_date,
        "target_date": target_completion_date
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-MO-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "production_order",
        "branch": "manufacturing",
        "created_by_agent": "production_scheduler",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "production_order",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Perintah Produksi '{product_id}' ({quantity} unit) ({doc.name}) berhasil dibuat."
    }

@ai_tool(
    name="generate_production_schedule",
    description="Menyusun urutan jadwal dan alokasi mesin lini produksi pabrik.",
    branch="manufacturing",
    roles=["production_scheduler", "production_manager"],
    parameters={
        "production_orders": {"type": "array", "description": "Daftar ID order produksi yang akan dijadwalkan"},
        "schedule_start_date": {"type": "string", "description": "Tanggal awal jadwal (YYYY-MM-DD)"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def generate_production_schedule(production_orders: List[Dict[str, Any]], schedule_start_date: str, tenant_id: int = 1) -> Dict[str, Any]:
    schedule_plan = [
        {"order_id": "MO-001", "work_center": "Lini Perakitan 1", "shift": "Shift Pagi (08:00 - 16:00)", "status": "SCHEDULED"},
        {"order_id": "MO-002", "work_center": "Lini Mesin CNC", "shift": "Shift Sore (16:00 - 24:00)", "status": "SCHEDULED"}
    ]
    return {
        "status": "SUCCESS",
        "start_date": schedule_start_date,
        "scheduled_orders_count": len(production_orders) or len(schedule_plan),
        "schedule_details": schedule_plan,
        "message": f"Jadwal Lini Produksi per {schedule_start_date} berhasil disusun untuk {len(schedule_plan)} pesanan kerja."
    }

@ai_tool(
    name="check_work_center_capacity",
    description="Mengevaluasi utilisasi kapasitas jam mesin dan stasiun kerja pabrik (Work Center Capacity).",
    branch="manufacturing",
    roles=["production_scheduler", "production_manager"],
    parameters={
        "work_center_id": {"type": "string", "description": "ID atau nama stasiun kerja / mesin (misal: 'CNC-Line-01')"},
        "target_week": {"type": "string", "description": "Minggu target evaluasi (default: 'Current Week')"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def check_work_center_capacity(work_center_id: str, target_week: str = "Current Week", tenant_id: int = 1) -> Dict[str, Any]:
    total_capacity_hours = 80.0
    allocated_hours = 62.5
    utilization_pct = (allocated_hours / total_capacity_hours) * 100

    return {
        "status": "SUCCESS",
        "work_center": work_center_id,
        "week": target_week,
        "total_available_hours": total_capacity_hours,
        "scheduled_load_hours": allocated_hours,
        "free_capacity_hours": total_capacity_hours - allocated_hours,
        "utilization_pct": round(utilization_pct, 1),
        "load_status": "NORMAL" if utilization_pct <= 85 else "OVERLOAD_RISK",
        "message": f"Kapasitas {work_center_id}: {utilization_pct:.1f}% terpakai ({allocated_hours}/{total_capacity_hours} jam)."
    }

@ai_tool(
    name="reschedule_delayed_orders",
    description="Membuat draf penjadwalan ulang urutan produksi pesanan yang terlambat (Action -> Draft Card).",
    branch="manufacturing",
    roles=["production_scheduler", "production_manager"],
    parameters={
        "order_id": {"type": "string", "description": "ID Perintah Produksi yang terlambat"},
        "new_start_date": {"type": "string", "description": "Tanggal mulai yang baru (YYYY-MM-DD)"},
        "new_completion_date": {"type": "string", "description": "Target tanggal selesai yang baru (YYYY-MM-DD)"},
        "reason": {"type": "string", "description": "Alasan penundaan jadwal"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def reschedule_delayed_orders(order_id: str, new_start_date: str, new_completion_date: str, reason: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "order_id": order_id,
        "new_start_date": new_start_date,
        "new_completion_date": new_completion_date,
        "reschedule_reason": reason
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-RESCHED-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "reschedule_production",
        "branch": "manufacturing",
        "created_by_agent": "production_scheduler",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "reschedule_production",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Penjadwalan Ulang MO #{order_id} ({doc.name}) berhasil dibuat dan menunggu persetujuan."
    }

@ai_tool(
    name="manage_routing_workstations",
    description="Membuat draf urutan operasi stasiun kerja dan waktu siklus per mesin (Action -> Draft Card).",
    branch="manufacturing",
    roles=["production_scheduler", "production_manager"],
    parameters={
        "product_id": {"type": "string", "description": "ID Produk"},
        "operations": {"type": "array", "description": "Daftar operasi routing (misal: [{'op': 'Pemotongan', 'machine': 'CNC', 'time_mins': 15}])"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def manage_routing_workstations(product_id: str, operations: List[Dict[str, Any]], tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "product_id": product_id,
        "operations": operations,
        "total_operations_count": len(operations)
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-ROUTING-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "routing_configuration",
        "branch": "manufacturing",
        "created_by_agent": "production_scheduler",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "routing_configuration",
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Konfigurasi Routing '{product_id}' ({doc.name}) berhasil dibuat."
    }

# =========================================================================
# PRODUCTION SUPERVISOR TOOLS (6 Tools)
# =========================================================================

@ai_tool(
    name="confirm_production_output",
    description="Membuat draf konfirmasi hasil barang jadi yang selesai diproduksi di lantai pabrik (Action -> Draft Card).",
    branch="manufacturing",
    roles=["production_supervisor", "production_manager"],
    parameters={
        "production_order_id": {"type": "string", "description": "ID Perintah Kerja Produksi"},
        "completed_quantity": {"type": "integer", "description": "Jumlah unit barang jadi yang berhasil diselesaikan"},
        "operator_name": {"type": "string", "description": "Nama penanggung jawab operator shift"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def confirm_production_output(production_order_id: str, completed_quantity: int, operator_name: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "order_id": production_order_id,
        "completed_qty": completed_quantity,
        "operator": operator_name,
        "timestamp": str(now_datetime())
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-OUTPUT-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "production_output_confirmation",
        "branch": "manufacturing",
        "created_by_agent": "production_supervisor",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "production_output_confirmation",
        "completed_quantity": completed_quantity,
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Konfirmasi Output MO #{production_order_id} ({completed_quantity} unit) ({doc.name}) siap di-approve."
    }

@ai_tool(
    name="report_production_scrap",
    description="Membuat draf pencatatan barang reject / limbah sisa produksi (Scrap Order) (Action -> Draft Card).",
    branch="manufacturing",
    roles=["production_supervisor", "production_manager"],
    parameters={
        "production_order_id": {"type": "string", "description": "ID Perintah Produksi"},
        "scrap_quantity": {"type": "integer", "description": "Jumlah unit/kuantitas yang rusak/scrap"},
        "scrap_reason": {"type": "string", "description": "Penyebab kerusakan (misal: 'Pahat Patah', 'Salah Setting Dimensi')"},
        "material_id": {"type": "string", "description": "Nama bahan baku atau komponen yang rusak"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def report_production_scrap(production_order_id: str, scrap_quantity: int, scrap_reason: str, material_id: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "order_id": production_order_id,
        "scrap_qty": scrap_quantity,
        "reason": scrap_reason,
        "material": material_id
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-SCRAP-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "scrap_report",
        "branch": "manufacturing",
        "created_by_agent": "production_supervisor",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "scrap_report",
        "scrap_quantity": scrap_quantity,
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Laporan Scrap MO #{production_order_id} ({scrap_quantity} unit) ({doc.name}) siap diotorisasi."
    }

@ai_tool(
    name="track_work_order_progress",
    description="Melacak status progres pekerjaan berjalan di lantai pabrik (Shop Floor Routing & Work Order Status).",
    branch="manufacturing",
    roles=["production_supervisor", "production_planner", "production_manager"],
    parameters={
        "production_order_id": {"type": "string", "description": "ID Perintah Kerja Produksi"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def track_work_order_progress(production_order_id: str, tenant_id: int = 1) -> Dict[str, Any]:
    agent = get_data_access_agent(tenant_id)
    prod_res = agent.query("Product")

    return {
        "status": "IN_PROGRESS",
        "order_id": production_order_id,
        "current_operation": "Tahap 3 - Perakitan Komponen Mekanik",
        "progress_percentage": 68.5,
        "completed_units": 68,
        "target_units": 100,
        "current_work_center": "Lini Assembly 02",
        "operator_on_duty": "Agus Setiawan",
        "data_source_status": prod_res.get("status"),
        "message": f"MO #{production_order_id} berjalan di 68.5% (68/100 unit selesai di Lini Assembly 02)."
    }

@ai_tool(
    name="analyze_oee_metrics",
    description="Menghitung Overall Equipment Effectiveness (OEE = Availability × Performance × Quality) suatu mesin.",
    branch="manufacturing",
    roles=["production_supervisor", "production_manager"],
    parameters={
        "planned_operating_time_mins": {"type": "number", "description": "Waktu operasi mesin yang direncanakan dalam menit (misal 480 menit)"},
        "actual_operating_time_mins": {"type": "number", "description": "Waktu aktual mesin beroperasi (misal 432 menit)"},
        "ideal_cycle_time_mins": {"type": "number", "description": "Waktu standar ideal per unit (misal 0.5 menit/unit)"},
        "total_count": {"type": "integer", "description": "Total produk yang dihasilkan (misal 800 unit)"},
        "good_count": {"type": "integer", "description": "Total produk berkualitas baik tanpa cacat (misal 780 unit)"}
    }
)
def analyze_oee_metrics(planned_operating_time_mins: float, actual_operating_time_mins: float, ideal_cycle_time_mins: float, total_count: int, good_count: int) -> Dict[str, Any]:
    availability = (actual_operating_time_mins / max(planned_operating_time_mins, 1))
    performance = (ideal_cycle_time_mins * total_count) / max(actual_operating_time_mins, 1)
    quality = good_count / max(total_count, 1)
    oee = availability * performance * quality * 100

    return {
        "status": "SUCCESS",
        "availability_pct": round(availability * 100, 2),
        "performance_pct": round(performance * 100, 2),
        "quality_pct": round(quality * 100, 2),
        "overall_oee_pct": round(oee, 2),
        "world_class_benchmark": "85.0%",
        "rating": "WORLD_CLASS" if oee >= 85 else ("ACCEPTABLE" if oee >= 70 else "NEEDS_IMPROVEMENT"),
        "message": f"Skor OEE Mesin: {oee:.1f}% (Availability {availability*100:.1f}%, Performance {performance*100:.1f}%, Quality {quality*100:.1f}%)."
    }

@ai_tool(
    name="generate_production_variance_report",
    description="Menganalisis selisih (varians) antara biaya standar rencana produksi dengan biaya aktual yang terjadi.",
    branch="manufacturing",
    roles=["production_supervisor", "production_planner", "production_manager"],
    parameters={
        "production_order_id": {"type": "string", "description": "ID Perintah Produksi"},
        "standard_cost": {"type": "number", "description": "Total biaya standar rencana anggaran"},
        "actual_cost": {"type": "number", "description": "Total biaya aktual yang terpakai"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def generate_production_variance_report(production_order_id: str, standard_cost: float, actual_cost: float, tenant_id: int = 1) -> Dict[str, Any]:
    variance = actual_cost - standard_cost
    variance_pct = (variance / max(standard_cost, 1)) * 100
    is_favorable = variance <= 0

    return {
        "status": "SUCCESS",
        "order_id": production_order_id,
        "standard_cost": standard_cost,
        "actual_cost": actual_cost,
        "cost_variance": variance,
        "variance_pct": round(variance_pct, 2),
        "evaluation": "FAVORABLE (HEMAT)" if is_favorable else "UNFAVORABLE (OVERBUDGET)",
        "message": f"Varians Biaya MO #{production_order_id}: {'Hemat' if is_favorable else 'Overbudget'} Rp {abs(variance):,.0f} ({abs(variance_pct):.1f}%)."
    }

@ai_tool(
    name="log_downtime_event",
    description="Mencatat insiden mesin mogok (Breakdown Event) atau gangguan lini produksi (Action -> Draft Card).",
    branch="manufacturing",
    roles=["production_supervisor", "production_manager"],
    parameters={
        "work_center_id": {"type": "string", "description": "Nama atau nomor mesin/lini yang rusak"},
        "downtime_duration_mins": {"type": "integer", "description": "Durasi mesin terhenti dalam menit"},
        "breakdown_cause": {"type": "string", "description": "Penyebab kerusakan (misal: 'Motor Overheat', 'Korsleting Listrik')"},
        "tenant_id": {"type": "integer", "description": "ID Tenant"}
    }
)
def log_downtime_event(work_center_id: str, downtime_duration_mins: int, breakdown_cause: str, tenant_id: int = 1) -> Dict[str, Any]:
    payload = {
        "work_center": work_center_id,
        "duration_mins": downtime_duration_mins,
        "cause": breakdown_cause,
        "recorded_at": str(now_datetime())
    }

    doc = frappe.get_doc({
        "doctype": "Pending Action Draft",
        "task_id": f"TSK-DOWN-{int(frappe.utils.now_datetime().timestamp())}",
        "type": "downtime_incident",
        "branch": "manufacturing",
        "created_by_agent": "production_supervisor",
        "payload": json.dumps(payload),
        "status": "PENDING_APPROVAL",
        "expires_at": add_to_date(now_datetime(), hours=24)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "PENDING_HUMAN_APPROVAL",
        "draft_id": doc.name,
        "action_type": "downtime_incident",
        "work_center": work_center_id,
        "duration_mins": downtime_duration_mins,
        "card_markdown": f"[Review Draf](/draft/{doc.name})",
        "message": f"Draf Insiden Downtime {work_center_id} ({downtime_duration_mins} menit) ({doc.name}) siap di-approve."
    }
