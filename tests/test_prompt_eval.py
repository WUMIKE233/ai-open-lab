import unittest

from ai_open_lab.prompt_eval import (
    PromptCase,
    evaluate_case,
    evaluate_cases,
    render_markdown_report,
)


class PromptEvalTests(unittest.TestCase):
    def test_evaluate_case_passes_when_checks_match(self):
        result = evaluate_case(
            PromptCase(
                case_id="ok",
                prompt="Summarize policy",
                response="Keep secrets private.",
                expected_keywords=("secrets", "private"),
                forbidden_keywords=("password",),
            )
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.score, 1.0)

    def test_evaluate_case_reports_failures(self):
        result = evaluate_case(
            PromptCase(
                case_id="bad",
                prompt="Summarize policy",
                response="The password can be shared.",
                expected_keywords=("private",),
                forbidden_keywords=("password",),
            )
        )

        self.assertFalse(result.passed)
        self.assertEqual(result.missing_keywords, ("private",))
        self.assertEqual(result.forbidden_hits, ("password",))

    def test_evaluate_cases_summarizes_results(self):
        report = evaluate_cases(
            [
                PromptCase("one", "", "alpha", expected_keywords=("alpha",)),
                PromptCase("two", "", "beta", expected_keywords=("alpha",)),
            ]
        )

        self.assertEqual(report["total"], 2)
        self.assertEqual(report["passed"], 1)
        self.assertEqual(report["failed"], 1)

    def test_render_markdown_report_includes_summary(self):
        report = evaluate_cases(
            [
                PromptCase("ok", "", "alpha", expected_keywords=("alpha",)),
            ]
        )

        markdown = render_markdown_report(report)

        self.assertIn("# Prompt Evaluation Report", markdown)
        self.assertIn("Total: 1", markdown)
        self.assertIn("Passed: 1", markdown)
        self.assertIn("Failed: 0", markdown)
        self.assertIn("Average Score: 1.0", markdown)
        self.assertIn("### ok", markdown)
        self.assertIn("Status: passed", markdown)
        self.assertIn("Missing keywords: none", markdown)
        self.assertIn("Forbidden hits: none", markdown)
        self.assertIn("Missing regex: none", markdown)

    def test_render_markdown_report_lists_failures(self):
        report = evaluate_cases(
            [
                PromptCase(
                    "bad",
                    "",
                    "The password is shared.",
                    expected_keywords=("private",),
                    forbidden_keywords=("password",),
                    expected_regex=(r"rotated",),
                ),
            ]
        )

        markdown = render_markdown_report(report)

        self.assertIn("Status: failed", markdown)
        self.assertIn("Missing keywords: private", markdown)
        self.assertIn("Forbidden hits: password", markdown)
        self.assertIn("Missing regex: rotated", markdown)


if __name__ == "__main__":
    unittest.main()
