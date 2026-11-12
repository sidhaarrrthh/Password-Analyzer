
import unittest
from password_analyzer import analyze_password


class TestPasswordAnalyzer(unittest.TestCase):

    def test_common_password(self):
        result = analyze_password("password")
        self.assertTrue(
            any("common-password" in warning.lower()
                for warning in result["warnings"])
        )

    def test_repeated_characters(self):
        result = analyze_password("Abcaaa!9ZxQ")
        self.assertTrue(
            any("repeated" in warning.lower()
                for warning in result["warnings"])
        )

    def test_sequential_pattern(self):
        result = analyze_password("Abcd!9Xy#7Qp")
        self.assertTrue(
            any("sequence" in warning.lower()
                for warning in result["warnings"])
        )

    def test_short_password(self):
        result = analyze_password("Ab1!")
        self.assertTrue(
            any("shorter" in warning.lower()
                for warning in result["warnings"])
        )
    
    def test_repeated_sequence(self):
        result = analyze_password("Abcabc!92")
        self.assertTrue(
            any("repeated sequence" in warning.lower()
                for warning in result["warnings"])
        )

    def test_single_character_type(self):
        result = analyze_password("123456789")
        self.assertTrue(
            any("one character type" in warning.lower()
                for warning in result["warnings"])
        )

    def test_review_status(self):
        result = analyze_password("password")
        self.assertEqual(result["review_status"], "Review recommended")


    def test_score_range(self):
        result = analyze_password("Example!92#Test")
        self.assertIn(result["score"], range(5))


if __name__ == "__main__":
    unittest.main()