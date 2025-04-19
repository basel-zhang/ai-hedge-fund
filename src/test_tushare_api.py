# -*- coding: utf-8 -*-
import os
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from data.models import Price
from tools.tushare_api import get_prices


@pytest.fixture
def mock_daily():
    """Fixture to create mock data for tushare API"""
    return pd.DataFrame(
        {
            "ts_code": ["000001.SZ", "000001.SZ", "000001.SZ"],
            "trade_date": ["20230101", "20230102", "20230103"],
            "open": [10.5, 11.2, 10.8],
            "high": [11.0, 11.5, 11.1],
            "low": [10.2, 10.9, 10.5],
            "close": [10.8, 11.3, 10.9],
            "vol": [1000000, 1200000, 900000],
        }
    )


@pytest.fixture
def mock_empty_daily():
    """Fixture to create empty mock data for tushare API"""
    return pd.DataFrame(
        {
            "ts_code": [],
            "trade_date": [],
            "open": [],
            "high": [],
            "low": [],
            "close": [],
            "vol": [],
        }
    )


@patch("tools.tushare_api.pro")
def test_get_prices(mock_pro, mock_daily):
    """Test the get_prices function from tushare_api"""
    # Configure the mock to return our test data
    mock_pro.daily.return_value = mock_daily

    # Call the function with test parameters
    ticker = "000001.SZ"
    start_date = "20230101"
    end_date = "20230103"
    result = get_prices(ticker, start_date, end_date)

    # Verify the function called tushare API correctly
    mock_pro.daily.assert_called_once_with(ts_code=ticker, start_date=start_date, end_date=end_date)

    # Verify the result structure
    assert len(result) == 3
    assert isinstance(result[0], Price)

    # Verify the data was transformed correctly
    assert result[0].time == "20230101"
    assert abs(result[0].open - 10.5) < 1e-10
    assert abs(result[0].high - 11.0) < 1e-10
    assert abs(result[0].low - 10.2) < 1e-10
    assert abs(result[0].close - 10.8) < 1e-10
    assert result[0].volume == 1000000

    # Check the last item
    assert result[2].time == "20230103"
    assert abs(result[2].close - 10.9) < 1e-10


@patch("tools.tushare_api.pro")
def test_get_prices_empty_response(mock_pro, mock_empty_daily):
    """Test the get_prices function when tushare API returns empty data"""
    # Configure the mock to return empty data
    mock_pro.daily.return_value = mock_empty_daily

    # Call the function with test parameters
    ticker = "000001.SZ"
    start_date = "20230101"
    end_date = "20230103"
    result = get_prices(ticker, start_date, end_date)

    # Verify the function called tushare API correctly
    mock_pro.daily.assert_called_once_with(ts_code=ticker, start_date=start_date, end_date=end_date)

    # Verify the result is an empty list
    assert isinstance(result, list)
    assert len(result) == 0
