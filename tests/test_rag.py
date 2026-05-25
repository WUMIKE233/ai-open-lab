from pathlib import Path
import unittest

from ai_open_lab.rag import search, tokenize


class RagTests(unittest.TestCase):
    def test_tokenize_normalizes_words(self):
        self.assertEqual(tokenize("Prompt Injection, prompt!"), ["prompt", "injection", "prompt"])

    def test_search_returns_relevant_document(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            (tmp_path / "safety.md").write_text("Prompt injection tries to override instructions.", encoding="utf-8")
            (tmp_path / "cooking.md").write_text("Soup recipes need vegetables and salt.", encoding="utf-8")

            results = search(tmp_path, "prompt injection", top_k=1)

        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].path.endswith("safety.md"))
        self.assertGreater(results[0].score, 0)


if __name__ == "__main__":
    unittest.main()
