# p-value correction for peeking in comparison tests

Demonstration of correction for p-values to avoid
inflating reported statistical significance in sequential experimentation. 
For a full explanation,
[check out the post](https://e2eml.school/correcting_for_peeking.html).

## Requirements

In addition to a Python interpreter, this code relies on the `numpy` and
`matplotlib` packages.

## Run the code

Generate some simulated data.

```bash
python3 sim_ab.py
```

Run the significance report with the correction.

```bash
python3 phi_correction.py
```

Compare against the Optimizely correction.

```bash
python3 optimizely_correction.py
```

## Modify the code

Change the number of runs by modifying `N_RUNS` in `sim_ab.py`.

Change the number of data points collected by modifying
`N_OBSERVATIONS` in `sim_ab.py`.

Adjust the $\phi$ correction factor by modifying `phi` in 
`phi_correction.py`. To remove the influence of the correction
factor altogether, set `phi = 1`.

Adjust the $\tau$ parameter in the Optimizely method by modifying `tau`
in `optimizely_correction.py`.

Change the significance threshold by uncommenting the relevant lines
at the beginning of `phi_correction.py`.
