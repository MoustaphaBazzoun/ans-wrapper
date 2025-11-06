"""ANS Wrapper - A Python wrapper for ANS ftp server

This package provides access to financial statements and beneficiary information
from the Brazilian National Health Agency (ANS).
"""

# Import the main classes
from ans_wrapper.beneficiarios import Beneficiarios
from ans_wrapper.demonstracoes_contabeis import DemonstracoesContabeis

# Explicitly define what should be available for import
__all__ = [
    "Beneficiarios",
    "DemonstracoesContabeis"
]

# Type hints for better IDE support
__version__: str = "0.1.1"
__author__: str = "Mousta Bazzoun"
__email__: str = "bazzounmousta@gmail.com"

