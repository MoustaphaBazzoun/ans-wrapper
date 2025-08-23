# ANS Wrapper

A Python wrapper for accessing Brazilian National Health Agency (ANS) open data portal. This package provides easy access to financial statements and beneficiary information from health plan operators in Brazil.

## Features

- **Financial Statements**: Download quarterly financial data (balance sheets and income statements)
- **Beneficiary Information**: Access consolidated beneficiary data by state and month
- **Easy Data Filtering**: Filter data by company ANS codes, quarters, states, and date ranges
- **Automated Downloads**: Handle ZIP file downloads and CSV extraction automatically
- **Type Safety**: Full type hints and comprehensive error handling

## Installation

### From PyPI
```bash
pip install ans-wrapper
```

### From Source
```bash
git clone https://github.com/yourusername/ans-wrapper.git
cd ans-wrapper
pip install -e .
```

## Quick Start

```python
from ans_wrapper import DemonstracoesContabeis, Beneficiarios

# Access financial statements
dc = DemonstracoesContabeis()
financial_data = dc.get_info(quarters=["1T2024", "2T2024"], company=12345)

# Access beneficiary data
bf = Beneficiarios()
print(bf.info)  # See available data range
beneficiary_data = bf.build_dataset(states=["SP", "RJ"], start="202401", end="202403")
```

## API Reference

### DemonstracoesContabeis

The `DemonstracoesContabeis` class provides access to quarterly financial statements from health plan operators.

#### Methods

##### `get_info(quarters, company=None)`

Downloads and filters financial data for specified quarters and companies.

**Parameters:**
- `quarters` (Union[str, List[str]]): Quarter(s) in format "1T2024", "2T2023", etc.
- `company` (Optional[Union[str, int, List[Union[str, int]]]]): ANS code(s) to filter by. If None, returns full dataset.

**Returns:**
- `pd.DataFrame`: Filtered financial data with columns including REG_ANS

**Example:**
```python
dc = DemonstracoesContabeis()

# Get data for specific quarters
data = dc.get_info(quarters=["1T2024", "2T2024"])

# Filter by specific company
company_data = dc.get_info(quarters="1T2024", company=12345)

# Filter by multiple companies
companies_data = dc.get_info(quarters=["1T2024"], company=[12345, 67890])
```

### Beneficiarios

The `Beneficiarios` class provides access to consolidated beneficiary information by state and month.

#### Properties

- `info`: Summary of available data range and source
- `date_range`: Human-readable range of available data
- `available_months`: List of available months in YYYYMM format

#### Methods

##### `build_dataset(states, target_date=None, start=None, end=None)`

Creates a dataset using customized configurations for states and date ranges.

**Parameters:**
- `states` (Union[STATE_CODES, List[STATE_CODES]]): Brazilian state code(s) (e.g., "SP", "RJ", "AC")
- `target_date` (str, optional): Specific target date in YYYYMM format
- `start` (str, optional): Start date in YYYYMM format
- `end` (str, optional): End date in YYYYMM format

**Note:** Provide either `target_date` OR both `start` and `end`, not both.

**Example:**
```python
bf = Beneficiarios()

# Get data for specific states and date range
data = bf.build_dataset(states=["SP", "RJ"], start="202401", end="202403")

# Get data for specific month
data = bf.build_dataset(states="AC", target_date="202401")

# Get data for multiple states
data = bf.build_dataset(states=["AC", "AM", "CE"], start="202305", end="202412")
```

##### `download_raw_data(states, dates)`

Downloads raw, unaltered datasets from the ANS server.

**Parameters:**
- `states` (List[str]): List of state codes
- `dates` (List[str]): List of dates in YYYM format

**Returns:**
- List of CSV file paths

## Data Sources

- **Financial Statements**: Quarterly data from ANS open data portal
- **Beneficiary Information**: Monthly consolidated data by Brazilian state
- **Base URL**: https://dadosabertos.ans.gov.br/FTP/PDA/

## Supported States

The package supports all Brazilian states using their standard abbreviations:
- AC (Acre), AL (Alagoas), AM (Amazonas), AP (Amapá)
- BA (Bahia), CE (Ceará), DF (Distrito Federal), ES (Espírito Santo)
- GO (Goiás), MA (Maranhão), MG (Minas Gerais), MS (Mato Grosso do Sul)
- MT (Mato Grosso), PA (Pará), PB (Paraíba), PE (Pernambuco)
- PI (Piauí), PR (Paraná), RJ (Rio de Janeiro), RN (Rio Grande do Norte)
- RO (Rondônia), RR (Roraima), RS (Rio Grande do Sul), SC (Santa Catarina)
- SE (Sergipe), SP (São Paulo), TO (Tocantins)

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/ans-wrapper.git
cd ans-wrapper

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Running Tests and Quality Checks

```bash
# Run all quality checks
nox

# Run specific sessions
nox -s lint          # Run flake8 and pylint
nox -s type_check    # Run mypy type checking
nox -s format        # Format code with black and isort
nox -s check_formatting  # Check formatting without modifying files
nox -s run_tests     # Run pytest
```

### Code Formatting

The project uses:
- **Black** with 80-character line length
- **isort** for import sorting
- **flake8** and **pylint** for linting
- **mypy** for type checking

## Project Structure

```
ans-wrapper/
├── src/
│   └── ans_wrapper/
│       ├── __init__.py
│       ├── demonstracoes_contabeis.py  # Financial statements
│       ├── beneficiarios.py            # Beneficiary information
│       ├── beneficiarios_utils.py      # Helper utilities
│       ├── download_utils.py           # Download utilities
│       └── enums.py                    # Constants and enums
├── tests/                              # Test files
├── docs/                               # Documentation
├── notebooks/                          # Jupyter notebooks
├── noxfile.py                         # Nox automation
├── pyproject.toml                     # Project configuration
└── README.md                          # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact: bazzounmousta@gmail.com

## Acknowledgments

- Brazilian National Health Agency (ANS) for providing open data
- The open-source community for the tools and libraries used in this project
