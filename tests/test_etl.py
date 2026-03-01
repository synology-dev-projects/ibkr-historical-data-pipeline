import load
import common_lib.connectors.oracle as oracle
import pandas as pd

pd.set_option('display.max_columns', None)
def test_extract(env_config, pipeline_data):
    """
    """
    raw_df = pipeline_data["raw_df"]
    # print("\n")
    # print(raw_df)
    assert len(raw_df) > 0

def test_transform(env_config, pipeline_data):
    """
    if input template found in post
    :return:
    """

    df = pipeline_data["clean_df"]
    # print("\n")
    # print(df)
    assert len(df) > 0


def test_load(env_config, pipeline_data):
    """
    if input template found in post
    :return:
    """

    df = pipeline_data["clean_df"]
    start_dt = df['datetime'].min().strftime('%Y-%m-%d %H:%M:%S')
    end_dt = df['datetime'].max().strftime('%Y-%m-%d %H:%M:%S')
    load.run(env_config,df)
    sql_template = f"""
        SELECT * FROM {env_config.oracle_ibkr_ticker_table_name}
        WHERE DATETIME >= TO_DATE('{start_dt}', 'YYYY-MM-DD HH24:MI:SS')
          AND DATETIME <= TO_DATE('{end_dt}', 'YYYY-MM-DD HH24:MI:SS')
        ORDER BY DATETIME ASC
        """
    oracle_df = oracle.sql(env_config, sql_template)
    oracle_df.columns = oracle_df.columns.str.lower()

    pd.testing.assert_frame_equal(df, oracle_df, check_like=True, check_dtype=False)

