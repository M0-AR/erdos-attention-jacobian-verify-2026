"""Jacobian core: atomic, composable, statically-typed techniques.

Design rule (verifiability-first):
- Every technique is a pure function with typed inputs/outputs + a Certificate.
- Compute path (fast, possibly buggy: SymPy/NumPy) is NEVER trusted alone.
- Verify path (independent, minimal, auditable) must re-check the certificate.
- This mirrors the 2026 best practice: skeptical architecture
  (Sage/SymPy = untrusted oracle, Lean/kernel = checker; cf. Veriphy,
  GroebnerTactic, Bourbaki compute-then-verify, Tao 2026).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Certificate:
    technique: str
    claim: str
    evidence: dict
    verified: bool
    checker: str = "independent-python"
    notes: str = ""


@dataclass(frozen=True)
class TechniqueResult(Generic[T]):
    value: T
    certificate: Certificate


Technique = Callable[..., TechniqueResult]
