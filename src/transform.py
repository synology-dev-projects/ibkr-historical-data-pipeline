import pandas as pd
from common_lib.config.history_req_config import HistoryReqConfig


def run(h_config: HistoryReqConfig, raw_df:pd.DataFrame):
    #verify the schema

    defined_types_df = _define_datatypes_df(h_config, raw_df)

    return defined_types_df



def _define_datatypes_df(h_config: HistoryReqConfig, df: pd.DataFrame) -> pd.DataFrame:
    """
    define datatypes properly
    """
    #apply lower case to everything
    df = df.rename(columns=str.lower)

    #apply string first
    df["symbol"] = h_config.symbol
    df["symbol"] = df["symbol"].astype("string")
    df["barsize"] = h_config.barSizeSetting
    df["barsize"] = df["barsize"].astype("string")

    #idapi version > 9.0 renamed to average to wap. Code to account for both versions
    if 'average' in df.columns:
        df = df.rename(columns={'average': 'wap'})

    #apply date columns
    if h_config.barSizeSetting == "1 day":
        df["datetime"] = df["date"].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
    else:
        df["datetime"] = df["date"].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d %H:%M:%S'))
    df = df.drop(columns=['date'])

    # assume numeric to all other columns
    col_list = [c for c in df.columns[df.dtypes == 'object']]
    for column in col_list:
        df[column] = df[column].apply(lambda x: pd.to_numeric(str(x)))

    return df