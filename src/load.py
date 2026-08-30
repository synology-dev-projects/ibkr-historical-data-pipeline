import logging
import pandas as pd
import common_lib.connectors.postgres as postgres
from common_lib.config.main_config import MainConfig
import sys



def run(m_config: MainConfig, df: pd.DataFrame, write_mode: str = "upsert") -> None:
    table_name = "ibkr_historical_te"
    primary_keys = ["symbol", "datetime", "barsize"]

    if df.empty:
        logging.error("DataFrame is empty. Skipping DB push.")
        sys.exit(1)

    logging.info(f"Pushing {len(df)} rows to '{table_name}' with mode='{write_mode}'...")


    try:
        postgres.insert_into_table(
            config=m_config,
            df=df,
            table_name=table_name,
            write_mode=write_mode,
            primary_keys=primary_keys
        )

        logging.info("Load into PostgreSQL successful.")

    except Exception as e:
        logging.error(f"Failed to push to PostgreSQL: {e}")
        raise e




