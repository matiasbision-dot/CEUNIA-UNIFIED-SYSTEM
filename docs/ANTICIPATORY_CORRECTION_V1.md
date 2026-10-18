# CEUNIA Ω online metacode v1.1

The runner retrieves NASA POWER monthly T2M for a point near Mar del Plata and replays each month as a simulated future. At time t, persistence, seasonal-naive, and online-corrected predictions are made from prior observations only. A trailing window of already revealed outcomes selects a model only when it beats persistence by a minimum relative margin. Then target t is revealed and the exponential moving average of seasonal residuals is updated for t+1.

This is genuine online-style sequential evaluation on historical data, not knowledge of the actual future. The downloaded response and final report receive SHA-256 fingerprints. The report contains each model's MAE, improvements versus persistence, and selection counts. Results must be interpreted with a final untouched chronological holdout; online selection itself can overfit the recent validation window. No financial or external actions are performed.

Run:
```bash
python -m unittest discover -s tests -p "test_nasa_power_validation.py" -v
python -m ceunia.metacode.nasa_power_validation
```
