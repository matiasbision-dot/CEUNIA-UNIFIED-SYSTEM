import unittest
from ceunia.metacode.anticipatory_correction import make_synthetic_history, walk_forward


class AnticipatoryCorrectionTests(unittest.TestCase):
    def test_reproducible_result_and_hash(self):
        a = walk_forward(make_synthetic_history())
        b = walk_forward(make_synthetic_history())
        self.assertEqual(a, b)
        self.assertEqual(len(a["result_sha256"]), 64)

    def test_target_boundary_and_sample_count(self):
        result = walk_forward(make_synthetic_history(300), start=50, window=32)
        self.assertEqual(result["n_test"], 250)
        self.assertIn("predict -> score/reveal target -> update correction", result["protocol"])

    def test_invalid_window_is_rejected(self):
        with self.assertRaises(ValueError):
            walk_forward([1.0, 2.0, 3.0], start=2, window=3)

    def test_invalid_alpha_is_rejected(self):
        with self.assertRaises(ValueError):
            walk_forward(make_synthetic_history(100), start=30, window=20, alpha=0)


if __name__ == "__main__":
    unittest.main()
