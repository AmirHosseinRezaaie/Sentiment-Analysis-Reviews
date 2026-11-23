import unittest

from src.sentiment_analysis.scraping.basalam import _review_id, parse_review_cards


class FakeElement:
    def __init__(self, text="", elements=None):
        self.text = text
        self.elements = elements or {}

    def find_elements(self, by, selector):
        return self.elements.get(selector, [])


class FakeSection(FakeElement):
    pass


class BasalamReviewIdentityTests(unittest.TestCase):
    def test_review_id_is_stable_across_processes(self):
        first = _review_id("کاربر", "۱۴۰۴/۰۱/۰۱", 5, "نظر نمونه")
        second = _review_id("کاربر", "۱۴۰۴/۰۱/۰۱", 5, "نظر نمونه")
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_review_id_changes_when_review_content_changes(self):
        first = _review_id("کاربر", "۱۴۰۴/۰۱/۰۱", 5, "نظر نمونه")
        second = _review_id("کاربر", "۱۴۰۴/۰۱/۰۱", 4, "نظر نمونه")
        self.assertNotEqual(first, second)

    def test_review_card_fields_are_extracted(self):
        card = FakeElement(elements={
            ".Rqze5j": [FakeElement("reviewer")],
            "time": [FakeElement("1404/01/01")],
            ".nkJy9o": [FakeElement("good product")],
            ".bs-rating__star--active": [FakeElement() for _ in range(5)],
        })
        section = FakeSection(elements={
            'div[data-testid*="review"]': [card],
        })
        reviews = parse_review_cards(section)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["نام کاربر"], "reviewer")
        self.assertEqual(reviews[0]["امتیاز"], 5)
        self.assertEqual(reviews[0]["متن نظر"], "good product")


if __name__ == "__main__":
    unittest.main()
