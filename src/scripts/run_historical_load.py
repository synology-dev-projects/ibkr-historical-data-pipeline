import logging
import sys

from parse_args import parse_args
import extract, transform, load
import common_lib.config.main_config as main_config
import common_lib.connectors.nfty as nfty

logger = logging.getLogger(__name__)


def main():
    m_config = main_config.load_config()
    try:
        h_config = parse_args()
        raw_df = extract.run(m_config, h_config)
        clean_df = transform.run(h_config, raw_df)
        load.run(m_config, clean_df)
        logging.info("IBKR historical load completed successfully.")
    except SystemExit:
        raise
    except Exception as e:
        error_msg = f"CRITICAL: run_historical_load.py failed with exception: {e}"
        logging.exception(error_msg)
        try:
            nfty.send_ntfy_notification(
                m_config.ntfy_endpoint,
                "quant_alerts",
                "🚨 PIPELINE FAILURE: IBKR Historical Load",
                error_msg,
                5
            )
        except Exception as alert_err:
            logging.error(f"Failed to dispatch error notification: {alert_err}")
        sys.exit(1)


if __name__ == "__main__":
    main()