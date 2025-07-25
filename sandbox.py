import ans_wrapper as ans

beneficiarios = ans.Beneficiarios()

df = beneficiarios.build_dataset(
  target_date="202504",
  state="AC"
)

print(df.head())