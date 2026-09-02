import os
import sqlite3
from typing import Dict, Any, List, Optional
from .adapters.base import BaseDatabaseAdapter, compute_schema_hash
from .adapters.sqlite_adapter import SQLiteAdapter
from .adapters.mysql_adapter import MySQLAdapter
from .adapters.postgres_adapter import PostgresAdapter

def create_adapter(engine: str, config: Dict[str, Any]) -> BaseDatabaseAdapter:
    eng = (engine or "sqlite").lower()
    if eng == "sqlite":
        return SQLiteAdapter(config)
    elif eng in ("mariadb", "mysql"):
        return MySQLAdapter(config)
    elif eng in ("postgres", "postgresql"):
        return PostgresAdapter(config)
    else:
        raise ValueError(f"Database engine tidak didukung: {engine}")

# SQL Schema dan Data Template ERP Standar untuk Provisioning
STANDARD_ERP_TEMPLATE_SQL = """
CREATE TABLE IF NOT EXISTS katalog_produk (
    kode_barang TEXT PRIMARY KEY,
    nama_barang TEXT NOT NULL,
    kategori TEXT,
    harga_satuan NUMERIC(14,2),
    stok_tersedia INTEGER
);

CREATE TABLE IF NOT EXISTS daftar_pelanggan (
    kode_pelanggan TEXT PRIMARY KEY,
    nama_pelanggan TEXT NOT NULL,
    nomor_telepon TEXT,
    email TEXT,
    kota TEXT
);

CREATE TABLE IF NOT EXISTS data_karyawan (
    nik TEXT PRIMARY KEY,
    nama_karyawan TEXT NOT NULL,
    jabatan TEXT,
    divisi TEXT,
    gaji_pokok NUMERIC(12,2),
    tanggal_masuk DATE
);

CREATE TABLE IF NOT EXISTS transaksi_penjualan (
    no_nota TEXT PRIMARY KEY,
    tanggal DATE NOT NULL,
    kode_pelanggan TEXT,
    kode_barang TEXT,
    jumlah INTEGER,
    total_bayar NUMERIC(14,2),
    status_order TEXT,
    FOREIGN KEY (kode_pelanggan) REFERENCES daftar_pelanggan(kode_pelanggan),
    FOREIGN KEY (kode_barang) REFERENCES katalog_produk(kode_barang)
);

CREATE TABLE IF NOT EXISTS pengeluaran_pembelian (
    no_po TEXT PRIMARY KEY,
    tanggal DATE NOT NULL,
    pemasok TEXT,
    total NUMERIC(14,2),
    status TEXT
);

DELETE FROM katalog_produk;
INSERT INTO katalog_produk (kode_barang, nama_barang, kategori, harga_satuan, stok_tersedia) VALUES
    ('P001', 'Kopi Arabika Gayo 200g', 'Minuman', 45000, 120),
    ('P002', 'Teh Melati Premium 100g', 'Minuman', 28000, 85),
    ('P003', 'Gula Aren Cair 250ml', 'Bahan Pokok', 32000, 40),
    ('P004', 'Keripik Singkong Balado', 'Snack', 15000, 200),
    ('P005', 'Sambal Bawang Bu Rina', 'Bumbu', 25000, 65),
    ('P006', 'Beras Merah Organik 1kg', 'Bahan Pokok', 38000, 90),
    ('P007', 'Madu Hutan Murni 350ml', 'Minuman', 95000, 25),
    ('P008', 'Kerupuk Udang Kelas Premium', 'Snack', 22000, 150);

DELETE FROM daftar_pelanggan;
INSERT INTO daftar_pelanggan (kode_pelanggan, nama_pelanggan, nomor_telepon, email, kota) VALUES
    ('C001', 'Warung Bu Sri', '081234567001', 'busri@mail.com', 'Bandung'),
    ('C002', 'Toko Berkah Jaya', '081234567002', 'berkah@mail.com', 'Jakarta'),
    ('C003', 'Cafe Kopi Senja', '081234567003', 'senja@mail.com', 'Yogyakarta'),
    ('C004', 'Resto Nusantara', '081234567004', 'nusantara@mail.com', 'Surabaya'),
    ('C005', 'Minimarket Sejahtera', '081234567005', 'sejahtera@mail.com', 'Semarang'),
    ('C006', 'Kantin Bu Joko', '081234567006', 'bujoko@mail.com', 'Jakarta'),
    ('C007', 'Depot Makmur', '081234567007', 'makmur@mail.com', 'Malang'),
    ('C008', 'Dapur Mama', '081234567008', 'dapurmama@mail.com', 'Denpasar');

DELETE FROM data_karyawan;
INSERT INTO data_karyawan (nik, nama_karyawan, jabatan, divisi, gaji_pokok, tanggal_masuk) VALUES
    ('K001', 'Budi Santoso', 'Financial Analyst', 'Finance', 8500000, '2023-01-15'),
    ('K002', 'Siti Rahmawati', 'Budgeting Staff', 'Finance', 6500000, '2023-03-01'),
    ('K003', 'Ahmad Fadillah', 'Sales Executive', 'Sales', 6000000, '2023-04-10'),
    ('K004', 'Dewi Lestari', 'HR Specialist', 'HR', 7000000, '2022-11-01'),
    ('K005', 'Rudi Hermawan', 'Inventory Officer', 'Supply Chain', 5800000, '2023-06-15'),
    ('K006', 'Maya Anggraini', 'Procurement Officer', 'Procurement', 6200000, '2023-02-20'),
    ('K007', 'Hendra Setiawan', 'Tax Specialist', 'Finance', 7500000, '2022-08-15'),
    ('K008', 'Dina Kartika', 'Customer Care Lead', 'Sales', 6800000, '2023-05-05');

DELETE FROM transaksi_penjualan;
INSERT INTO transaksi_penjualan (no_nota, tanggal, kode_pelanggan, kode_barang, jumlah, total_bayar, status_order) VALUES
    ('INV-2026-001', '2026-08-01', 'C001', 'P001', 10, 450000, 'LUNAS'),
    ('INV-2026-002', '2026-08-02', 'C002', 'P004', 30, 450000, 'LUNAS'),
    ('INV-2026-003', '2026-08-05', 'C003', 'P001', 25, 1125000, 'LUNAS'),
    ('INV-2026-004', '2026-08-08', 'C004', 'P006', 15, 570000, 'LUNAS'),
    ('INV-2026-005', '2026-08-10', 'C005', 'P007', 5, 475000, 'PENDING'),
    ('INV-2026-006', '2026-08-12', 'C001', 'P003', 12, 384000, 'LUNAS'),
    ('INV-2026-007', '2026-08-15', 'C006', 'P002', 20, 560000, 'LUNAS'),
    ('INV-2026-008', '2026-08-18', 'C002', 'P008', 15, 330000, 'LUNAS'),
    ('INV-2026-009', '2026-08-20', 'C007', 'P005', 18, 450000, 'PENDING'),
    ('INV-2026-010', '2026-08-25', 'C008', 'P004', 40, 600000, 'LUNAS');

DELETE FROM pengeluaran_pembelian;
INSERT INTO pengeluaran_pembelian (no_po, tanggal, pemasok, total, status) VALUES
    ('PO-2026-001', '2026-08-01', 'PT Kopi Nusantara Jaya', 3500000, 'SELESAI'),
    ('PO-2026-002', '2026-08-03', 'CV Kemasan Prima', 1200000, 'SELESAI'),
    ('PO-2026-003', '2026-08-07', 'UD Sumber Tani Organik', 2800000, 'SELESAI'),
    ('PO-2026-004', '2026-08-11', 'PT Logistik Cepat Sentosa', 850000, 'SELESAI'),
    ('PO-2026-005', '2026-08-15', 'CV Bahan Pangan Sejahtera', 2100000, 'PROSES'),
    ('PO-2026-006', '2026-08-18', 'PT Label & Percetakan Indah', 950000, 'SELESAI'),
    ('PO-2026-007', '2026-08-22', 'UD Madu Hutan Lestari', 1800000, 'SELESAI'),
    ('PO-2026-008', '2026-08-26', 'CV Gula Aren Tradisional', 1100000, 'PROSES');
"""

