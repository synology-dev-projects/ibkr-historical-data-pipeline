import pytest
import pandas as pd
from unittest.mock import patch
from common_lib.config.history_req_config import HistoryReqConfig
from transform import run, _define_datatypes_df
from parse_args import parse_args


def test_define_datatypes_daily():
    h_config = HistoryReqConfig(
        symbol="SPY",
        exchange="NASDAQ",
        startDateStr="2026-02-18",
        endDateStr="2026-02-24",
        barSizeSetting="1 day"
    )
    raw_df = pd.DataFrame([
        {
            "date": "2026-02-18",
            "open": 500.0,
            "high": 505.0,
            "low": 499.0,
            "close": 504.0,
            "volume": 100000,
            "average": 502.0,
            "barCount": 1500
        }
    ])
    df = run(h_config, raw_df)
    assert "datetime" in df.columns
    assert "date" not in df.columns
    assert "wap" in df.columns
    assert df["symbol"].iloc[0] == "SPY"
    assert df["barsize"].iloc[0] == "1 day"
    assert pd.to_datetime("2026-02-18") == df["datetime"].iloc[0]


def test_define_datatypes_intraday():
    h_config = HistoryReqConfig(
        symbol="QQQ",
        exchange="NASDAQ",
        startDateStr="2026-02-18",
        endDateStr="2026-02-24",
        barSizeSetting="1 min"
    )
    raw_df = pd.DataFrame([
        {
            "date": "2026-02-18 09:30:00",
            "open": 400.0,
            "high": 401.0,
            "low": 399.5,
            "close": 400.5,
            "volume": 5000,
            "wap": 400.2,
            "barCount": 50
        }
    ])
    df = run(h_config, raw_df)
    assert "datetime" in df.columns
    assert df["symbol"].iloc[0] == "QQQ"
    assert pd.to_datetime("2026-02-18 09:30:00") == df["datetime"].iloc[0]


def test_parse_args_unit():
    test_cli_args = [
        "prog",
        "--symbol", "AAPL",
        "--exchange", "NASDAQ",
        "--startDateStr", "2026-01-01",
        "--endDateStr", "2026-01-05",
        "--barSizeSetting", "1 day"
    ]
    with patch("sys.argv", test_cli_args):
        h_config = parse_args()
        assert h_config.symbol == "AAPL"
        assert h_config.exchange == "NASDAQ"
        assert h_config.startDateStr == "2026-01-01"
        assert h_config.endDateStr == "2026-01-05"
        assert h_config.barSizeSetting == "1 day"
