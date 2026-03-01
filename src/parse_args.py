import argparse
from common_lib.config.history_req_config import HistoryReqConfig

def parse_args() -> HistoryReqConfig :
    parser = argparse.ArgumentParser(description="Ticker Data Processor")

    # We set required=True so the script fails if the user omits any flag
    #It is important the arguments must match order of load_ibkr_data function
    parser.add_argument("--symbol", required=True, type=str, help="Asset Symbol")
    parser.add_argument("--exchange", required=True, type=str, help="Exchange Name")
    parser.add_argument("--startDateStr", required=True, type=str, help="Start Date (yyyy-MM-dd)")
    parser.add_argument("--endDateStr", required=True, type=str, help="End Date (yyyy-MM-dd)")
    parser.add_argument("--barSizeSetting", required=False, type=str, help="Bar Size")
    parser.add_argument("--whatToShow", required=False, type=str, help="Data Type")
    parser.add_argument("--useRTH", required=False, type=bool, help="Regular Trading Hours (True or False)")
    parser.add_argument("--currency", required=False, type=str, help="Currency")

    # This creates the object with dot-notation attributes
    args = parser.parse_args()

    # Get the list of field names that TradeConfig actually accepts
    valid_keys = HistoryReqConfig.__annotations__.keys()

    # Filter the argparse dictionary:
    # Keep only keys that exist in TradeConfig AND are not None
    clean_params = {
        k: v for k, v in vars(args).items()
        if k in valid_keys and v is not None
    }

    # Create the object safely
    h_config = HistoryReqConfig(**clean_params)


    return h_config
