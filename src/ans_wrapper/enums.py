"""
Provides a few enums to be used on the codebase. 
"""


from enum import Enum
from typing import Literal

BRAZILIAN_STATE_CODES = [
    "AC",  # Acre
    "AL",  # Alagoas
    "AP",  # Amapá
    "AM",  # Amazonas
    "BA",  # Bahia
    "CE",  # Ceará
    "DF",  # Distrito Federal
    "ES",  # Espírito Santo
    "GO",  # Goiás
    "MA",  # Maranhão
    "MT",  # Mato Grosso
    "MS",  # Mato Grosso do Sul
    "MG",  # Minas Gerais
    "PA",  # Pará
    "PB",  # Paraíba
    "PR",  # Paraná
    "PE",  # Pernambuco
    "PI",  # Piauí
    "RJ",  # Rio de Janeiro
    "RN",  # Rio Grande do Norte
    "RS",  # Rio Grande do Sul
    "RO",  # Rondônia
    "RR",  # Roraima
    "SC",  # Santa Catarina
    "SP",  # São Paulo
    "SE",  # Sergipe
    "TO",  # Tocantins
]

STATE_CODES = Literal[
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]


class States(Enum):
    AC = ("Acre", "Norte")
    AL = ("Alagoas", "Nordeste")
    AP = ("Amapá", "Norte")
    AM = ("Amazonas", "Norte")
    BA = ("Bahia", "Nordeste")
    CE = ("Ceará", "Nordeste")
    DF = ("Distrito Federal", "Centro-Oeste")
    ES = ("Espírito Santo", "Sudeste")
    GO = ("Goiás", "Centro-Oeste")
    MA = ("Maranhão", "Nordeste")
    MT = ("Mato Grosso", "Centro-Oeste")
    MS = ("Mato Grosso do Sul", "Centro-Oeste")
    MG = ("Minas Gerais", "Sudeste")
    PA = ("Pará", "Norte")
    PB = ("Paraíba", "Nordeste")
    PR = ("Paraná", "Sul")
    PE = ("Pernambuco", "Nordeste")
    PI = ("Piauí", "Nordeste")
    RJ = ("Rio de Janeiro", "Sudeste")
    RN = ("Rio Grande do Norte", "Nordeste")
    RS = ("Rio Grande do Sul", "Sul")
    RO = ("Rondônia", "Norte")
    RR = ("Roraima", "Norte")
    SC = ("Santa Catarina", "Sul")
    SP = ("São Paulo", "Sudeste")
    SE = ("Sergipe", "Nordeste")
    TO = ("Tocantins", "Norte")


URL_BENEFICIARIOS = "https://dadosabertos.ans.gov.br/FTP/PDA/informacoes_consolidadas_de_beneficiarios-024/"

URL = "https://dadosabertos.ans.gov.br/FTP/"
