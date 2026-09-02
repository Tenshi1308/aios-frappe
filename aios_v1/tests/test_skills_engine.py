"""
Unit Test Suite untuk AIOS Skills Engine & Loader (Role-Centric Architecture Opsi C - Tahap 6M.1 s/d 6M.10).
Menguji parser YAML frontmatter, path discovery hierarki <branch>/<role>/, smart caching, resolusi RBAC per role,
serta integritas 78 skills aktif di Orchestrator, Finance, Sales, Material, HR, Manufacturing, Quality, Logistics, dan Maintenance.
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
name: "Failure Mode FMEA and MTBF MTTR"
slug: "failure-mode-fmea-and-mtbf-mttr"
version: "1.0.0"
branch: "maintenance"
role: "reliability_engineer"
tools_required:
  - "calculate_mtbf_mttr"
triggers:
  - "hitung mtbf mttr"
priority: "high"
---

# 1. Peran & Tujuan Bisnis
Menghitung metrik keandalan mesin.
"""
        metadata, body = parse_frontmatter(raw_md)
        self.assertEqual(metadata.get("name"), "Failure Mode FMEA and MTBF MTTR")
        self.assertEqual(metadata.get("slug"), "failure-mode-fmea-and-mtbf-mttr")
        self.assertEqual(metadata.get("role"), "reliability_engineer")
        self.assertEqual(len(metadata.get("tools_required", [])), 1)
        self.assertIn("# 1. Peran & Tujuan Bisnis", body)

    # =========================================================================
    # 2. TEST LOAD SINGLE SKILL FROM FILE DENGAN PATH DISCOVERY
    # =========================================================================
    def test_02_load_skill_from_file_hierarchy(self):
        """Memastikan load_skill_from_file mengekstrak branch dan role dari hierarki direktori."""
        content = """---
name: "Predictive Maintenance"
slug: "predictive-maintenance"
version: "1.0.0"
tools_required:
  - "predict_equipment_failure"
priority: "high"
---
# Content SOP
Prediksi kerusakan mesin.
"""
        file_path = self._create_sample_skill_file("maintenance", "reliability_engineer", "pdm.md", content)
        skill = load_skill_from_file(file_path)

        self.assertIsNotNone(skill)
        self.assertEqual(skill["name"], "Predictive Maintenance")
        self.assertEqual(skill["branch"], "maintenance")
        self.assertEqual(skill["role"], "reliability_engineer")
        self.assertIn("reliability_engineer", skill["roles"])
        self.assertEqual(skill["priority"], "high")
        self.assertIn("predict_equipment_failure", skill["tools_required"])

    # =========================================================================
    # 3. TEST ROLE VARIANT NORMALIZATION
    # =========================================================================
    def test_03_normalize_role_variants(self):
        """Memastikan variasi nama peran (kebab-case, snake_case, space-case) dikenali setara."""
        variants_kebab = _normalize_role_variants("reliability-engineer")
        self.assertIn("reliability-engineer", variants_kebab)
        self.assertIn("reliability_engineer", variants_kebab)
        self.assertIn("reliability engineer", variants_kebab)

    # =========================================================================
    # 4. TEST ROLE-CENTRIC RBAC DISCOVERY (MAINTENANCE & CROSS-BRANCH)
    # =========================================================================
    def test_04_get_skills_for_worker_rbac_option_c(self):
        """Menguji pemisahan hak akses peran mandiri (Role-Centric Maintenance)."""
        # 1. Maintenance Technician (2 skills di maintenance/maintenance_technician/)
        tec_skills = get_skills_for_worker(branch="maintenance", worker_key="maintenance_technician")
        tec_slugs = [s["slug"] for s in tec_skills]
        self.assertEqual(len(tec_slugs), 2)
        self.assertIn("incident-reporting-and-reading-logs", tec_slugs)
        self.assertIn("work-hours-and-parts-consumption", tec_slugs)
        self.assertNotIn("work-order-drafting-and-scheduling", tec_slugs)

        # 2. Maintenance Planner (2 skills di maintenance/maintenance_planner/)
        pln_skills = get_skills_for_worker(branch="maintenance", worker_key="maintenance_planner")
        pln_slugs = [s["slug"] for s in pln_skills]
        self.assertEqual(len(pln_slugs), 2)
        self.assertIn("work-order-drafting-and-scheduling", pln_slugs)
        self.assertIn("backlog-cost-and-equipment-master", pln_slugs)

        # 3. Reliability Engineer (2 skills di maintenance/reliability_engineer/)
        rel_skills = get_skills_for_worker(branch="maintenance", worker_key="reliability_engineer")
        rel_slugs = [s["slug"] for s in rel_skills]
        self.assertEqual(len(rel_slugs), 2)
        self.assertIn("failure-mode-fmea-and-mtbf-mttr", rel_slugs)
        self.assertIn("predictive-maintenance-and-rcm", rel_slugs)

        # 4. Maintenance Manager (8 skills Maintenance + 3 skills Orchestrator = 11 skills)
        mgr_skills = get_skills_for_worker(branch="maintenance", worker_key="manager")
        self.assertEqual(len(mgr_skills), 11)

    # =========================================================================
    # 5. TEST VALIDATE SKILL DEPENDENCIES
    # =========================================================================
    def test_05_validate_skill_dependencies(self):
        """Memastikan validasi dependensi tools_required mencocokkan ke _TOOL_REGISTRY."""
        valid_skill = {
            "name": "Maintenance Test",
            "slug": "test-valid-mnt",
            "tools_required": ["calculate_mtbf_mttr", "schedule_preventive_maintenance"]
        }
        res_valid = validate_skill_dependencies(valid_skill)
        self.assertTrue(res_valid["valid"])
        self.assertEqual(len(res_valid["missing_tools"]), 0)

    # =========================================================================
    # 6. TEST COMPOSE WORKER SYSTEM PROMPT
    # =========================================================================
    def test_06_compose_worker_system_prompt(self):
        """Memastikan perakitan SOP ke dalam prompt berjalan rapi."""
        base_prompt = "Anda adalah Reliability Engineer handal."
        composed = compose_worker_system_prompt(branch="maintenance", worker_key="reliability_engineer", base_prompt=base_prompt)

        self.assertIn("Anda adalah Reliability Engineer handal.", composed)
        self.assertIn("[STANDARD OPERATING PROCEDURES & WORKFLOW SKILLS]", composed)
        self.assertIn("Failure Mode FMEA and MTBF MTTR", composed)
        self.assertIn("Predictive Maintenance and RCM", composed)

    # =========================================================================
    # 7. TEST REAL SKILLS INTEGRITY (78 SKILLS AKTIF)
    # =========================================================================
    def test_07_real_skills_integrity(self):
        """Menguji integritas seluruh 78 file skill nyata di direktori skills/ (Opsi C)."""
        all_skills = load_all_skills(force_reload=True)
        
        # Total harus 78 skills (3 Orch + 11 Fin + 10 Sales + 10 Mat + 11 HR + 7 Mfg + 9 QA + 9 Log + 8 Mnt)
        self.assertEqual(len(all_skills), 78, f"Ekspektasi 78 skills, ditemukan {len(all_skills)}: {list(all_skills.keys())}")

        # Pastikan validasi seluruh tools_required (100% dari 78 skills) valid di _TOOL_REGISTRY
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
