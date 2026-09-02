"""
Unit Test Suite untuk AIOS Skills Engine & Loader (Role-Centric Architecture Opsi C - Tahap 6M.1 s/d 6M.9).
Menguji parser YAML frontmatter, path discovery hierarki <branch>/<role>/, smart caching, resolusi RBAC per role,
serta integritas 70 skills aktif di Orchestrator, Finance, Sales, Material, HR, Manufacturing, Quality, dan Logistics.
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
name: "Freight Cost Optimization"
slug: "freight-cost-optimization"
version: "1.0.0"
branch: "logistics"
role: "logistics_coordinator"
tools_required:
  - "calculate_shipping_cost"
triggers:
  - "hitung ongkir"
priority: "high"
---

# 1. Peran & Tujuan Bisnis
Menghitung ongkos kirim kargo.
"""
        metadata, body = parse_frontmatter(raw_md)
        self.assertEqual(metadata.get("name"), "Freight Cost Optimization")
        self.assertEqual(metadata.get("slug"), "freight-cost-optimization")
        self.assertEqual(metadata.get("role"), "logistics_coordinator")
        self.assertEqual(len(metadata.get("tools_required", [])), 1)
        self.assertIn("# 1. Peran & Tujuan Bisnis", body)

    # =========================================================================
    # 2. TEST LOAD SINGLE SKILL FROM FILE DENGAN PATH DISCOVERY
    # =========================================================================
    def test_02_load_skill_from_file_hierarchy(self):
        """Memastikan load_skill_from_file mengekstrak branch dan role dari hierarki direktori."""
        content = """---
name: "Route Planning"
slug: "route-planning"
version: "1.0.0"
tools_required:
  - "plan_shipment_route"
priority: "high"
---
# Content SOP
Perencanaan rute truk.
"""
        file_path = self._create_sample_skill_file("logistics", "logistics_coordinator", "route.md", content)
        skill = load_skill_from_file(file_path)

        self.assertIsNotNone(skill)
        self.assertEqual(skill["name"], "Route Planning")
        self.assertEqual(skill["branch"], "logistics")
        self.assertEqual(skill["role"], "logistics_coordinator")
        self.assertIn("logistics_coordinator", skill["roles"])
        self.assertEqual(skill["priority"], "high")
        self.assertIn("plan_shipment_route", skill["tools_required"])

    # =========================================================================
    # 3. TEST ROLE VARIANT NORMALIZATION
    # =========================================================================
    def test_03_normalize_role_variants(self):
        """Memastikan variasi nama peran (kebab-case, snake_case, space-case) dikenali setara."""
        variants_kebab = _normalize_role_variants("logistics-coordinator")
        self.assertIn("logistics-coordinator", variants_kebab)
        self.assertIn("logistics_coordinator", variants_kebab)
        self.assertIn("logistics coordinator", variants_kebab)

    # =========================================================================
    # 4. TEST ROLE-CENTRIC RBAC DISCOVERY (LOGISTICS & CROSS-BRANCH)
    # =========================================================================
    def test_04_get_skills_for_worker_rbac_option_c(self):
        """Menguji pemisahan hak akses peran mandiri (Role-Centric Logistics)."""
        # 1. Shipping Clerk (2 skills di logistics/shipping_clerk/)
        shp_skills = get_skills_for_worker(branch="logistics", worker_key="shipping_clerk")
        shp_slugs = [s["slug"] for s in shp_skills]
        self.assertEqual(len(shp_slugs), 2)
        self.assertIn("inbound-and-outbound-delivery-order", shp_slugs)
        self.assertIn("warehouse-goods-movement-and-pod", shp_slugs)
        self.assertNotIn("route-planning-and-tracking", shp_slugs)

        # 2. Logistics Coordinator (3 skills di logistics/logistics_coordinator/)
        crd_skills = get_skills_for_worker(branch="logistics", worker_key="logistics_coordinator")
        crd_slugs = [s["slug"] for s in crd_skills]
        self.assertEqual(len(crd_slugs), 3)
        self.assertIn("route-planning-and-tracking", crd_slugs)
        self.assertIn("freight-cost-and-load-optimization", crd_slugs)
        self.assertIn("courier-integration-and-cross-docking", crd_slugs)

        # 3. Fleet Manager (2 skills di logistics/fleet_manager/)
        flt_skills = get_skills_for_worker(branch="logistics", worker_key="fleet_manager")
        flt_slugs = [s["slug"] for s in flt_skills]
        self.assertEqual(len(flt_slugs), 2)
        self.assertIn("vehicle-maintenance-and-fuel-log", flt_slugs)
        self.assertIn("driver-assignment-and-dispatch", flt_slugs)

        # 4. Logistics Manager (9 skills Logistics + 3 skills Orchestrator = 12 skills)
        mgr_skills = get_skills_for_worker(branch="logistics", worker_key="manager")
        self.assertEqual(len(mgr_skills), 12)

    # =========================================================================
    # 5. TEST VALIDATE SKILL DEPENDENCIES
    # =========================================================================
    def test_05_validate_skill_dependencies(self):
        """Memastikan validasi dependensi tools_required mencocokkan ke _TOOL_REGISTRY."""
        valid_skill = {
            "name": "Logistics Test",
            "slug": "test-valid-log",
            "tools_required": ["calculate_shipping_cost", "plan_shipment_route"]
        }
        res_valid = validate_skill_dependencies(valid_skill)
        self.assertTrue(res_valid["valid"])
        self.assertEqual(len(res_valid["missing_tools"]), 0)

    # =========================================================================
    # 6. TEST COMPOSE WORKER SYSTEM PROMPT
    # =========================================================================
    def test_06_compose_worker_system_prompt(self):
        """Memastikan perakitan SOP ke dalam prompt berjalan rapi."""
        base_prompt = "Anda adalah Logistics Coordinator berpengalaman."
        composed = compose_worker_system_prompt(branch="logistics", worker_key="logistics_coordinator", base_prompt=base_prompt)

        self.assertIn("Anda adalah Logistics Coordinator berpengalaman.", composed)
        self.assertIn("[STANDARD OPERATING PROCEDURES & WORKFLOW SKILLS]", composed)
        self.assertIn("Route Planning and Tracking", composed)
        self.assertIn("Freight Cost and Load Optimization", composed)

    # =========================================================================
    # 7. TEST REAL SKILLS INTEGRITY (70 SKILLS AKTIF)
    # =========================================================================
    def test_07_real_skills_integrity(self):
        """Menguji integritas seluruh 70 file skill nyata di direktori skills/ (Opsi C)."""
        all_skills = load_all_skills(force_reload=True)
        
        # Total harus 70 skills (3 Orch + 11 Fin + 10 Sales + 10 Mat + 11 HR + 7 Mfg + 9 QA + 9 Log)
        self.assertEqual(len(all_skills), 70, f"Ekspektasi 70 skills, ditemukan {len(all_skills)}: {list(all_skills.keys())}")

        # Pastikan validasi seluruh tools_required (100% dari 70 skills) valid di _TOOL_REGISTRY
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
