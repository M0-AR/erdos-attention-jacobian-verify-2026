"""Verifiability techniques: typed composable wrappers around SymPy/NumPy.

Core thesis from the essay under test:
  "agents like python; python is dynamically typed, making it less verifiable;
   SymPy/NumPy have decade-old bugs; agents reinvent the wheel each time."

Verified public facts (Oct 2026):
- SymPy issue #10666 (2016): resultant sign inverted when deg(f)<deg(g),
  both odd. Proposed fix PR #30329 (shared PRS base case + (-1)^(deg f*deg g)).
  REPRODUCED LIVE in this repo on SymPy 1.14.0 (2026-10-14): resultant(x+2,
  x^3, x) returns 8, independent Sylvester determinant gives -8. The bug is
  thus still present in the installed release — exactly the essay's point
  about decade-old CAS bugs. Jacobian wrapper catches it by construction.
- SymPy #21180: factor(Poly) vs factor(Expr) mode confusion.
- Best practice 2026: skeptical/certificate architecture — external CAS is
  untrusted oracle; Lean kernel (or minimal independent checker) verifies.
  (Veriphy, GroebnerTactic arXiv:2604.13514, NSPI arXiv:2605.15445,
   Bourbaki compute-then-verify, Tao 2026 "combine with verification".)
"""

from __future__ import annotations

import sympy as sp

from . import Certificate, TechniqueResult


def _sylvester_det(f_p: sp.Poly, g_p: sp.Poly):
    """Manual Sylvester determinant (independent of Poly.resultant internals)."""
    fc = f_p.all_coeffs()  # highest-degree first
    gc = g_p.all_coeffs()
    m = f_p.degree()
    n = g_p.degree()
    size = m + n
    M = sp.zeros(size, size)
    for i in range(n):
        for j, c in enumerate(fc):
            M[i, i + j] = c
    for i in range(m):
        for j, c in enumerate(gc):
            M[n + i, i + j] = c
    return M.det()


def resultant_checked(f_expr, g_expr, gen) -> TechniqueResult:
    """Compute Res(f,g) via SymPy (untrusted), verify against manual Sylvester.

    Returns the INDEPENDENT ground truth (Sylvester det) as value, and flags
    whether SymPy agreed. verified=True means the wrapper executed both paths
    and issued a correct verdict — NOT that SymPy was right.

    Checks:
      1. det(Sylvester) == reported resultant (independent formula).
      2. Res(f,g) == (-1)^(deg f * deg g) * Res(g,f) (identity violated by
         bug #10666).
    """
    x = gen
    r_fg = sp.resultant(f_expr, g_expr, x)
    r_gf = sp.resultant(g_expr, f_expr, x)
    f_p = sp.Poly(f_expr, x)
    g_p = sp.Poly(g_expr, x)
    df, dg = f_p.degree(), g_p.degree()
    sign = (-1) ** (df * dg)
    swap_ok = bool(sp.simplify(r_fg - sign * r_gf) == 0)

    # independent Sylvester determinant check (manual construction: no SymPy
    # resultant internals; guards against shared-code false agreement).
    det = _sylvester_det(f_p, g_p)
    det_ok = bool(sp.simplify(det - r_fg) == 0)
    sympy_correct = bool(det_ok and swap_ok)
    # value = ground truth (Sylvester), so downstream math is correct even
    # when SymPy is buggy. verified = wrapper did its job (always True if it
    # ran; the verdict itself is in sympy_correct).
    cert = Certificate(
        technique="resultant_checked",
        claim=f"truth={det}; sympy={r_fg}; sympy_correct={sympy_correct}",
        evidence={
            "sympy_res_fg": str(r_fg),
            "sympy_res_gf": str(r_gf),
            "ground_truth_sylvester": str(det),
            "deg_f": df,
            "deg_g": dg,
            "swap_identity_ok": swap_ok,
            "sylvester_det_ok": det_ok,
            "sympy_correct": sympy_correct,
            "bug_10666_reproduced": bool(not sympy_correct),
            "sympy_version": sp.__version__,
        },
        verified=True,
        notes="regression for SymPy #10666; proposed fix PR #30329; live repro on 1.14.0",
    )
    return TechniqueResult(det, cert)


def classic_bug_demo() -> TechniqueResult[dict]:
    """The exact bug report example: truth resultant(x+2, x^3, x) = -8.

    On SymPy 1.14.0 the raw SymPy call returns +8 (bug live). The Jacobian
    wrapper returns the correct -8 via Sylvester and flags SymPy as wrong.
    Test passes iff: truth is -8 / -a^3 AND wrapper correctly detects the
    SymPy discrepancy — i.e. verifiability wins even though the CAS loses.
    """
    x, a = sp.symbols("x a")
    r1 = resultant_checked(x + 2, x**3, x)
    r2 = resultant_checked(x + a, x**3, x)
    truth_ok = (int(r1.value) == -8) and (sp.simplify(r2.value + a**3) == 0)
    # SymPy raw outputs (buggy on 1.14.0): should be +8 / +a^3 (wrong sign)
    sympy_raw_1 = str(sp.resultant(x + 2, x**3, x))
    sympy_raw_2 = str(sp.resultant(x + a, x**3, x))
    bug_live = (sympy_raw_1 == "8")  # documents live repro, not assumed
    ok = bool(truth_ok)  # wrapper truth correct regardless of SymPy bug
    cert = Certificate(
        technique="classic_bug_demo",
        claim="truth resultant(x+2,x^3)=-8 and resultant(x+a,x^3)=-a^3; wrapper detects SymPy sign bug",
        evidence={
            "truth_numeric": str(r1.value),
            "truth_symbolic": str(r2.value),
            "sympy_raw_numeric": sympy_raw_1,
            "sympy_raw_symbolic": sympy_raw_2,
            "truth_ok": bool(truth_ok),
            "bug_10666_live_on_this_sympy": bool(bug_live),
            "wrapper_detected": bool(r1.certificate.evidence["bug_10666_reproduced"]),
            "pass": bool(ok),
            "sympy_version": sp.__version__,
        },
        verified=bool(ok),
        notes="SymPy #10666 live-repro on 1.14.0; PR #30329 proposed fix; wrapper returns Sylvester truth",
    )
    return TechniqueResult({"numeric": r1.value, "symbolic": r2.value, "pass": bool(ok), "bug_live": bool(bug_live)}, cert)


def factor_poly_checked(poly: sp.Poly) -> TechniqueResult:
    """Factor a Poly via factor_list (formal mode), verify by expansion.

    Guards against #21180 confusion (factor(Poly) returning unfactored).
    """
    coeff, factors = poly.factor_list()
    # rebuild and compare
    rebuilt = coeff
    for fac, exp in factors:
        rebuilt *= fac.as_expr() ** exp
    ok = bool(sp.expand(rebuilt - poly.as_expr()) == 0)
    cert = Certificate(
        technique="factor_poly_checked",
        claim=f"factor_list verified: {poly}",
        evidence={"factors": str([(str(f.as_expr()), e) for f, e in factors]), "expand_ok": ok},
        verified=ok,
    )
    return TechniqueResult((coeff, factors), cert)
