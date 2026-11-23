import unittest

from src.sentiment_analysis.scraping.trustpilot import _rating_from_alt, _stable_id, parse_review_html


class TrustpilotParsingHelpersTests(unittest.TestCase):
    def test_rating_is_parsed_from_accessible_alt_text(self):
        self.assertEqual(_rating_from_alt("Rated 5 out of 5 stars"), 5)
        self.assertEqual(_rating_from_alt("Rated 3 stars"), 3)

    def test_unknown_or_invalid_rating_is_not_zero(self):
        self.assertIsNone(_rating_from_alt("Rating unavailable"))
        self.assertIsNone(_rating_from_alt("Rated 0 out of 5 stars"))

    def test_review_identity_is_deterministic(self):
        self.assertEqual(
            _stable_id("customer", "2026-01-01", 5, "good"),
            _stable_id("customer", "2026-01-01", 5, "good"),
        )

    def test_parser_extracts_rating_and_preserves_unknown_rating(self):
        html = '''
        <article data-service-review-card-paper>
          <span data-consumer-name-typography>Reviewer A</span>
          <time datetime="2026-01-02">2 days ago</time>
          <img alt="Rated 4 out of 5 stars" />
          <p data-service-review-text-typography>Great service</p>
        </article>
        <article data-service-review-card-paper>
          <span data-consumer-name-typography>Reviewer B</span>
          <p data-service-review-text-typography>No rating supplied</p>
        </article>
        '''
        reviews = parse_review_html(html)
        self.assertEqual(reviews[0]["stars"], 4)
        self.assertIsNone(reviews[1]["stars"])


if __name__ == "__main__":
    unittest.main()
