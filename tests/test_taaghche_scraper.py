import unittest

from src.sentiment_analysis.scraping.taaghche import _stable_id


class TaaghcheReviewIdentityTests(unittest.TestCase):
    def test_identity_is_deterministic(self):
        self.assertEqual(
            _stable_id("reader", "1404/01/01", 4, "great book"),
            _stable_id("reader", "1404/01/01", 4, "great book"),
        )

    def test_identity_distinguishes_content(self):
        self.assertNotEqual(
            _stable_id("reader", "1404/01/01", 4, "great book"),
            _stable_id("reader", "1404/01/01", 3, "great book"),
        )


if __name__ == "__main__":
    unittest.main()
