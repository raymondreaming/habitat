from datetime import date

import pytest

from app.dates import parse_target_date


def test_parse_target_date_accepts_iso_date():
    assert parse_target_date("2026-05-26") == date(2026, 5, 26)


def test_parse_target_date_rejects_non_iso_date():
    with pytest.raises(ValueError):
        parse_target_date("26/05/2026")
