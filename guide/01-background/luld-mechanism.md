# Limit Up-Limit Down (LULD) Mechanism

## Purpose
- Implemented after May 6, 2010 flash crash
- Prevent trades far from recent prices
- Provide "cooling off" periods during volatility
- Replace older single-stock circuit breakers

## How LULD Works

**Price Bands**
- Upper and lower price limits around reference price
- Trading cannot occur outside bands
- Band width varies by security tier and time of day

**Tier 1 Securities** (S&P 500 stocks, large ETFs):
- **9:30-9:45 AM** (Opening): ±10% bands
- **9:45 AM-3:35 PM** (Regular trading): ±5% bands
- **3:35-4:00 PM** (Closing): ±10% bands

## Reference Price Calculation
- Based on 5-minute average of transaction prices
- Updates when price moves >1% from current reference
- **Critical flaw exposed Aug 24:**
  - If primary exchange can't open within 5 minutes, uses midpoint of national best bid/offer
  - With market makers withdrawn, bid-ask spreads widened to $10-20
  - Reference price based on midpoint bore no relationship to fair value
  - Example: $50 bid, $70 ask → $60 reference price, but true value $72

## Limit State and Trading Halts

**Limit State** (15 seconds):
- Triggered when national best bid or offer reaches band edge
- If price remains at band edge >15 seconds:
- Trading pauses across all exchanges for 5 minutes minimum

**Reopening Process:**
- Primary exchange conducts reopening auction
- Non-primary exchanges remain halted until primary reopens
- Different exchanges had different procedures on Aug 24 (fixed by Amendment 12)

## What Happened on August 24, 2015

**Scale of Halts:**
- **1,278 trading halts** across 471 securities in first hour
- **80% were ETFs** (not individual stocks)
- **78% of ETF halts** occurred in first 15 minutes when bands widest
- RSP: 10 separate halts, only 2.29 minutes of actual trading in one hour
- SPLV: 11 halts despite "low volatility" mandate

**Perverse Feedback Loop:**
1. Volatility triggers halt
2. 5-minute pause creates information vacuum
3. Pent-up uncertainty when trading resumes
4. Volatility immediately triggers another halt
5. Cycle repeats

**Failed Price Discovery:**
- No trading = no price discovery
- Reference prices became stale during halts
- 15-30 second trading windows between halts
- Insufficient time for rational price formation

## Why LULD Amplified the Crisis

**For Market Makers:**
- Couldn't hedge with halted underlying stocks
- Couldn't determine fair value without current prices
- Risk of being caught with large positions when halt triggered
- Rational response: withdraw liquidity entirely

**For Arbitrageurs:**
- Can't execute both legs of arbitrage when stocks halted
- Apparent opportunity (RSP at $50 vs $71 iNAV) = unhedgeable directional bet
- Circuit breakers made arbitrage impossible precisely when most needed

**For Investors:**
- Staggered halts across related securities created chaos
- IVV and SPY (both track S&P 500) showed 349-point discrepancy
- Many ETFs halted while underlying stocks traded
- Some stocks halted while ETFs traded

## Post-Crisis Improvements

**Amendment 10** (April 2016):
- Modified reference price calculation
- Use prior day's closing price instead of potentially wide midpoints
- Reduced garbage-in-garbage-out problem

**Amendment 12** (September 2016):
- Harmonized reopening procedures
- Non-primary markets must remain halted if primary can't reopen within 10 minutes
- Reduced coordination failures

**Rule 48** (repealed 2016):
- Previously suspended requirement for pre-opening price indications
- Reduced transparency at worst possible moment on Aug 24
- Now repealed to maintain information flow

## Fundamental Tension
- Circuit breakers **stop trading** but don't **create liquidity**
- They mask underlying problems rather than solving them
- When resumed, same conditions that caused halt often still exist
- LULD remains: Same vulnerabilities could recur

---

**See also:**
- [LULD from Market Maker View](../04-market-maker-perspective/luld-from-mm-view.md)
- [Opening Chaos](../02-the-event/opening-chaos.md)
- [LULD Calculator Notebook](../../notebooks/03-luld-calculator.ipynb)
