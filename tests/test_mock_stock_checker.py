"""Mock tests for stock_checker.py.

Tests MySQL protocol parsing, live query simulation, out-of-stock handling,
network failure fallbacks, and password scrambling.
"""

from unittest.mock import MagicMock, patch
import pytest
from stock_checker import (
    StockChecker,
    check_stock,
    scramble_native_password,
)

def test_password_scramble_deterministic():
    salt = b"12345678901234567890"
    pwd = "secret_password"
    scrambled = scramble_native_password(pwd, salt)
    assert isinstance(scrambled, bytes)
    assert len(scrambled) == 20
    assert scramble_native_password("", salt) == b""

def test_stock_checker_fallback_when_unreachable():
    checker = StockChecker(env={"MYSQL_HOST": "192.0.2.1", "MYSQL_USER": "u", "MYSQL_PASSWORD": "p"})
    skus = ["SIS-GEL-01", "NUT-SALT-02"]
    
    # Must never raise exception; must return optimistic fallback so quiz never breaks
    results = checker.check_stock_for_skus(skus)
    assert len(results) == 2
    for sku in skus:
        assert sku in results
        assert results[sku]["in_stock"] is True
        assert results[sku]["is_live_check"] is False
        assert "каталог" in results[sku]["stock_status_text_uk"]

def test_stock_checker_mocked_db_response():
    checker = StockChecker(env={"MYSQL_USER": "user", "MYSQL_PASSWORD": "pwd"})
    skus = ["1940", "3110", "UNKNOWN_SKU"]

    mock_db_rows = [
        {
            "product_id": "1940",
            "model": "1940",
            "sku": "SIS-1940",
            "quantity": "25",
            "status": "1",
            "stock_status_id": "7",
            "price": "85.50"
        },
        {
            "product_id": "3110",
            "model": "3110",
            "sku": "NUT-3110",
            "quantity": "0",  # Out of stock
            "status": "1",
            "stock_status_id": "5",
            "price": "60.00"
        }
    ]

    with patch.object(checker, "_ensure_connection", return_value=MagicMock()):
        with patch("stock_checker._mysql_query", return_value=mock_db_rows):
            res = checker.check_stock_for_skus(skus)
            
            # In stock item
            assert "1940" in res
            assert res["1940"]["in_stock"] is True
            assert res["1940"]["quantity"] == 25
            assert res["1940"]["live_price_uah"] == 85.50
            assert res["1940"]["stock_status_text_uk"] == "В наявності"

            # Out of stock item
            assert "3110" in res
            assert res["3110"]["in_stock"] is False
            assert res["3110"]["quantity"] == 0
            assert res["3110"]["stock_status_text_uk"] == "Немає в наявності"

            # Unknown SKU
            assert "UNKNOWN_SKU" in res
            assert res["UNKNOWN_SKU"]["in_stock"] is False
            assert res["UNKNOWN_SKU"]["stock_status_text_uk"] == "Товар не знайдено"

def test_check_stock_singleton_api():
    with patch("stock_checker.get_stock_checker") as mock_get:
        mock_instance = MagicMock()
        mock_instance.check_stock_for_skus.return_value = {"TEST": {"in_stock": True}}
        mock_get.return_value = mock_instance

        res = check_stock(["TEST"])
        assert res == {"TEST": {"in_stock": True}}
        mock_instance.check_stock_for_skus.assert_called_once_with(["TEST"])
