"""
Unit Test Suite untuk AIOS Skills Engine & Loader (Role-Centric Architecture Opsi C - Tahap 6M.1 s/d 6M.5).
Menguji parser YAML frontmatter, path discovery hierarki <branch>/<role>/, smart caching, resolusi RBAC per role,
serta integritas 34 skills aktif di Orchestrator, Finance, Sales, dan Material.
"""

import os
import json
import unittest
import tempfile
import shutil
from pathlib import Path

import frappe
from aios_v1.lib.skills_loader import (
    parse_frontmatter,
    load_skill_from_file,
    load_all_skills,
    get_skill_by_slug,
    get_skills_for_worker,
    validate_skill_dependencies,
    compose_worker_system_prompt,
    clear_skills_cache,
    _normalize_role_variants,
    _SKILLS_CACHE
)


class TestSkillsEngine(unittest.TestCase):
    def setUp(self):
        clear_skills_cache()
        self.test_dir = tempfile.mkdtemp(prefix="aios_test_skills_")

    def tearDown(self):
        clear_skills_cache()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def _create_sample_skill_file(self, branch: str, role: str, filename: str, content: str) -> str:
        role_dir = os.path.join(self.test_dir, branch, role)
        os.makedirs(role_dir, exist_ok=True)
        file_path = os.path.join(role_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    # =========================================================================
    # 1. TEST PARSE FRONTMATTER
    # =========================================================================
    def test_01_parse_frontmatter_valid_and_edge_cases(self):
        """Memastikan parser YAML frontmatter memisahkan header dan body secara presisi."""
        raw_md = """---
name: "Financial Statement Analysis"
slug: "financial-statement-analysis"
version: "1.0.0"
branch: "finance"
role: "financial_analyst"
tools_required:
  - "generate_pnl_statement"
  - "calculate_financial_ratios"
triggers:
  - "analisis rasio"
  - "laporan pnl"
priority: "high"
---

# 1. Peran & Tujuan Bisnis
Menilai kesehatan finansial perusahaan.
"""
        metadata, body = parse_frontmatter(raw_md)
        self.assertEqual(metadata.get("name"), "Financial Statement Analysis")
        self.assertEqual(metadata.get("slug"), "financial-statement-analysis")
        self.assertEqual(metadata.get("role"), "financial_analyst")
        self.assertEqual(len(metadata.get("tools_required", [])), 2)
        self.assertIn("# 1. Peran & Tujuan Bisnis", body)

    # =========================================================================
    # 2. TEST LOAD SINGLE SKILL FROM FILE DENGAN PATH DISCOVERY
    # =========================================================================
    def test_02_load_skill_from_file_hierarchy(self):
        """Memastikan load_skill_from_file mengekstrak branch dan role dari hierarki direktori."""
        content = """---
name: "Cashflow Forecasting"
slug: "cashflow-forecasting"
version: "1.0.0"
tools_required:
  - "forecast_30d_cashflow"
priority: "critical"
---
# Content SOP
Periksa kas harian.
"""
        file_path = self._create_sample_skill_file("finance", "treasurer", "cashflow.md", content)
        skill = load_skill_from_file(file_path)

        self.assertIsNotNone(skill)
        self.assertEqual(skill["name"], "Cashflow Forecasting")
        self.assertEqual(skill["branch"], "finance")
        self.assertEqual(skill["role"], "treasurer")
        self.assertIn("treasurer", skill["roles"])
        self.assertEqual(skill["priority"], "critical")
        self.assertIn("forecast_30d_cashflow", skill["tools_required"])

    # =========================================================================
    # 3. TEST ROLE VARIANT NORMALIZATION
    # =========================================================================
    def test_03_normalize_role_variants(self):
        """Memastikan variasi nama peran (kebab-case, snake_case, space-case) dikenali setara."""
        variants_kebab = _normalize_role_variants("purchasing-officer")
        self.assertIn("purchasing-officer", variants_kebab)
        self.assertIn("purchasing_officer", variants_kebab)
        self.assertIn("purchasing officer", variants_kebab)

    # =========================================================================
    # 4. TEST ROLE-CENTRIC RBAC DISCOVERY (MATERIAL & CROSS-BRANCH)
    # =========================================================================
    def test_04_get_skills_for_worker_rbac_option_c(self):
        """Menguji pemisahan hak akses peran mandiri (Role-Centric)."""
        # 1. Inventory Clerk (3 skills di material/inventory_clerk/)
        ic_skills = get_skills_for_worker(branch="material", worker_key="inventory_clerk")
        ic_slugs = [s["slug"] for s in ic_skills]
        self.assertEqual(len(ic_slugs), 3)
        self.assertIn("stock-level-and-availability-check", ic_slugs)
        self.assertIn("goods-receipt-verification", ic_slugs)
        self.assertIn("physical-inventory-adjustment", ic_slugs)
        self.assertNotIn("purchase-order-procurement", ic_slugs)

        # 2. Purchasing Officer (2 skills di material/purchasing_officer/)
        po_skills = get_skills_for_worker(branch="material", worker_key="purchasing_officer")
        po_slugs = [s["slug"] for s in po_skills]
        self.assertEqual(len(po_slugs), 2)
        self.assertIn("purchase-order-procurement", po_slugs)
        self.assertIn("purchase-order-tracking-and-status", po_slugs)

        # 3. Sourcing Specialist (2 skills)
        src_skills = get_skills_for_worker(branch="material", worker_key="sourcing_specialist")
        src_slugs = [s["slug"] for s in src_skills]
        self.assertEqual(len(src_slugs), 2)
        self.assertIn("rfq-and-vendor-quote-comparison", src_slugs)
        self.assertIn("vendor-sla-and-abc-classification", src_slugs)

        # 4. Material Manager (10 skills Material + 3 skills Orchestrator = 13 skills)
        mgr_skills = get_skills_for_worker(branch="material", worker_key="manager")
        self.assertEqual(len(mgr_skills), 13)

    # =========================================================================
    # 5. TEST VALIDATE SKILL DEPENDENCIES
    # =========================================================================
    def test_05_validate_skill_dependencies(self):
        """Memastikan validasi dependensi tools_required mencocokkan ke _TOOL_REGISTRY."""
        valid_skill = {
            "name": "Financial Ratio Test",
            "slug": "test-valid",
            "tools_required": ["calculate_financial_ratios", "generate_pnl_statement"]
        }
        res_valid = validate_skill_dependencies(valid_skill)
        self.assertTrue(res_valid["valid"])
        self.assertEqual(len(res_valid["missing_tools"]), 0)

    # =========================================================================
    # 6. TEST COMPOSE WORKER SYSTEM PROMPT
    # =========================================================================
    def test_06_compose_worker_system_prompt(self):
        """Memastikan perakitan SOP ke dalam prompt berjalan rapi."""
        base_prompt = "Anda adalah Purchasing Officer profesional."
        composed = compose_worker_system_prompt(branch="material", worker_key="purchasing_officer", base_prompt=base_prompt)

        self.assertIn("Anda adalah Purchasing Officer profesional.", composed)
        self.assertIn("[STANDARD OPERATING PROCEDURES & WORKFLOW SKILLS]", composed)
        self.assertIn("Purchase Order Procurement", composed)
        self.assertIn("Purchase Order Tracking", composed)

    # =========================================================================
    # 7. TEST REAL SKILLS INTEGRITY (34 SKILLS: ORCHESTRATOR, FINANCE, SALES, MATERIAL)
    # =========================================================================
    def test_07_real_skills_integrity(self):
        """Menguji integritas seluruh 34 file skill nyata di direktori skills/ (Opsi C)."""
        all_skills = load_all_skills(force_reload=True)
        
        # Total harus 34 skills (3 Orchestrator + 11 Finance + 10 Sales + 10 Material)
        self.assertEqual(len(all_skills), 34, f"Ekspektasi 34 skills, ditemukan {len(all_skills)}: {list(all_skills.keys())}")

        # Pastikan validasi seluruh tools_required (100% dari 34 skills) valid di _TOOL_REGISTRY
        validation = validate_skill_dependencies()
        self.assertTrue(validation["valid"], f"Ada missing tools pada skills: {validation.get('missing_tools')}")
        self.assertEqual(len(validation["missing_tools"]), 0)


def run_tests():
    """Fungsi runner untuk dieksekusi via `bench execute`."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSkillsEngine)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    summary = {
        "success": result.wasSuccessful(),
        "total_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors)
    }
    print(json.dumps(summary, indent=2))
    return summary
