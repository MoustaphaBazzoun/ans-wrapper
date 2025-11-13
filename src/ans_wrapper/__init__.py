"""ANS Wrapper - A Python wrapper for ANS ftp server

This package provides access to financial statements and beneficiary information
from the Brazilian National Health Agency (ANS).
"""

# Import the main classes
from ans_wrapper.beneficiarios import Beneficiarios
from ans_wrapper.demonstracoes_contabeis import DemonstracoesContabeis

__all__ = ["Beneficiarios", "DemonstracoesContabeis"]

__version__ = "0.1.1"
__author__ = "Mousta Bazzoun"
__email__ = "bazzounmousta@gmail.com"
