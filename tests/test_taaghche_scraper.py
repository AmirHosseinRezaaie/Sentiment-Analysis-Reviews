import unittest

from src.sentiment_analysis.scraping.taaghche import _stable_id, parse_review_html


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

    def test_parser_extracts_main_reviews_and_ignores_replies(self):
        html = '''
        <div class="bookComments_comment___TU8v">
          <div class="bookComments_info__x"><div><div>reader one</div></div>
            <div><div class="name">reader one</div><div><span class="icon-star-2"></span><span class="icon-star-2"></span></div></div>
          </div>
          <time>1404/01/01</time>
          <div class="bookComments_content___9Xbz">main review</div>
        </div>
        <div class="bookComments_replies__dXS_n">
          <div class="bookComments_comment___TU8v"><div class="bookComments_content___9Xbz">reply</div></div>
        </div>
        '''
        reviews = parse_review_html(html)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["comment"], "main review")
        self.assertEqual(reviews[0]["stars"], 2)


if __name__ == "__main__":
    unittest.main()
