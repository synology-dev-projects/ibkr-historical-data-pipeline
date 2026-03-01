
import sys
import scripts.run_historical_load as calling_script
from unittest.mock import patch

def test_historical_load(env_config, pipeline_data):
    """
    Verifies that the .env file exists and that Pydantic reads it correctly.
    """

    test_args = ["run_historical_load.py", "--symbol", "SPY", "--exchange", "NASDAQ","--startDateStr","2026-02-18","--endDateStr", "2026-02-24"]

    with patch.object(sys, 'argv', test_args):

        calling_script.main()


