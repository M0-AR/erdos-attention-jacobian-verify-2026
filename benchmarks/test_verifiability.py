"""B2: SymPy verifiability — 2016 sign-bug regression + Poly/Expr guard."""
import sympy as sp
from jacobian.verification import classic_bug_demo, factor_poly_checked, resultant_checked


def test_resultant_sign_bug_fixed():
    res = classic_bug_demo()
    assert res.value["pass"] is True, res.certificate.evidence
    assert res.certificate.verified is True
    # live-repro documentation: on SymPy 1.14.0 the raw call is still wrong
    assert res.value["bug_live"] is True
    assert res.certificate.evidence["wrapper_detected"] is True


def test_resultant_swap_identity_holds_both_orders():
    x = sp.symbols("x")
    r1 = resultant_checked(x + 2, x**3, x)
    r2 = resultant_checked(x**3, x + 2, x)
    # wrapper always executes both paths
    assert r1.certificate.verified and r2.certificate.verified
    # ground truth respects (-1)^(1*3) = -1 flip even when SymPy does not
    assert int(r1.value) == -8
    assert int(r2.value) == 8
    # and it correctly flags SymPy as wrong on the ascending-degree order
    assert r1.certificate.evidence["sympy_correct"] is False


def test_factor_poly_guards_21180():
    x = sp.symbols("x")
    p = sp.Poly(x**4 + 6 * x**3 + 4 * x**2 - 30 * x - 45, x)
    res = factor_poly_checked(p)
    assert res.certificate.verified is True
    # (x+3)^2 (x^2-5): check factor multiset
    facs = sorted([(str(f.as_expr()), e) for f, e in res.value[1]])
    assert any("x + 3" in s and e == 2 for s, e in facs)
