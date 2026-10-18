import unittest
from ceunia.metacode.nasa_power_validation import mae,run_walk_forward
class OnlineMetaCodeTests(unittest.TestCase):
 def test_mae(self): self.assertAlmostEqual(mae([1,2],[2,2]),.5)
 def test_online_replay_counts_and_protocol(self):
  months=[f"{2000+i//12:04d}-{i%12+1:02d}" for i in range(120)]
  values=[10+.2*(i%12) for i in range(120)]
  r=run_walk_forward(months,values,initial_train=60,validation_window=12)
  self.assertEqual(r["test_months"],60)
  self.assertEqual(r["test_start"],months[60])
  self.assertEqual(sum(r["selection_counts"].values()),60)
  self.assertTrue(r["online_learning"]["enabled"])
  self.assertIn("reveal current target",r["protocol"])
  self.assertEqual(set(r["mae_by_model"]),{"persistence","seasonal","online_corrected","gated"})
 def test_rejects_invalid_inputs(self):
  with self.assertRaises(ValueError): run_walk_forward(["2000-01"],[1],initial_train=24)
if __name__=="__main__": unittest.main()
