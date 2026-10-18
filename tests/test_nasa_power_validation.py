import unittest
from ceunia.metacode.nasa_power_validation import mae, run_walk_forward

class NasaPowerValidationTests(unittest.TestCase):
    def test_mae(self):
        self.assertAlmostEqual(mae([1, 2], [2, 2]), .5)
    def test_chronological_walk_forward(self):
        months=[f"{2000+i//12:04d}-{i%12+1:02d}" for i in range(120)]
        values=[10 + 0.2*(i%12) for i in range(120)]
        result=run_walk_forward(months, values, initial_train=60, validation_window=12)
        self.assertEqual(result["test_months"], 60)
        self.assertEqual(result["test_start"], months[60])
        self.assertEqual(result["protocol"], "forecast using months < t -> lock -> reveal month t -> score -> update residual")
    def test_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            run_walk_forward(["2000-01"], [1], initial_train=24)
if __name__ == "__main__": unittest.main()
