"""Offline checks for the requirements-based risk register prototype."""

from datetime import date
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
import risk_register as rr


AS_OF = date(2026, 11, 10)


class RiskRegisterTests(unittest.TestCase):
    def setUp(self):
        self.items = json.loads((PROJECT / "examples/synthetic_risks.json").read_text(encoding="utf-8"))

    def test_three_workbook_seed_scores_and_ratings(self):
        # Numeric inputs are copied from three synthetic workbook examples.
        # The workbook uses two-digit IDs; the prototype uses three digits.
        expected = [(20, "High", 10, "Medium"), (16, "High", 6, "Low"), (8, "Medium", 4, "Low")]
        for row, want in zip(rr.assess_register(self.items[:3], AS_OF)["risks"], expected):
            self.assertEqual((row["inherent"]["value"], row["inherent"]["rating"],
                              row["residual"]["value"], row["residual"]["rating"]), want)

    def test_all_25_factor_pairs_have_expected_bands(self):
        expected = ["LLLLL", "LLLMM", "LLMMH", "LMMHH", "LMHHH"]
        legend = {"L": ("Low", "green", 180), "M": ("Medium", "amber", 90), "H": ("High", "red", 30)}
        for likelihood, bands in enumerate(expected, 1):
            for impact, band in enumerate(bands, 1):
                with self.subTest(likelihood=likelihood, impact=impact):
                    result = rr.score(likelihood, impact)
                    self.assertEqual((result["rating"], result["color"], result["review_days"]), legend[band])

    def test_workbook_fixed_medium_label_does_not_override_low_cadence(self):
        row = rr.assess_risk(self.items[6], AS_OF)
        self.assertEqual((6, "Low", "2027-04-18"), (
            row["inherent"]["value"], row["inherent"]["rating"], row["review_date"],
        ))

    def test_invalid_factors_are_rejected(self):
        for invalid in (0, 6, -1, True, 4.0, "4", None):
            with self.subTest(value=invalid), self.assertRaisesRegex(ValueError, "integers from 1 to 5"):
                rr.assess_register([{**self.items[0], "likelihood": invalid}], AS_OF)

    def test_entered_scores_cannot_override_calculation(self):
        with self.assertRaisesRegex(ValueError, "documented input fields"):
            rr.assess_register([{**self.items[0], "score": 1}], AS_OF)

    def test_residual_score_cannot_exceed_inherent(self):
        with self.assertRaisesRegex(ValueError, "Residual score cannot exceed"):
            rr.assess_register([{**self.items[0], "residual_likelihood": 5}], AS_OF)

    def test_high_residual_flags_required_acceptance(self):
        report = rr.assess_register(self.items, AS_OF)
        self.assertEqual(["R-006"], report["acceptance_required_ids"])

    def test_duplicate_risk_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate risk ID"):
            rr.assess_register([self.items[0], self.items[0]], AS_OF)

    def test_duplicate_json_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate JSON fields"):
            json.loads('{"likelihood":1,"likelihood":5}', object_pairs_hook=rr.unique_fields)

    def test_invalid_id_category_and_unspecific_mitigation(self):
        for changes, message in (({"risk_id": "R-01"}, "Risk IDs"),
                                 ({"category": "Other"}, "Category"),
                                 ({"mitigation": "Monitor."}, "specific action"),
                                 ({"owner_role": " "}, "non-empty text")):
            with self.subTest(field=changes), self.assertRaisesRegex(ValueError, message):
                rr.assess_register([{**self.items[0], **changes}], AS_OF)

    def test_empty_register_does_not_produce_a_clean_report(self):
        with self.assertRaisesRegex(ValueError, "at least one risk"):
            rr.assess_register([], AS_OF)

    def test_team_style_owners_are_rejected(self):
        for owner in ("Security Team", "security TEAM.", "Security Teams", "IT Department",
                      "Operations Group", "Risk Committee", "  security-team  "):
            with self.subTest(owner=owner), self.assertRaisesRegex(ValueError, "not a team"):
                rr.assess_register([{**self.items[0], "owner_role": owner}], AS_OF)

    def test_accountable_role_titles_are_preserved(self):
        for owner in ("ISSM", "ISSE", "ISSO", "Business Owner", "Team Lead"):
            with self.subTest(owner=owner):
                risk = rr.assess_register([{**self.items[0], "owner_role": f" {owner} "}], AS_OF)["risks"][0]
                self.assertEqual(owner, risk["owner_role"])

    def test_review_due_starts_on_the_review_date(self):
        first = self.items[0]
        before = rr.assess_register([first], date(2026, 11, 9))
        on_date = rr.assess_register([first], AS_OF)
        self.assertEqual("2026-11-10", on_date["risks"][0]["review_date"])
        self.assertEqual([], before["review_due_ids"])
        self.assertEqual(["R-001"], on_date["review_due_ids"])

    def test_invalid_or_future_assessment_dates_are_rejected(self):
        for invalid in ("2026-02-30", "20261110", "2026-11-11"):
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                rr.assess_register([{**self.items[0], "assessed_on": invalid}], AS_OF)

    def test_heatmap_places_all_risks_in_25_cells(self):
        report = rr.assess_register(self.items, AS_OF)
        cells = {(cell["likelihood"], cell["impact"]): cell["risk_ids"] for cell in report["heatmap"]}
        self.assertEqual(25, len(cells))
        self.assertEqual(["R-001"], cells[4, 5])
        self.assertEqual(["R-002", "R-010"], cells[4, 4])
        self.assertEqual(["R-003"], cells[2, 4])
        self.assertCountEqual([r["risk_id"] for r in self.items], [i for ids in cells.values() for i in ids])
        self.assertEqual(12, len(report["risks"]))
        self.assertEqual({"Security", "Vendor", "Business"}, {r["category"] for r in report["risks"]})

    def test_top_five_has_stable_order_when_inputs_are_reversed(self):
        report = rr.assess_register(list(reversed(self.items)), AS_OF)
        self.assertEqual(["R-006", "R-001", "R-002", "R-010", "R-004"],
                         [r["risk_id"] for r in report["top_five"]])
        self.assertEqual(rr.assess_register(self.items, AS_OF), report)

    def test_report_escapes_input_text_and_labels_simulation(self):
        item = {**self.items[0], "description": "<script>example</script>"}
        page = rr.render_html(rr.assess_register([item], AS_OF))
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;example&lt;/script&gt;", page)
        self.assertIn("Risk Register simulation", page)
        self.assertIn('scope="col"', page)


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory(prefix="risk07-cli-")
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)
        self.input = self.directory / "synthetic.json"
        self.input.write_bytes((PROJECT / "examples/synthetic_risks.json").read_bytes())

    def invoke(self, *arguments):
        stdout, stderr = StringIO(), StringIO()
        status = 0
        with patch.object(sys, "argv", ["risk_register.py", *map(str, arguments)]), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                rr.main()
            except SystemExit as error:
                status = error.code
        return status, stdout.getvalue(), stderr.getvalue()

    def assert_error(self, arguments, message):
        status, stdout, stderr = self.invoke(*arguments)
        self.assertEqual(2, status)
        self.assertEqual("", stdout)
        self.assertIn(message, stderr)
        self.assertNotIn("Traceback", stderr)

    def test_json_and_html_reports_exit_successfully(self):
        status, stdout, stderr = self.invoke(self.input, "--as-of", AS_OF.isoformat())
        self.assertEqual((0, ""), (status, stderr))
        report = json.loads(stdout)
        self.assertEqual("offline_simulation", report["mode"])
        self.assertEqual(12, len(report["risks"]))
        status, stdout, stderr = self.invoke(self.input, "--as-of", AS_OF.isoformat(), "--format", "html")
        self.assertEqual((0, ""), (status, stderr))
        self.assertIn("Risk Register simulation", stdout)

    def test_empty_input_is_an_error_in_both_formats(self):
        self.input.write_text("[]", encoding="utf-8")
        for output in ("json", "html"):
            with self.subTest(output=output):
                self.assert_error([self.input, "--as-of", AS_OF.isoformat(), "--format", output],
                                  "at least one risk")

    def test_private_evidence_is_rejected_without_reading(self):
        private_path = self.directory / "private-evidence" / "synthetic.json"
        # No evidence directory or file is created, opened or read.
        for resolved_path in (private_path, self.input):
            with self.subTest(resolved_path=resolved_path), \
                    patch.object(rr.Path, "resolve", return_value=resolved_path), \
                    patch.object(rr.Path, "open") as open_input:
                self.assert_error([private_path, "--as-of", AS_OF.isoformat()], "outside private evidence")
                open_input.assert_not_called()

    def test_symlink_into_private_evidence_is_rejected_without_reading(self):
        link = self.directory / "linked.json"
        link.symlink_to(self.directory / "private-evidence" / "synthetic.json")
        with patch.object(rr.Path, "open") as open_input:
            self.assert_error([link, "--as-of", AS_OF.isoformat()], "outside private evidence")
            open_input.assert_not_called()

    def test_missing_directory_and_wrong_extension_are_errors(self):
        wrong_extension = self.directory / "synthetic.txt"
        wrong_extension.write_text("[]", encoding="utf-8")
        for path in (self.directory / "missing.json", self.directory, wrong_extension):
            with self.subTest(path=path):
                self.assert_error([path, "--as-of", AS_OF.isoformat()], "existing synthetic JSON file")

    def test_malformed_json_and_invalid_register_are_errors(self):
        for content, message in (("{", "Expecting property name"),
                                 ('{"same":1,"same":2}', "Duplicate JSON fields"),
                                 ("{}", "JSON array"),
                                 ("[{}]", "documented input fields")):
            with self.subTest(content=content):
                self.input.write_text(content, encoding="utf-8")
                self.assert_error([self.input, "--as-of", AS_OF.isoformat()], message)

    def test_unreadable_or_non_utf8_input_has_a_clear_error(self):
        with patch.object(rr.Path, "open", side_effect=PermissionError("synthetic failure")):
            self.assert_error([self.input, "--as-of", AS_OF.isoformat()], "Unable to read")
        self.input.write_bytes(b"\xff")
        self.assert_error([self.input, "--as-of", AS_OF.isoformat()], "Unable to read")

    def test_bad_or_pre_assessment_report_dates_are_errors(self):
        for value, message in (("20261110", "YYYY-MM-DD"), ("2026-02-30", "valid calendar"),
                               ("2020-01-01", "after the report date")):
            with self.subTest(value=value):
                self.assert_error([self.input, "--as-of", value], message)

    def test_missing_date_and_unknown_format_are_usage_errors(self):
        self.assert_error([self.input], "--as-of")
        self.assert_error([self.input, "--as-of", AS_OF.isoformat(), "--format", "csv"], "invalid choice")


if __name__ == "__main__":
    unittest.main()
