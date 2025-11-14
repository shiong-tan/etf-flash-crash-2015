# Sample Data Files

This directory contains **sample/synthetic data** for educational purposes, based on publicly available information about the August 24, 2015 ETF flash crash.

## ⚠️ Important Notes

- **These are not real tick-by-tick market data files**
- Data is **synthesized** to illustrate the events described in SEC and academic reports
- Real historical market data requires Bloomberg, Refinitiv, or exchange data licenses
- Use this data for **learning and demonstration purposes only**

## Files

### `aug24_price_data.csv`

Simulated ETF and stock prices during the flash crash period (9:30 AM - 10:15 AM ET).

**Columns:**
- `timestamp`: Date and time (ET)
- `ticker`: Security symbol
- `type`: ETF or Stock
- `price`: Last trade price (shows "HALTED" during circuit breaker periods)
- `inav`: Indicative Net Asset Value (for ETFs)
- `volume`: Trade volume at that timestamp
- `bid`: Best bid price
- `ask`: Best ask price
- `spread_bps`: Bid-ask spread in basis points (100 bps = 1%)

**Key features demonstrated:**
- **RSP (Guggenheim S&P 500 Equal Weight)**: Crashes from $76.15 to $43.77 (low), recovers to $71.40
- **IVV vs SPY discrepancy**: IVV trades at $202-198 while SPY at $199-191 (dual pricing failure)
- **IUSV stop-loss example**: Falls to $87.32 (demonstrating 20%+ slippage)
- **Trading halts**: Shown as "HALTED" in price column
- **Spread widening**: Narrow spreads (50 bps) balloon to 2,000-4,500 bps during stress

**Data sources for synthesis:**
- SEC Market Access Alert (Aug 25, 2015) - halt counts and timing
- SEC Staff Report on August 24, 2015 - RSP specific data points
- FINRA review - retail execution examples
- Academic papers on the event

### `luld_halts.csv`

Simulated LULD (Limit Up-Limit Down) circuit breaker halts during the crash.

**Columns:**
- `ticker`: Security symbol
- `type`: ETF or Stock
- `halt_start`: Trading halt start time
- `halt_end`: Trading halt end time (5 minutes later per LULD)
- `duration_sec`: Halt duration in seconds (typically 300)
- `price_before`: Last price before halt triggered
- `price_after`: First price after halt lifted
- `reference_price`: LULD reference price used for band calculation
- `band_pct`: Band width percentage (5% regular, 10% open/close)
- `trigger_reason`: Why halt was triggered
- `halt_number`: Sequential halt number for that security (RSP had 10!)

**Key features demonstrated:**
- **1,278 halts across 471 securities** (sample subset shown)
- **RSP**: 10 separate halts between 9:33 AM - 10:33 AM
- **80% of halts were ETFs** not individual stocks
- **Post-halt price gaps**: Prices often moved significantly during 5-minute blackouts
- **Cascade effect**: Multiple securities halting in rapid succession

**Data sources for synthesis:**
- SEC Market Access Alert - total halt statistics
- LULD Halt data from consolidated tape (publicly available summary stats)
- SEC Staff Report on August 24, 2015
- Jane Street internal analysis (as described in public materials)

## Methodology

These datasets were created by:

1. **Starting with confirmed facts:**
   - RSP: Close $76, low $43.77, iNAV ~$71
   - IVV vs SPY: 349-point discrepancy reported
   - IUSV: Stop trigger ~$108.69, execution $87.32
   - Total: 1,278 halts, 471 securities, 302 ETFs triggered breakers

2. **Interpolating realistic intraday paths:**
   - Using volatility patterns typical of stressed markets
   - Ensuring LULD triggers occur at 5% bands
   - Modeling bid-ask spread widening during stress

3. **Adding market microstructure realism:**
   - Staggered stock openings (9:30-10:15 AM)
   - 5-minute halt durations per LULD rules
   - Reference price updates between halts
   - Post-halt price discontinuities

## Usage in Notebooks

```python
import pandas as pd

# Load price data
prices = pd.read_csv('assets/data/aug24_price_data.csv', parse_dates=['timestamp'])

# Filter to RSP crash
rsp = prices[prices['ticker'] == 'RSP'].copy()

# Calculate dislocation
rsp['dislocation_pct'] = (rsp['price'] - rsp['inav']) / rsp['inav'] * 100

# Load halt data
halts = pd.read_csv('assets/data/luld_halts.csv', parse_dates=['halt_start', 'halt_end'])

# Count halts per ticker
halt_counts = halts.groupby('ticker').size().sort_values(ascending=False)
```

## Real Data Sources

If you need actual historical market data for research:

- **Bloomberg Terminal**: LULD halt data, tick-by-tick prices
- **Refinitiv/LSEG**: Historical intraday data
- **SEC EDGAR**: Regulatory filings and reports
- **Academic datasets**: TAQ (Trade and Quote), CRSP
- **Exchange websites**: Limited free data from NYSE, Nasdaq

## References

1. SEC Market Access Alert (August 25, 2015) - [Link to SEC.gov](https://www.sec.gov)
2. SEC Staff Report: "Research Note on August 24, 2015 Market Volatility"
3. FINRA Regulatory Notice 15-33 (September 2015)
4. Academic: Madhavan, Sobczyk, Ang (2016) - "Toward a Better Understanding of the Events of August 24, 2015"
5. Jane Street public materials on market making and ETF structure

---

**For questions about this data or to report issues:** See main repository README.md
