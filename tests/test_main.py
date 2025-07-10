import ans_wrapper

# Initializando
beneficiarios = ans_wrapper.Beneficiarios()

# Exemplos

# retorna o dataset do mês/ano mais recente para todos os estados
df_geral = beneficiarios.make_dataset()

# dataset do mês/ano mais recente para sp
df_sp = beneficiarios.make_dataset(states="SP")

# dataset do mês/ano mais recente para uma lista de estados contendo SP e RJ
df_sp_rj = beneficiarios.make_dataset(states=["SP", "RJ"])

# Dados para SP em julho de 2021
df_sp_julho_2021 = beneficiarios.make_dataset(states="SP", date="2021-07")

# dataset com a evolução dos dados ao longo dos meses de 2020 (jan a dez) para sp
df_sp_dec_2020 = beneficiarios.make_dataset(states="SP", year="2020")

# Dados para SP começando em jan/2022 e indo até dez de 2023
df_sp_2022_a_2023 = beneficiarios.make_dataset(
    states="SP", start="2022-01", end="2023-12"
)

#
