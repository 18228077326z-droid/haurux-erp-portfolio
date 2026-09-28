from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_URL = "https://18228077326z-droid.github.io/haurux-erp-portfolio/"


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"Required file is missing: {relative_path}")
    return path.read_text(encoding="utf-8")


class GitHubPresenceContractTests(unittest.TestCase):
    def test_public_source_manifest_is_exact_and_resolvable(self):
        manifest = read(".github/public-files.txt").splitlines()
        expected = sorted((
            ".github/public-files.txt",
            ".gitignore",
            ".nojekyll",
            "CASE_STUDY.md",
            "LICENSE.md",
            "README.md",
            "app.toml",
            "assets/HAURUX_ERP_UIUX_Portfolio.pdf",
            "assets/avatar.png",
            "assets/favicon.png",
            "assets/social-preview.png",
            "docs/images/accounting.png",
            "docs/images/dashboard.png",
            "docs/images/inventory.png",
            "docs/images/mobile-accounting.png",
            "docs/images/portfolio-cover.png",
            "docs/images/procurement.png",
            "docs/images/role-permissions.png",
            "docs/images/sales.png",
            "index.html",
            "portfolio-print.html",
            "tests/test_github_presence_contract.py",
            "tests/test_portfolio_contract.py",
        ))
        self.assertEqual(manifest, expected)
        for relative_path in manifest:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_repository_readme_is_an_english_case_study_landing_page(self):
        readme = read("README.md")
        for phrase in (
            "HAURUX TECH STUDIO",
            "ERP UI/UX Concept Portfolio",
            "Live Demo",
            "Download PDF",
            "Read the Case Study",
            "37-screen",
            "User & Role",
            "Concept / Demo",
            PUBLIC_URL,
            "status-concept%20%2F%20demo",
            "scope-37%20screens",
            "delivery-responsive%20web",
        ):
            self.assertIn(phrase, readme)
        self.assertIsNone(re.search(r"[\u3400-\u9fff]", readme))

    def test_detailed_english_case_study_documents_decisions_and_limits(self):
        case_study = read("CASE_STUDY.md")
        for heading in (
            "## Context",
            "## Constraints and Assumptions",
            "## Information Architecture",
            "## Key Workflows",
            "## Design Decisions",
            "## Responsive and Accessible by Design",
            "## Validation",
            "## From Concept to Production",
            "## Integrity Statement",
        ):
            self.assertIn(heading, case_study)
        self.assertIn("synthetic data", case_study)
        self.assertIn("37", case_study)
        self.assertIsNone(re.search(r"[\u3400-\u9fff]", case_study))

    def test_code_and_portfolio_assets_have_separate_rights(self):
        license_text = read("LICENSE.md")
        self.assertIn("MIT License", license_text)
        self.assertIn("Portfolio Assets", license_text)
        self.assertIn("All Rights Reserved", license_text)
        for asset_type in ("portrait", "screenshots", "PDF", "case-study content"):
            self.assertIn(asset_type, license_text)

    def test_real_erp_screenshots_are_present(self):
        expected = (
            "portfolio-cover.png",
            "dashboard.png",
            "role-permissions.png",
            "procurement.png",
            "inventory.png",
            "sales.png",
            "accounting.png",
            "mobile-accounting.png",
        )
        image_dir = ROOT / "docs" / "images"
        for name in expected:
            image = image_dir / name
            self.assertTrue(image.is_file(), name)
            self.assertGreater(image.stat().st_size, 20_000, name)

        social_preview = ROOT / "assets" / "social-preview.png"
        self.assertTrue(social_preview.is_file())
        self.assertGreater(social_preview.stat().st_size, 20_000)

    def test_live_page_has_complete_share_metadata(self):
        html = read("index.html")
        for snippet in (
            f'<link rel="canonical" href="{PUBLIC_URL}"',
            '<meta property="og:type" content="website"',
            '<meta property="og:title"',
            '<meta property="og:description"',
            f'<meta property="og:image" content="{PUBLIC_URL}assets/social-preview.png"',
            '<meta name="twitter:card" content="summary_large_image"',
            f'content="{PUBLIC_URL}assets/social-preview.png"',
            '<link rel="icon" type="image/png" href="assets/favicon.png"',
        ):
            self.assertIn(snippet, html)
        favicon = ROOT / "assets" / "favicon.png"
        self.assertTrue(favicon.is_file())
        self.assertGreater(favicon.stat().st_size, 1_000)

    def test_live_screen_inventory_matches_the_case_study(self):
        html = read("index.html")
        for snippet in (
            "Foundation & navigation <span>5 screens</span>",
            "User & access <span>5 screens</span>",
            "Sales <span>8 screens</span>",
            "PR / PO <span>8 screens</span>",
            "IMS / Inventory <span>6 screens</span>",
            "Accounting <span>5 screens</span>",
        ):
            self.assertIn(snippet, html)

    def test_live_site_uses_a_generic_project_contact_section(self):
        html = read("index.html")
        for phrase in (
            "Start with one clear workflow.",
            "Current product",
            "Roles and rules",
            "First milestone",
            "Discuss your ERP",
        ):
            self.assertIn(phrase, html)
        self.assertNotIn('id="copyBid"', html)
        self.assertNotIn('id="bidText"', html)

    def test_live_site_has_consistent_english_positioning(self):
        html = read("index.html")
        for phrase in (
            '<html lang="en">',
            "Complex ERP,",
            "Explore the case study",
            "Complex operations should not feel complex on screen.",
            "A prototype you can test, not just view.",
            "Every screen earns its place.",
            "Evidence, not claims",
            "A system built to scale.",
        ):
            self.assertIn(phrase, html)

    def test_live_site_keeps_concept_claims_verifiable(self):
        html = read("index.html")
        self.assertIn("Concept / Demo · Synthetic data", html)
        self.assertIn("Interactive web prototype", html)
        self.assertIn("Concept pattern · Exception management", html)
        self.assertNotIn("Figma-ready", html)
        self.assertNotIn("Flood and dam inspection system", html)

    def test_dashboard_date_and_demo_action_are_not_misleading(self):
        html = read("index.html")
        self.assertIn("Sunday, 27 Sep 2026", html)
        self.assertNotIn("Tuesday, 27 Sep", html)
        self.assertIn('id="protoActionStatus"', html)
        self.assertIn("does not submit or export production data", html)
        self.assertIn("protoAction.addEventListener('click'", html)

    def test_branch_pages_publish_set_is_complete(self):
        self.assertTrue((ROOT / ".nojekyll").is_file())
        for public_asset in (
            "index.html",
            "portfolio-print.html",
            "assets/HAURUX_ERP_UIUX_Portfolio.pdf",
            "assets/avatar.png",
            "assets/favicon.png",
            "assets/social-preview.png",
            "docs/images/dashboard.png",
            "docs/images/role-permissions.png",
        ):
            self.assertTrue((ROOT / public_asset).is_file(), public_asset)

    def test_live_site_uses_only_relevant_erp_proof_images(self):
        html = read("index.html")
        self.assertIn('src="docs/images/dashboard.png"', html)
        self.assertIn('src="docs/images/role-permissions.png"', html)
        self.assertNotIn("lead-automation.png", html)
        self.assertNotIn("research-brief.png", html)

    def test_print_portfolio_is_an_english_reusable_concept(self):
        printable = read("portfolio-print.html")
        self.assertIn('<html lang="en">', printable)
        self.assertIn("Complex ERP", printable)
        self.assertIn("Self-initiated concept study", printable)
        self.assertIn("Portfolio integrity statement", printable)

    def test_new_public_copy_has_no_em_or_en_dashes(self):
        copy_paths = (
            "README.md",
            "CASE_STUDY.md",
            "LICENSE.md",
            "portfolio-print.html",
        )
        for path in copy_paths:
            content = read(path)
            self.assertNotRegex(content, r"[—–]", path)


if __name__ == "__main__":
    unittest.main()
