import unittest

from ai_open_lab.prompt_eval import PromptCase, evaluate_case, evaluate_cases


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


if __name__ == "__main__":
    unittest.main()
