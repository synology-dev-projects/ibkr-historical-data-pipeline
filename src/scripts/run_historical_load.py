import sys

from parse_args import parse_args
import extract, transform, load
import common_lib.config.main_config as main_config

def main():

   m_config = main_config.load_config()
   h_config = parse_args()

   raw_df = extract.run(m_config, h_config)
   clean_df = transform.run(h_config, raw_df)
   load.run(m_config,clean_df)


if __name__ == "__main__":
    main()