"""
Unit Test Suite untuk AIOS Skills Engine & Loader (Role-Centric Architecture Opsi C - Tahap 6M.1 s/d 6M.6).
Menguji parser YAML frontmatter, path discovery hierarki <branch>/<role>/, smart caching, resolusi RBAC per role,
serta integritas 45 skills aktif di Orchestrator, Finance, Sales, Material, dan HR.
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
name: "Job Requisition and Posting"
slug: "job-requisition-and-posting"
version: "1.0.0"
branch: "hr"
role: "recruiter"
tools_required:
  - "post_job_vacancy"
triggers:
  - "buka lowongan"
priority: "high"
---

# 1. Peran & Tujuan Bisnis
Mengatur pembukaan lowongan pekerjaan.
"""
        metadata, body = parse_frontmatter(raw_md)
        self.assertEqual(metadata.get("name"), "Job Requisition and Posting")
        self.assertEqual(metadata.get("slug"), "job-requisition-and-posting")
        self.assertEqual(metadata.get("role"), "recruiter")
        self.assertEqual(len(metadata.get("tools_required", [])), 1)
        self.assertIn("# 1. Peran & Tujuan Bisnis", body)

    # =========================================================================
    # 2. TEST LOAD SINGLE SKILL FROM FILE DENGAN PATH DISCOVERY
    # =========================================================================
    def test_02_load_skill_from_file_hierarchy(self):
        """Memastikan load_skill_from_file mengekstrak branch dan role dari hierarki direktori."""
        content = """---
name: "Batch Payroll"
slug: "batch-payroll"
version: "1.0.0"
tools_required:
  - "calculate_payroll_batch"
priority: "critical"
---
# Content SOP
Hitung gaji bulanan.
"""
        file_path = self._create_sample_skill_file("hr", "payroll_officer", "payroll.md", content)
        skill = load_skill_from_file(file_path)

        self.assertIsNotNone(skill)
        self.assertEqual(skill["name"], "Batch Payroll")
        self.assertEqual(skill["branch"], "hr")
        self.assertEqual(skill["role"], "payroll_officer")
        self.assertIn("payroll_officer", skill["roles"])
        self.assertEqual(skill["priority"], "critical")
        self.assertIn("calculate_payroll_batch", skill["tools_required"])

    # =========================================================================
    # 3. TEST ROLE VARIANT NORMALIZATION
    # =========================================================================
    def test_03_normalize_role_variants(self):
        """Memastikan variasi nama peran (kebab-case, snake_case, space-case) dikenali setara."""
        variants_kebab = _normalize_role_variants("payroll-officer")
        self.assertIn("payroll-officer", variants_kebab)
        self.assertIn("payroll_officer", variants_kebab)
        self.assertIn("payroll officer", variants_kebab)

    # =========================================================================
    # 4. TEST ROLE-CENTRIC RBAC DISCOVERY (HR & CROSS-BRANCH)
    # =========================================================================
    def test_04_get_skills_for_worker_rbac_option_c(self):
        """Menguji pemisahan hak akses peran mandiri (Role-Centric)."""
        # 1. Recruiter (2 skills di hr/recruiter/)
        rec_skills = get_skills_for_worker(branch="hr", worker_key="recruiter")
        rec_slugs = [s["slug"] for s in rec_skills]
        self.assertEqual(len(rec_slugs), 2)
        self.assertIn("job-requisition-and-posting", rec_slugs)
        self.assertIn("applicant-screening-and-ranking", rec_slugs)
        self.assertNotIn("batch-payroll-processing", rec_slugs)

        # 2. Payroll Officer (3 skills di hr/payroll_officer/)
        pay_skills = get_skills_for_worker(branch="hr", worker_key="payroll_officer")
        pay_slugs = [s["slug"] for s in pay_skills]
        self.assertEqual(len(pay_slugs), 3)
        self.assertIn("batch-payroll-processing", pay_slugs)
        self.assertIn("overtime-and-bpjs-statutory-deductions", pay_slugs)
        self.assertIn("severance-and-termination-compensation", pay_slugs)

        # 3. HR Staff (3 skills di hr/hr_staff/)
        hrs_skills = get_skills_for_worker(branch="hr", worker_key="hr_staff")
        hrs_slugs = [s["slug"] for s in hrs_skills]
        self.assertEqual(len(hrs_slugs), 3)
        self.assertIn("employee-master-onboarding", hrs_slugs)
        self.assertIn("attendance-and-leave-administration", hrs_slugs)
        self.assertIn("employee-benefits-and-claims", hrs_slugs)

        # 4. Training Specialist (1 skill)
        trn_skills = get_skills_for_worker(branch="hr", worker_key="training_specialist")
        trn_slugs = [s["slug"] for s in trn_skills]
        self.assertEqual(len(trn_slugs), 1)
        self.assertIn("employee-training-program-lifecycle", trn_slugs)

        # 5. HR Manager (11 skills HR + 3 skills Orchestrator = 14 skills)
        mgr_skills = get_skills_for_worker(branch="hr", worker_key="manager")
        self.assertEqual(len(mgr_skills), 14)

    # =========================================================================
    # 5. TEST VALIDATE SKILL DEPENDENCIES
    # =========================================================================
    def test_05_validate_skill_dependencies(self):
        """Memastikan validasi dependensi tools_required mencocokkan ke _TOOL_REGISTRY."""
        valid_skill = {
            "name": "HR Test",
            "slug": "test-valid",
            "tools_required": ["post_job_vacancy", "screen_applicant_profile"]
        }
        res_valid = validate_skill_dependencies(valid_skill)
        self.assertTrue(res_valid["valid"])
        self.assertEqual(len(res_valid["missing_tools"]), 0)

    # =========================================================================
    # 6. TEST COMPOSE WORKER SYSTEM PROMPT
    # =========================================================================
    def test_06_compose_worker_system_prompt(self):
        """Memastikan perakitan SOP ke dalam prompt berjalan rapi."""
        base_prompt = "Anda adalah Recruiter profesional."
        composed = compose_worker_system_prompt(branch="hr", worker_key="recruiter", base_prompt=base_prompt)

        self.assertIn("Anda adalah Recruiter profesional.", composed)
        self.assertIn("[STANDARD OPERATING PROCEDURES & WORKFLOW SKILLS]", composed)
        self.assertIn("Job Requisition and Posting", composed)
        self.assertIn("Applicant Screening and Ranking", composed)

    # =========================================================================
    # 7. TEST REAL SKILLS INTEGRITY (45 SKILLS: ORCHESTRATOR, FINANCE, SALES, MATERIAL, HR)
    # =========================================================================
    def test_07_real_skills_integrity(self):
        """Menguji integritas seluruh 45 file skill nyata di direktori skills/ (Opsi C)."""
        all_skills = load_all_skills(force_reload=True)
        
        # Total harus 45 skills (3 Orchestrator + 11 Finance + 10 Sales + 10 Material + 11 HR)
        self.assertEqual(len(all_skills), 45, f"Ekspektasi 45 skills, ditemukan {len(all_skills)}: {list(all_skills.keys())}")

        # Pastikan validasi seluruh tools_required (100% dari 45 skills) valid di _TOOL_REGISTRY
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
