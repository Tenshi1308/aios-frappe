"""
Unit Test Suite untuk AIOS Skills Engine & Loader (Role-Centric Architecture Opsi C - Tahap 6M.1 s/d 6M.7).
Menguji parser YAML frontmatter, path discovery hierarki <branch>/<role>/, smart caching, resolusi RBAC per role,
serta integritas 52 skills aktif di Orchestrator, Finance, Sales, Material, HR, dan Manufacturing.
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
name: "MRP and BOM Explosion"
slug: "mrp-and-bom-explosion"
version: "1.0.0"
branch: "manufacturing"
role: "production_planner"
tools_required:
  - "explode_bill_of_materials"
triggers:
  - "mrp explosion"
priority: "critical"
---

# 1. Peran & Tujuan Bisnis
Mengatur penguraian struktur komponen BOM.
"""
        metadata, body = parse_frontmatter(raw_md)
        self.assertEqual(metadata.get("name"), "MRP and BOM Explosion")
        self.assertEqual(metadata.get("slug"), "mrp-and-bom-explosion")
        self.assertEqual(metadata.get("role"), "production_planner")
        self.assertEqual(len(metadata.get("tools_required", [])), 1)
        self.assertIn("# 1. Peran & Tujuan Bisnis", body)

    # =========================================================================
    # 2. TEST LOAD SINGLE SKILL FROM FILE DENGAN PATH DISCOVERY
    # =========================================================================
    def test_02_load_skill_from_file_hierarchy(self):
        """Memastikan load_skill_from_file mengekstrak branch dan role dari hierarki direktori."""
        content = """---
name: "Work Center Capacity"
slug: "work-center-capacity"
version: "1.0.0"
tools_required:
  - "check_work_center_capacity"
priority: "high"
---
# Content SOP
Evaluasi beban mesin.
"""
        file_path = self._create_sample_skill_file("manufacturing", "production_scheduler", "capacity.md", content)
        skill = load_skill_from_file(file_path)

        self.assertIsNotNone(skill)
        self.assertEqual(skill["name"], "Work Center Capacity")
        self.assertEqual(skill["branch"], "manufacturing")
        self.assertEqual(skill["role"], "production_scheduler")
        self.assertIn("production_scheduler", skill["roles"])
        self.assertEqual(skill["priority"], "high")
        self.assertIn("check_work_center_capacity", skill["tools_required"])

    # =========================================================================
    # 3. TEST ROLE VARIANT NORMALIZATION
    # =========================================================================
    def test_03_normalize_role_variants(self):
        """Memastikan variasi nama peran (kebab-case, snake_case, space-case) dikenali setara."""
        variants_kebab = _normalize_role_variants("production-supervisor")
        self.assertIn("production-supervisor", variants_kebab)
        self.assertIn("production_supervisor", variants_kebab)
        self.assertIn("production supervisor", variants_kebab)

    # =========================================================================
    # 4. TEST ROLE-CENTRIC RBAC DISCOVERY (MANUFACTURING & CROSS-BRANCH)
    # =========================================================================
    def test_04_get_skills_for_worker_rbac_option_c(self):
        """Menguji pemisahan hak akses peran mandiri (Role-Centric Manufacturing)."""
        # 1. Production Planner (2 skills di manufacturing/production_planner/)
        pln_skills = get_skills_for_worker(branch="manufacturing", worker_key="production_planner")
        pln_slugs = [s["slug"] for s in pln_skills]
        self.assertEqual(len(pln_slugs), 2)
        self.assertIn("mrp-and-bom-explosion", pln_slugs)
        self.assertIn("production-cost-and-takt-time", pln_slugs)
        self.assertNotIn("machine-oee-and-downtime-incident", pln_slugs)

        # 2. Production Scheduler (2 skills di manufacturing/production_scheduler/)
        sch_skills = get_skills_for_worker(branch="manufacturing", worker_key="production_scheduler")
        sch_slugs = [s["slug"] for s in sch_skills]
        self.assertEqual(len(sch_slugs), 2)
        self.assertIn("work-center-capacity-and-routing", sch_slugs)
        self.assertIn("manufacturing-order-scheduling", sch_slugs)

        # 3. Production Supervisor (2 skills di manufacturing/production_supervisor/)
        spv_skills = get_skills_for_worker(branch="manufacturing", worker_key="production_supervisor")
        spv_slugs = [s["slug"] for s in spv_skills]
        self.assertEqual(len(spv_slugs), 2)
        self.assertIn("shop-floor-output-and-scrap-logging", spv_slugs)
        self.assertIn("machine-oee-and-downtime-incident", spv_slugs)

        # 4. Production Manager (7 skills Manufacturing + 3 skills Orchestrator = 10 skills)
        mgr_skills = get_skills_for_worker(branch="manufacturing", worker_key="manager")
        self.assertEqual(len(mgr_skills), 10)

    # =========================================================================
    # 5. TEST VALIDATE SKILL DEPENDENCIES
    # =========================================================================
    def test_05_validate_skill_dependencies(self):
        """Memastikan validasi dependensi tools_required mencocokkan ke _TOOL_REGISTRY."""
        valid_skill = {
            "name": "Mfg Test",
            "slug": "test-valid-mfg",
            "tools_required": ["analyze_oee_metrics", "confirm_production_output"]
        }
        res_valid = validate_skill_dependencies(valid_skill)
        self.assertTrue(res_valid["valid"])
        self.assertEqual(len(res_valid["missing_tools"]), 0)

    # =========================================================================
    # 6. TEST COMPOSE WORKER SYSTEM PROMPT
    # =========================================================================
    def test_06_compose_worker_system_prompt(self):
        """Memastikan perakitan SOP ke dalam prompt berjalan rapi."""
        base_prompt = "Anda adalah Production Supervisor pabrik."
        composed = compose_worker_system_prompt(branch="manufacturing", worker_key="production_supervisor", base_prompt=base_prompt)

        self.assertIn("Anda adalah Production Supervisor pabrik.", composed)
        self.assertIn("[STANDARD OPERATING PROCEDURES & WORKFLOW SKILLS]", composed)
        self.assertIn("Machine OEE and Downtime Incident", composed)
        self.assertIn("Shop Floor Output and Scrap Logging", composed)

    # =========================================================================
    # 7. TEST REAL SKILLS INTEGRITY (52 SKILLS AKTIF)
    # =========================================================================
    def test_07_real_skills_integrity(self):
        """Menguji integritas seluruh 52 file skill nyata di direktori skills/ (Opsi C)."""
        all_skills = load_all_skills(force_reload=True)
        
        # Total harus 52 skills (3 Orch + 11 Fin + 10 Sales + 10 Mat + 11 HR + 7 Mfg)
        self.assertEqual(len(all_skills), 52, f"Ekspektasi 52 skills, ditemukan {len(all_skills)}: {list(all_skills.keys())}")

        # Pastikan validasi seluruh tools_required (100% dari 52 skills) valid di _TOOL_REGISTRY
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
