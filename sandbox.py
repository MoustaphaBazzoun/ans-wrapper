from src.ans_wrapper import Beneficiarios

beneficiarios = Beneficiarios()

ret = beneficiarios.build_dataset(
    states=["AC", "RO"],
    target_date="202401"
)

print(ret)