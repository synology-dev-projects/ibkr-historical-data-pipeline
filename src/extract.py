import common_lib.connectors.ibkr as ibkr
from common_lib.config.main_config import MainConfig
from common_lib.config.history_req_config import HistoryReqConfig

import pandas as pd

def run(m_config: MainConfig,
        h_config: HistoryReqConfig)-> pd.DataFrame:

    return ibkr.extract_ibkr_ticker_data(m_config, h_config)





