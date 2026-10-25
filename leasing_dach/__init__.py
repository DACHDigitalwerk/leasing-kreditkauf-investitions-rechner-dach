"""
leasing_dach — DACH B2B Leasing- vs. Kreditkauf- & Eigenkapital-Vergleichsrechner 2026
"""

from .calculator import (
    LeasingComparisonInput,
    LeasingComparisonResult,
    calculate_leasing_vs_loan,
    check_bmf_40_90_rule,
)

__all__ = [
    "LeasingComparisonInput",
    "LeasingComparisonResult",
    "calculate_leasing_vs_loan",
    "check_bmf_40_90_rule",
]
__version__ = "1.0.0"
