import pytest

from ans_wrapper.beneficiarios import Beneficiarios


def test_available_months_not_empty():
    b = Beneficiarios()
    assert isinstance(b.available_months, list)
    assert len(b.available_months) > 0
    assert all(m.isdigit() and len(m) == 6 for m in b.available_months)


def test_date_range_format():
    b = Beneficiarios()
    output = b.date_range
    assert isinstance(output, str)
    assert "data available from" in output
    assert "to" in output
