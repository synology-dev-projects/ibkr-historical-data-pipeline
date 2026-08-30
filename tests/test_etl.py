import pytest
import load
import common_lib.connectors.postgres as postgres
import pandas as pd

pd.set_option('display.max_columns', None)

@pytest.mark.integration
def test_extract(env_config, pipeline_data):
    """
    """
    raw_df = pipeline_data["raw_df"]
    # print("\n")
    # print(raw_df)
    assert len(raw_df) > 0

@pytest.mark.integration
def test_transform(env_config, pipeline_data):
    """
    if input template found in post
    :return:
    """

    df = pipeline_data["clean_df"]
    # print("\n")
    # print(df)
    assert len(df) > 0


@pytest.mark.integration
def test_load(env_config, pipeline_data):
    """
    if input template found in post
    :return:
    """

    df = pipeline_data["clean_df"]
    start_dt = df['datetime'].min().strftime('%Y-%m-%d %H:%M:%S')
    end_dt = df['datetime'].max().strftime('%Y-%m-%d %H:%M:%S')
    load.run(env_config, df)
    sql_template = f"""
        SELECT * FROM ibkr_historical_te
        WHERE datetime >= '{start_dt}'
          AND datetime <= '{end_dt}'
        ORDER BY datetime ASC
        """
    pg_df = postgres.sql(env_config, sql_template)
    pg_df.columns = pg_df.columns.str.lower()

    pd.testing.assert_frame_equal(df, pg_df, check_like=True, check_dtype=False)


