# `ibkr-historical-data-pipeline`

An automated historical market data ingestion ETL pipeline that interfaces with Interactive Brokers (IB Gateway) via `common-lib`, fetches multi-timeframe OHLCV bar data, transforms and validates the series, and performs idempotent upserts into Oracle Database.

---

## 🏛️ Architecture & Modules

```
ibkr-historical-data-pipeline/
├── src/
│   ├── extract.py         # Connects to IB Gateway and extracts historical price bars
│   ├── transform.py       # Cleans OHLCV series, standardizes timestamps and bar counts
│   ├── load.py            # Persists cleaned market data into Oracle DB table ticker_data_ibkr
│   ├── parse_args.py      # CLI parameter parsing (tickers, duration, bar size, end date)
│   └── scripts/           # Scheduled execution entrypoints
├── tests/                 # Local & CI/CD test suite
├── Dockerfile             # Container build
└── README.md
```

---

## 🎯 Design Goals

1. **Idempotent Ingestion**:
   - Uses Oracle database `MERGE INTO` via `common-lib`'s `write_to_oracle_upsert` to guarantee duplicate-free bar insertion across repeated historical backfills.
2. **Reliable Gateway Connection**:
   - Manages connection lifecycle with local IB Gateway container (`gnzsnz-ib-gateway` on port `4001`), utilizing exponential backoffs on network throttling.
3. **Flexible CLI & Batch Interface**:
   - Supports ad-hoc historical backfilling and automated daily/hourly incremental cron updates.

---

## 🚀 Usage

Run data extraction via CLI:
```powershell
python src/scripts/run_pipeline.py --symbol AAPL --duration "7 D" --bar-size "1 hour"
```