def provision_sqlite_database(target_dir: str, tenant_name: str, mode: str = "template", custom_tables: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    os.makedirs(target_dir, exist_ok=True)
    safe_name = "".join(c for c in tenant_name.lower() if c.isalnum() or c in ("_", "-")) or "client"
    db_file = os.path.join(target_dir, f"client_{safe_name}.db")

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    if mode == "template":
        cur.executescript(STANDARD_ERP_TEMPLATE_SQL)
    elif mode == "custom" and custom_tables:
        for t in custom_tables:
            t_name = t.get("name", "").strip()
            cols = t.get("columns", [])
            if not t_name or not cols:
                continue
            col_defs = []
            for c in cols:
                c_name = c.get("name", "").strip()
                c_type = (c.get("type") or "text").upper()
                if c_name:
                    col_defs.append(f'"{c_name}" {c_type}')
            if col_defs:
                cur.execute(f'CREATE TABLE IF NOT EXISTS "{t_name}" ({", ".join(col_defs)})')

    conn.commit()
    conn.close()

    adapter = SQLiteAdapter({"path": db_file})
    schema = adapter.extract_schema()
    s_hash = compute_schema_hash(schema)

    return {
        "engine": "sqlite",
        "file_path": db_file,
        "database_name": f"client_{safe_name}.db",
        "schema": schema,
        "schema_hash": s_hash,
        "tables_count": schema.get("tables_count", 0)
    }
