import tempfile
import unittest
from pathlib import Path

from src.sentiment_analysis.preprocessing.labels import normalize_rating, sentiment_from_rating
from scripts.audit_datasets import audit_csv


class SentimentRatingLabelTests(unittest.TestCase):
    def test_valid_ratings_are_normalized(self):
        for rating in range(1, 6):
            self.assertEqual(normalize_rating(rating), rating)

    def test_invalid_ratings_remain_unknown(self):
        for rating in (0, 6, -1, None, "", "unknown", "4.5"):
            self.assertIsNone(normalize_rating(rating))

    def test_persian_and_arabic_digits_are_supported(self):
        self.assertEqual(normalize_rating("۵"), 5)
        self.assertEqual(normalize_rating("٤"), 4)

    def test_binary_labels_exclude_neutral_and_invalid_ratings(self):
        self.assertEqual(sentiment_from_rating(1), 0)
        self.assertEqual(sentiment_from_rating(2), 0)
        self.assertIsNone(sentiment_from_rating(3))
        self.assertEqual(sentiment_from_rating(4), 1)
        self.assertEqual(sentiment_from_rating(5), 1)
        self.assertIsNone(sentiment_from_rating(0))
        self.assertIsNone(sentiment_from_rating(None))

    def test_dataset_audit_reports_invalid_ratings_and_label_mismatches(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reviews.csv"
            path.write_text(
                "stars,comment,sentiment\n5,good,1\n5, good  ,1\n3,neutral,0\n0,unknown,0\n",
                encoding="utf-8",
            )
            report = audit_csv(path)

        self.assertEqual(report["rows"], 4)
        self.assertEqual(report["invalid_or_missing_ratings"], 1)
        self.assertEqual(report["neutral_three_star_ratings"], 1)
        self.assertEqual(report["rating_label_mismatches"], 0)
        self.assertEqual(report["normalized_text_duplicates"], 1)


if __name__ == "__main__":
    unittest.main()
