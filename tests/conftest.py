# tests/conftest.py
import pytest
import extract, transform
import logging
import common_lib.config.main_config as config
from common_lib.config.history_req_config import HistoryReqConfig


@pytest.fixture(scope="session")
def env_config():
    """Load config once for the whole session."""
    return config.load_config()


@pytest.fixture(scope="session")
def pipeline_data(env_config):
    """
    Runs the expensive pipeline ONCE and returns a dictionary
    containing all intermediate dataframes/variables.
    """
    logging.info("\n[Setup] Running expensive pipeline extraction...")
    h_config = HistoryReqConfig(symbol="SPY"
                                ,exchange="NASDAQ"
                                ,startDateStr="2026-02-18"
                                ,endDateStr="2026-02-24")
    raw_df = extract.run(env_config, h_config)
    clean_df = transform.run(h_config, raw_df)


    # 2. Return EVERYTHING in a dictionary
    return {
        "hist_req_config": h_config,
        "raw_df": raw_df,
        "clean_df": clean_df
    }