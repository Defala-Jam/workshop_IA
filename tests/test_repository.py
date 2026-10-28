import unittest
from pathlib import Path
from science_tutor.repository import KnowledgeBase

ROOT = Path(__file__).resolve().parents[1]

class RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = KnowledgeBase(ROOT / "data" / "knowledge_base.json")

    def test_topic_count(self):
        self.assertEqual(len(self.kb.list_topics()), 6)

    def test_each_topic_has_six_questions(self):
        for topic in self.kb.data["topics"]:
            self.assertEqual(len(topic["questions"]), 6, topic["id"])

    def test_get_question_hides_answer(self):
        q = self.kb.get_question("ce_004")
        self.assertNotIn("answer", q)
        self.assertEqual(q["id"], "ce_004")

    def test_check_answer(self):
        self.assertTrue(self.kb.check_answer("fm_004", "a")["correct"])
        self.assertFalse(self.kb.check_answer("fm_004", "b")["correct"])

if __name__ == "__main__": unittest.main()
