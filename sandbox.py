import requests
import pandas as pd

URL = "https://www.ans.gov.br/operadoras-entity/v1/operadoras"

r = requests.get(URL)
print(r.json())