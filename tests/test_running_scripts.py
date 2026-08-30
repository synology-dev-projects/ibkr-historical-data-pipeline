
import sys
import pytest
from unittest.mock import patch

@pytest.mark.integration
def test_historical_load(env_config, pipeline_data):
    """
    Integration test: Runs historical load script against active IBKR Gateway socket.
    """
    try:
        import scripts.run_historical_load as calling_script
    except ImportError as e:
        pytest.skip(f"IBKR dependencies not installed: {e}")

    test_args = ["run_historical_load.py", "--symbol", "SPY", "--exchange", "NASDAQ", "--startDateStr", "2026-02-18", "--endDateStr", "2026-02-24"]

    with patch.object(sys, 'argv', test_args):
        calling_script.main()


