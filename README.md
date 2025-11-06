## ans-wrapper

Small Python wrapper around the ANS (Agência Nacional de Saúde Suplementar) open data portal to help download and work with datasets. For now, the focus is on financial statements ("demonstrações contábeis"). The beneficiaries ("beneficiários") module is a work in progress.

### What this provides today

- **Demonstrações Contábeis**: download quarterly financial statements for Brazilian health plan operators directly from ANS, optionally filter by operator `REG_ANS` code(s), and receive a combined `pandas.DataFrame`.
- Files are downloaded from the official ANS FTP and extracted locally.

### Installation


```bash
pip install ans_wrapper
```

Requirements are declared in `pyproject.toml` and include `requests`, `pandas`, and `tqdm`.

### Quick start (Demonstrações Contábeis)

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

### API (Demonstrações Contábeis)

`DemonstracoesContabeis.get_info(quarters, company=None) -> pandas.DataFrame`

- **quarters**: string like `"1T2024"` or list of strings, e.g. `["4T2023", "1T2024"]`.
- **company**: optional `REG_ANS` code or list of codes (`str` or `int`). When provided, the returned dataframe is filtered to those operators and will raise a `ValueError` if any requested code is not present in the dataset for the selected quarters.
- **return**: a combined dataframe with all rows from the requested quarter files (and filtered by `REG_ANS` if `company` is provided).

### Where data is downloaded

- ZIPs are downloaded from ANS and saved under `ans_downloads/`.
- The first CSV inside each ZIP is extracted into the same folder and used to build the dataframe.

### Data source

- ANS Open Data Portal: `https://dadosabertos.ans.gov.br/FTP/PDA/`
- This wrapper uses the `demonstracoes_contabeis` endpoint. Example URL format used internally:
  - `https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/{YEAR}/{QUARTER}T{YEAR}.zip`
  - Example: `.../2024/1T2024.zip`

### Notes, assumptions, and tips

- The CSVs are semicolon-separated (`;`) and read with `pandas.read_csv(sep=";")`.
- The operator code column is expected as `REG_ANS` and is coerced to `int` when filtering.
- If a quarter file is missing upstream or fails to download, the call continues with the remaining quarters and raises if none could be read.
- The function prints simple progress/diagnostics during downloads and CSV reads.

### Examples and notebooks

- See `notebooks/demonstracoes_contabeis.ipynb` for an exploratory example using real downloads.

### Roadmap

- Beneficiários module is under development and not documented here yet.
- Possible additions: richer validations, caching, and more friendly error messages.
- Improve Autocomplete and Importing/Module Structure

### Development

- Formatters and linters are configured via `pyproject.toml` and `noxfile.py`.
- Run tests with `pytest` (if/when tests for this module are added).



