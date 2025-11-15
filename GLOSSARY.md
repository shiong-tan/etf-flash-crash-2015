# Glossary of Terms

**ETF Flash Crash 2015 Educational Project**

This glossary defines financial, technical, and market structure terms used throughout the repository.

---

## Table of Contents

- [ETF and Market Structure](#etf-and-market-structure)
- [Market Microstructure](#market-microstructure)
- [Trading and Execution](#trading-and-execution)
- [Risk and Quantitative Metrics](#risk-and-quantitative-metrics)
- [Regulatory and Circuit Breakers](#regulatory-and-circuit-breakers)
- [Technical Implementation](#technical-implementation)

---

## ETF and Market Structure

### ETF (Exchange-Traded Fund)
An investment fund that trades on stock exchanges, similar to individual stocks. ETFs hold a basket of underlying securities (stocks, bonds, commodities) and their price tracks the net asset value of those holdings.

**Example**: SPY holds shares of all 500 companies in the S&P 500 index.

### NAV (Net Asset Value)
The total value of an ETF's underlying holdings divided by the number of shares outstanding. This is the "true" or "fair" value of the ETF.

**Formula**: `NAV = (Sum of holdings values) / Shares outstanding`

**Example**: If an ETF holds $100M in stocks and has 1M shares outstanding, NAV = $100 per share.

### iNAV (Indicative Net Asset Value)
A real-time estimate of NAV published every 15 seconds during trading hours. Used by traders to determine whether an ETF is trading at a premium or discount to fair value.

**Critical Issue on Aug 24, 2015**: When underlying stocks were halted, iNAV became stale and unreliable, breaking the arbitrage mechanism.

### Creation Unit
The minimum block size for creating or redeeming ETF shares, typically 50,000 shares. Only Authorized Participants can create/redeem in these blocks.

**Purpose**: Allows arbitrageurs to keep ETF prices aligned with NAV through the creation/redemption mechanism.

### Authorized Participant (AP)
Large financial institutions (typically market makers or broker-dealers) authorized to create and redeem ETF shares directly with the issuer. They perform the arbitrage that keeps ETF prices aligned with NAV.

**Examples**: Jane Street, Citadel Securities, Virtu Financial

### Arbitrage Spread
The difference between the ETF market price and its NAV/iNAV, representing potential profit for arbitrageurs.

**Formula**: `Spread % = ((ETF Price - iNAV) / iNAV) × 100`

**Normal Range**: ±0.05% to ±0.25%
**Aug 24, 2015**: Spreads reached 30-40% for some ETFs

### Premium
When an ETF trades above its NAV. Signals that arbitrageurs should **create** new shares (buy underlying basket, deliver to issuer, receive ETF shares, sell ETF shares).

### Discount
When an ETF trades below its NAV. Signals that arbitrageurs should **redeem** shares (buy ETF shares, deliver to issuer, receive underlying basket, sell basket).

---

## Market Microstructure

### Order Book
A ledger showing all outstanding buy (bid) and sell (ask) orders at various price levels. The order book represents available liquidity at each price.

**Structure**:
```
ASKS (Sell Orders)
$100.05 → 500 shares
$100.04 → 1,000 shares
$100.03 → 2,000 shares
-----------------
$100.00 → 1,500 shares (BID)
$99.99  → 2,500 shares
$99.98  → 3,000 shares
BIDS (Buy Orders)
```

### Bid-Ask Spread
The difference between the best (highest) bid price and the best (lowest) ask price.

**Formula**: `Spread = Best Ask - Best Bid`

**Basis Points**: `Spread (bps) = (Spread / Midpoint) × 10,000`

**Normal**: 1-5 basis points for liquid ETFs
**Aug 24, 2015**: 200-4,500 basis points during crash

### Market Order
An order to buy or sell immediately at the best available price. Guarantees execution but not price.

**Risk**: During flash crash, market orders executed at catastrophically bad prices due to sparse order books.

**Example**: Market sell of 1,000 shares might execute at $100, $99.50, and $98 if order book is thin.

### Limit Order
An order that specifies the worst acceptable price. Provides price protection but may not execute.

**Example**: "Buy 1,000 shares at $100 or better" - won't pay more than $100, but might not fill if price rises.

### Stop-Loss Order
An order that becomes a market order when a trigger price is reached. Designed to limit losses, but can result in execution far below the trigger during volatile markets.

**Aug 24, 2015 Problem**: Stop at $108.69 executed at $87.32 (20% worse than trigger) due to order book gaps.

### Liquidity
The ability to buy or sell without significantly moving the price. Measured by:
- Bid-ask spread (tighter = more liquid)
- Order book depth (more shares = more liquid)
- Price impact (less impact = more liquid)

### Air Pocket / Liquidity Gap
A price range with no bids or offers in the order book. Market orders "fall through" these gaps, causing dramatic price moves.

**Aug 24, 2015**: Many ETFs had 5-10% gaps in their order books.

### Price Impact
The change in price caused by executing a trade. Larger orders have greater price impact.

**Kyle's Lambda (λ)**: Coefficient measuring price impact per unit of order flow
- Higher λ = less liquid market
- Aug 24 saw λ increase 40-50x

### Market Maker
A firm that continuously provides both buy and sell quotes, profiting from the bid-ask spread while providing liquidity to the market.

**Revenue**: Bid-ask spread capture
**Cost**: Inventory risk, adverse selection
**Aug 24, 2015**: Many withdrew due to inability to hedge

---

## Trading and Execution

### VWAP (Volume-Weighted Average Price)
The average price weighted by volume traded at each price level. Used to measure execution quality.

### Slippage
The difference between expected execution price and actual execution price.

**Aug 24, 2015**: Stop-loss orders experienced 20-30% slippage.

### Adverse Selection
When informed traders take the opposite side of market maker quotes, causing losses. Market makers widen spreads when adverse selection risk is high.

### Quote Skewing
Market makers adjust bid/ask quotes based on inventory position. If long (holding inventory), they lower both bid and ask to encourage selling.

**Purpose**: Reduce inventory risk by incentivizing mean reversion.

---

## Risk and Quantitative Metrics

### VaR (Value at Risk)
Statistical measure of potential loss at a given confidence level.

**Example**: 99% VaR of $100,000 means there's a 1% chance of losing more than $100,000.

**Formula**: `VaR = Position Value × Volatility × Z-score`

### Expected Shortfall (ES) / CVaR
Average loss in the worst X% of outcomes. More conservative than VaR.

**Example**: If 99% VaR = $100K, ES might be $150K (average of worst 1% of outcomes).

### Kyle's Lambda (λ)
Price impact coefficient from Kyle (1985) market microstructure model.

**Formula**: `λ = dP / dQ` (price change per unit of signed order flow)

**Interpretation**: How many dollars price moves per 1,000 shares traded

**Normal**: λ ≈ 0.0001 (1 cent per 1,000 shares)
**Aug 24, 2015**: λ ≈ 0.005 (50 cents per 1,000 shares)

### Amihud Illiquidity Measure
Captures price movement per dollar of trading volume.

**Formula**: `Amihud = Mean(|Return| / Dollar Volume)`

**Interpretation**: Higher values = less liquid market

### Delta
Directional market exposure. For market makers, net delta should be close to zero (hedged).

**Example**: Long 1,000 shares SPY, short 1,000 shares basket → Net delta ≈ 0

### Gamma
Sensitivity of delta to price changes. High gamma positions have unstable hedges.

**Market Maker Risk**: Large gamma during volatile markets makes hedging difficult.

---

## Regulatory and Circuit Breakers

### LULD (Limit Up-Limit Down)
Circuit breaker system that halts trading when prices move beyond specified percentage bands from a reference price.

**Standard Bands**: ±5% from reference price (wider during open/close)
**Duration**: 5-minute trading pause if breached

**Aug 24, 2015**: 1,278 LULD halts across 471 securities (80% were ETFs)

### Reference Price
The price used to calculate LULD bands. Updates periodically during trading.

**Problem**: Reference price can become stale during volatile markets, causing bands to be incorrectly positioned.

### Trading Halt
Temporary suspension of trading in a security, imposed by exchanges.

**Reasons**:
- LULD band breach
- Regulatory news pending
- Market disruption

**Aug 24, 2015**: Cascading halts prevented arbitrage and price discovery.

### Stale Price
A price that doesn't reflect current market conditions, typically due to lack of recent trading (e.g., halted security).

**Aug 24, 2015**: iNAV calculations used stale prices for halted stocks, making iNAV unreliable.

---

## Technical Implementation

### Order Book Snapshot
A point-in-time view of the order book, capturing bids, asks, and market state.

**Implementation**: `OrderBookSnapshot` class in `src/order_book_dynamics.py`

### Market Simulation
Computational model of market dynamics used to understand behavior under different conditions.

**Modules**:
- `order_book.py`: Basic order book mechanics
- `order_book_dynamics.py`: Advanced flash crash simulation
- `market_maker_pnl.py`: Market maker P&L modeling

### Synthetic Data
Artificially generated data based on known facts, used when real historical data is unavailable.

**This Repository**: Uses synthetic data calibrated to August 24, 2015 events for educational purposes.

### Time Series
Data points indexed by time, such as minute-by-minute prices.

**Format**: Pandas DataFrame with datetime index

### Basis Points (bps)
1/100th of 1%. Used to express spreads, fees, and returns.

**Examples**:
- 1 bp = 0.01%
- 100 bps = 1%
- 10,000 bps = 100%

---

## Acronyms Quick Reference

| Acronym | Full Term | Definition |
|---------|-----------|------------|
| ETF | Exchange-Traded Fund | Pooled investment security that trades on exchanges |
| NAV | Net Asset Value | True value of fund's holdings |
| iNAV | Indicative Net Asset Value | Real-time NAV estimate |
| AP | Authorized Participant | Institution authorized to create/redeem ETF shares |
| LULD | Limit Up-Limit Down | Circuit breaker system |
| VaR | Value at Risk | Statistical loss measure |
| ES | Expected Shortfall | Conditional VaR |
| VWAP | Volume-Weighted Average Price | Execution benchmark |
| bps | Basis Points | 1/100th of 1% |
| P&L | Profit and Loss | Financial performance |
| OHLC | Open-High-Low-Close | Price bar data |
| SEC | Securities and Exchange Commission | U.S. financial regulator |

---

## Additional Resources

### Academic Papers
- Kyle, A.S. (1985) - Continuous Auctions and Insider Trading
- Amihud, Y. (2002) - Illiquidity and Stock Returns
- Hasbrouck, J. (2007) - Empirical Market Microstructure

### Regulatory Reports
- SEC Staff Report on August 24, 2015
- FINRA Regulatory Notice 15-33
- SEC Market Access Alert (August 25, 2015)

### Industry Sources
- Jane Street ETF market making materials
- BlackRock ETF education resources
- CFA Institute ETF research

---

*For implementation details, see [ARCHITECTURE.md](ARCHITECTURE.md)*

*Last updated: November 2024*
