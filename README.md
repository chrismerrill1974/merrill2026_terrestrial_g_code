# A Terrestrial Test of Radial Dimensionality Theory: Source-Mass Density Dependence of Newton's Constant

Scientific source and reproducible results for version v3.

- [Paper](reproduction/output/pdf/publication/terrestrial/merrill_rdt_terrestrial_G_v3.pdf)
- [Manuscript](reproduction/paper6/terrestrial_G_note/note_terrestrial_G_v2.tex)

## Reproduction

Requires Python 3.14, NumPy 2.4.2, SciPy 1.17.1, Matplotlib 3.10.8,
TeX Live with revtex4-2, and Poppler. The resource controller uses POSIX
nice/setpriority, SIGPROF and SIGSTOP/SIGCONT.

Install the pinned Python dependencies in an isolated Python 3.14 environment
with `python3 -m pip install -r requirements.txt`.

From the repository directory:

```sh
nice -n 19 python3 reproduce.py --output /tmp/merrill2026_terrestrial_g_code-reproduction
```

The output directory must not exist. This verifies every capsule checksum,
regenerates tables, figures or algebraic checks from retained scientific outputs,
and builds a PDF whose extracted text matches the included paper.
No parameter scan runs in this command. Full scientific runs use the producing
scripts and their data under `reproduction/`. Use one worker, verified nice 19,
at most 95% of one CPU and one native-library thread.

`release.json` identifies the current manuscript and PDF;
`reproduction/CAPSULE.json` binds the scientific source and data by checksum.
Shared dependencies and saved results are included so no sibling checkout is
required. Historical top-level scripts and data retain their original identity;
the current paper and source manifest distinguish them from the revised results.

## Scientific scope

This version retains the published title and a testable laboratory proposal. Source-density dependence is a separately specified phenomenological force-law ansatz, not a derivation from the failed action in Paper VI. The revision corrects NIST uncertainty units and covariance propagation and withdraws unsupported cross-experiment amplitude bounds. Retained measurement contrasts are descriptive diagnostics, not a detection or calibrated bound.
