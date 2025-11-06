## ans-wrapper

ans-wrapper is a lightweight Python library that simplifies access to public healthcare datasets from the Agência Nacional de Saúde Suplementar (ANS). 

It abstracts away the manual process of having to navigate ANS’s FTP-like directories, download gigabytes of CSV files and manualy clean, filter and merger them into one single dataset, allowing you to do all of this with a single line of code.

### What this provides today

- **Demonstrações Contábeis**: fetch quarterly financial statements of Brazilian health plan operators directly from ANS as a `pandas.DataFrame`.

- **Beneficiários**: fetch granular monthly beneficiary datasets across Brazilian states.

### Installation


```bash
pip install ans_wrapper
```


### Quick start 

#### (Demonstrações Contábeis)

```python
from ans_wrapper.demonstracoes_contabeis import DemonstracoesContabeis

dc = DemonstracoesContabeis()

# 1) Download a single quarter
df = dc.get_info("1T2024")
print(df.head())

# 2) Download and combine multiple quarters
df_multi = dc.get_info(["4T2023", "1T2024", "2T2024"])

# 3) Filter by one or more operator codes (REG_ANS)
df_filtered = dc.get_info(["1T2024", "2T2024"], company=[353889, 323140])
```

#### (Beneficiarios)

```python
# Build a dataset for São Paulo and Rio de Janeiro between Jan–Apr 2024
df = b.build_dataset(states=["SP", "RJ"], start="202401", end="202404")
```

### Examples and notebooks

- See `notebooks/demonstracoes_contabeis.ipynb` for an exploratory example using real downloads.


### Where data is downloaded

- ZIPs are downloaded from ANS and saved under `ans_downloads/`.
- The first CSV inside each ZIP is extracted into the same folder and used to build the dataframe.

### Data source

- ANS Open Data Portal: `https://dadosabertos.ans.gov.br/FTP/PDA/`

### Roadmap

- Beneficiários module is under development and not 100% documented here yet.
- Possible additions: richer validations, caching, and more friendly error messages.
- Improve Autocomplete and Importing/Module Structure

### Development

- Formatters and linters are configured via `pyproject.toml` and `noxfile.py`.
- Run tests with `pytest` (if/when tests for this module are added).
