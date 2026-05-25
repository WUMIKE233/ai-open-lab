import contextlib
import io
import json
import tempfile
from pathlib import Path
import unittest

from ai_open_lab.cli import main


class CliTests(unittest.TestCase):
    def _write_cases(self, content: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "cases.jsonl"
        path.write_text(content, encoding="utf-8")
        return path

    def test_eval_prompts_defaults_to_json(self):
        cases = self._write_cases(
            '{"id":"ok","response":"Keep secrets private.","expected_keywords":["private"]}\n'
        )
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            exit_code = main(["eval-prompts", str(cases)])

        report = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["total"], 1)
        self.assertEqual(report["passed"], 1)

    def test_eval_prompts_can_render_markdown(self):
        cases = self._write_cases(
            '{"id":"ok","response":"Keep secrets private.","expected_keywords":["private"]}\n'
        )
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            exit_code = main(["eval-prompts", str(cases), "--format", "markdown"])

        self.assertEqual(exit_code, 0)
        self.assertIn("# Prompt Evaluation Report", output.getvalue())
        self.assertIn("Status: passed", output.getvalue())

    def test_eval_prompts_rejects_unknown_format(self):
        cases = self._write_cases(
            '{"id":"ok","response":"Keep secrets private.","expected_keywords":["private"]}\n'
        )

        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                main(["eval-prompts", str(cases), "--format", "html"])

        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
