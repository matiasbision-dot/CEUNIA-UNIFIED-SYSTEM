import unittest
from ceunia.metacode.anticipatory_correction import make_synthetic_history, walk_forward
class AnticipatoryCorrectionTests(unittest.TestCase):
    def test_reproducible_hash(self):
        self.assertEqual(walk_forward(make_synthetic_history()),walk_forward(make_synthetic_history()))
        self.assertEqual(len(walk_forward(make_synthetic_history())["result_sha256"]),64)
    def test_causal_protocol_and_count(self):
        r=walk_forward(make_synthetic_history(300),start=50,window=32,validation=24)
        self.assertEqual(r["n_test"],250)
        self.assertEqual(r["protocol"],"predict -> lock -> reveal target -> score -> update")
    def test_gate_rejects_unproven_candidates_on_reference_series(self):
        r=walk_forward(make_synthetic_history(),improvement_margin=.03)
        self.assertEqual(r["selection_counts"]["raw_trend"],0)
        self.assertEqual(r["selection_counts"]["adaptive_correction"],0)
        self.assertAlmostEqual(r["evidence_gated_mae"],r["baseline_mae"],places=12)
    def test_invalid_window_alpha_validation(self):
        with self.assertRaises(ValueError): walk_forward([1.,2.,3.],start=2,window=3)
        with self.assertRaises(ValueError): walk_forward(make_synthetic_history(100),start=30,window=20,alpha=0)
        with self.assertRaises(ValueError): walk_forward(make_synthetic_history(100),start=30,window=20,validation=2)
if __name__=="__main__": unittest.main()
