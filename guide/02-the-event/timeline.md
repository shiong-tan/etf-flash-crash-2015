# Timeline of August 24, 2015

## Pre-Open (before 9:30 AM ET)

**Overnight and Global Markets:**
- Asian equity markets tumbled overnight
- European indices opened sharply lower
- Market anxiety elevated following China concerns
- Weekend order buildup created massive imbalances

**9:25 AM ET:**
- **E-Mini S&P 500 futures hit 5% limit down**
- Trading paused before U.S. equity markets even opened
- Ominous sign of extreme volatility ahead
- Futures provided no price discovery for market makers

**Pre-Open Positioning:**
- ETF market makers prepared for uncertain, volatile open
- Underlying stock liquidity thin in pre-market
- Bid-ask spreads already widening dramatically
- **NYSE invoked Rule 48**: Suspended requirement for pre-opening price indications
- Reduced transparency at worst possible moment

---

## 9:30-9:31 AM — Chaotic Open

**The Opening:**
- NYSE bell rings at 9:30 AM ET
- **Hundreds of individual stocks fail to open on time**
- Staggered openings prevented coherent price discovery
- SPY (SPDR S&P 500 ETF) immediately fell 5.2%

**Market Maker Response:**
- ETF market makers lacked component prices for fair value calculation
- iNAV calculations based on stale data from 15-30 minutes earlier
- Normal hedging tools unavailable (stocks not trading, futures at limit)
- Rational response: withdraw liquidity or quote extremely wide spreads

**Order Flow:**
- Retail market sell and stop-loss orders hit thin order books
- Many stop-losses triggered by distorted opening prints
- Massive order imbalances: far more sellers than buyers
- Each execution triggered more stop-losses at progressively lower levels

**First Wave of Halts:**
- **1,278 trading halts** would occur across **471 securities** in next hour
- **80% of halts were ETFs** (not individual stocks)
- Circuit breakers designed to calm markets instead created chaos

---

## 9:31-9:40 AM — Dislocations Emerge

**Extreme ETF Mispricing:**
- **RSP (S&P 500 Equal Weight ETF)**: Crashed from $76 to **$43.77 low** (43% decline)
  - Underlying equal-weight S&P 500 index fell only 4%
  - iNAV never dropped below $71
  - Traded at **38% discount** to demonstrable fair value

- **DVY (iShares Select Dividend ETF)**: Plunged 35% to $48
  - Combined weighted value of underlying stocks stood at $72.42
  - Underlying stocks down merely 2.7%

- **SPLV (PowerShares S&P 500 Low Volatility ETF)**: Dropped 46% from $36.90 to $20.00
  - Ironically marketed to risk-averse investors
  - Would be **halted 11 separate times** in one hour

- **IVV (iShares Core S&P 500 ETF, $65B AUM)**: Fell 26% intraday
  - S&P 500 index itself declined only 5.3%
  - At respective lows: SPY priced S&P 500 at 1,829, IVV at 1,480
  - **349-point discrepancy** on identical index (second occurrence)

**Limit Up/Limit Down Accelerates:**
- **78% of ETF circuit breaker triggers occurred in first 15 minutes**
- When bands widest (±10% during opening period)
- Rapid-fire halts: ETFs had 15-30 second trading windows before next halt
- RSP: **Only 2.29 minutes of actual trading** despite one hour period
- **10 separate LULD halts** for RSP alone

**Hedging Becomes Impossible:**
- Dozens of underlying stocks halted simultaneously
- Last traded prices 15-30 minutes old and demonstrably stale
- Market makers couldn't determine if iNAV at $71 was accurate or mirage
- Couldn't short stocks that weren't trading for delta hedge
- Apparent arbitrage (RSP $50 vs $71 iNAV) = unhedgeable directional bet

**Algorithmic Breakdown:**
- High-frequency trading systems detected pricing impossibilities
- Automated safety mechanisms shut down to prevent catastrophic losses
- ~50% of RSP trades flagged as Intermarket Sweep Orders (HFT signature)
- Single-share trades appeared frequently (humans don't trade one share)
- Broken algorithms dumping positions at any available price

---

## 9:40-10:15 AM — Stability Gradually Returns

**More Underlying Stocks Begin Trading:**
- Staggered opens continue but more stocks achieve price discovery
- iNAV calculations begin reflecting current rather than stale prices
- Fair value becomes calculable again

**Market Makers Cautiously Return:**
- Can hedge again with underlying stocks trading
- Fair value uncertainty decreases
- Begin providing liquidity with tighter spreads
- Still extremely cautious given ongoing volatility

**ETFs Snap Back Toward Fair Value:**
- Prices recover dramatically in minutes
- RSP rebounds from $43.77 toward $71+ levels
- Those who bought at lows captured massive gains
- Those forced to sell suffered permanent losses

**Circuit Breaker Halts Decrease:**
- Fewer new LULD triggers as volatility subsides
- Trading windows lengthen between halts
- Price discovery improves

---

## Afternoon — Damage Assessment

**Market Stabilizes:**
- By 10:15 AM most ETFs trading near fair value again
- Dislocations largely resolved
- Normal trading patterns resume

**Scope of Event:**
- **302 of 1,569 ETFs triggered circuit breakers** (19% of all ETFs)
- **1,278 total trading halts** in first hour
- Dow Jones had plunged over 1,000 points at low
- Most losses recovered by end of day, but damage done to forced sellers

**Investor Casualties:**
- Stop-loss orders executed 20-40% below trigger prices
- Protective mechanisms became instruments of destruction
- Conservative investors in "low volatility" products suffered extreme losses
- Many positions liquidated at worst possible moment, never to recover

---

## Aftermath — Post-Mortems Begin

**Immediate:**
- Exchanges and market participants begin analyzing what went wrong
- SEC announces investigation
- Industry debates responsibility and solutions

**December 2015:**
- **SEC Division of Economic and Risk Analysis publishes detailed research note**
- Documented scale of dislocations
- Analyzed contributing factors
- But minimal new regulations proposed

**2016:**
- **Amendment 10** (April): Modified LULD reference price calculations
- **Amendment 12** (September): Harmonized reopening procedures
- Rule 48 repealed
- But fundamental vulnerabilities remain

---

**See also:**
- [Pre-Crash Conditions](pre-crash-conditions.md)
- [Opening Chaos](opening-chaos.md)
- [RSP Case Study](../03-deep-dive/case-study-rsp.md)
- [Who Was Affected](who-was-affected.md)
