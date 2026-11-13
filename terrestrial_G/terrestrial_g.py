"""
terrestrial_g.py -- RDT predicted source-mass-density differential in measured
G (the Paper VI continuation note).

RDT weak-field Gauss law: div^2 Phi = 4 pi G_eff(rho) rho, with
    G_eff(rho)/G_N = 1/(1 - sigma),  sigma = A x/(1+x),  x=(rho/rho0)^alpha,
    rho0 = 150 g/cm^3,  A <= 0.0087 (solar ceiling, Paper I),  alpha in [0.02,0.5].
For a uniform body the EXTERNAL field integrates to dPhi/dr = G_eff(rho) M/r^2,
so its external pull is enhanced by 1/(1-sigma(rho)): denser masses gravitate
(fractionally) harder. The bare G_N is unmeasurable, but the DIFFERENCE between
two source-mass materials is observable:

    (Delta G / G)_{1,2} = (1-sigma_2)/(1-sigma_1) - 1  ~  sigma(rho_1) - sigma(rho_2).

Includes single-crystal sapphire (Al2O3, 3.98 g/cc), the low-density source
mass used in the NIST-2026 controlled swap and proposed for a dedicated
experiment. Effect scales linearly in A; tabulated at the solar ceiling
A=0.0087.

Single-threaded run recommended:
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 terrestrial_g.py
"""
import numpy as np

A_SOLAR = 0.0087
RHO0 = 150.0

# source-mass materials used by precision-G experiments (g/cm^3)
MATERIALS = {
    "Aluminium": 2.70, "Sapphire": 3.98, "Titanium": 4.51,
    "Steel(SS)": 8.00, "Copper": 8.96, "Mercury": 13.53,
    "W-alloy": 18.00, "Tungsten": 19.30, "Platinum": 21.45,
}

G_SCATTER = 4.0e-4       # spread between modern experiments ("the puzzle")
G_BESTPAIR = 1.0e-4      # typical agreement of the best experiments
G_BESTPREC = 2.0e-5      # best single-experiment precision


def sigma(rho, A, alpha):
    x = (rho / RHO0) ** alpha
    return A * x / (1.0 + x)


def dG_over_G(rho1, rho2, A, alpha):
    s1, s2 = sigma(rho1, A, alpha), sigma(rho2, A, alpha)
    return (1.0 - s2) / (1.0 - s1) - 1.0


if __name__ == "__main__":
    alphas = [0.02, 0.12, 0.334, 0.50]
    print(f"RDT: G_eff/G = 1/(1-sigma), sigma=A x/(1+x), A={A_SOLAR} (solar "
          f"ceiling), rho0={RHO0} g/cm^3\n")

    print("sigma(rho) by material (at A=0.0087):")
    print(f"  {'material':>10} {'rho':>6}   " +
          "  ".join(f"a={a:<4}" for a in alphas))
    for name, rho in MATERIALS.items():
        vals = "  ".join(f"{sigma(rho, A_SOLAR, a):.5f}" for a in alphas)
        print(f"  {name:>10} {rho:6.2f}   {vals}")

    # ---- Table 1 of the note (Delta G/G = sigma(dense) - sigma(light)) ----
    print("\nPredicted Delta G/G = sigma(rho1)-sigma(rho2), A=0.0087:")
    pairs = [("Tungsten", "Aluminium"), ("Tungsten", "Sapphire"),
             ("Tungsten", "Steel(SS)"), ("Copper", "Sapphire")]
    print(f"  {'pair (rho1-rho2)':>26}   " + "  ".join(f"a={a:<6}" for a in alphas))
    for hi, lo in pairs:
        r_hi, r_lo = MATERIALS[hi], MATERIALS[lo]
        vals = "  ".join(f"{dG_over_G(r_hi, r_lo, A_SOLAR, a):.2e}"
                         for a in alphas)
        lbl = f"{hi}({r_hi:.1f})-{lo}({r_lo:.1f})"
        print(f"  {lbl:>26}   {vals}")

    # ---- the dedicated-experiment swing: sapphire -> tungsten ----
    print(f"\nDedicated-experiment signal  (sapphire 3.98 -> tungsten 19.30 "
          f"swing, A=0.0087):")
    for a in alphas:
        d = dG_over_G(MATERIALS["Tungsten"], MATERIALS["Sapphire"], A_SOLAR, a)
        req = d / 3.0   # single-exp precision for a 3-sigma detection
        print(f"  alpha={a:<5} dG/G={d:.2e}  (needs single-exp precision "
              f"<~{req:.1e} for a 3-sigma detection; best today ~{G_BESTPREC:.0e})")

    print(f"\nMeasured-G landscape (relative): scatter ~{G_SCATTER:.0e}, "
          f"best-pair ~{G_BESTPAIR:.0e}, best single-exp precision "
          f"~{G_BESTPREC:.0e}")
    print("Effect scales linearly in A. The observable is the source-density")
    print("differential; the absolute vs bare G_N is absorbed into G.")
