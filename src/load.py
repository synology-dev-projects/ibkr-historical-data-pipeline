import logging
import pandas as pd
import common_lib.connectors.oracle as oracle
from common_lib.config.main_config import MainConfig
import sys



def run(m_config: MainConfig, df: pd.DataFrame, write_mode: str = "upsert") -> None:
    table_name = m_config.oracle_ibkr_ticker_table_name
    primary_keys = oracle.get_table_metadata(m_config,table_name).get("primary_keys", [])

    if df.empty:
        logging.error("DataFrame is empty. Skipping DB push.")
        sys.exit(1)

    logging.info(f"Pushing {len(df)} rows to '{table_name}' with mode='{write_mode}'...")


    try:
        oracle.insert_into_table(
            config=m_config,
            df=df,
            table_name=table_name,
            write_mode=write_mode,
            primary_keys=primary_keys
        )

        logging.info("Load into oracle successful.")

    except Exception as e:
        logging.error(f"Failed to push to Oracle: {e}")
        raise e




