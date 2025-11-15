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

### The 15-Second Trigger Threshold

A critical but often overlooked detail: LULD does **not** immediately trigger a 5-minute halt when a stock touches a price band.

**The Two-Stage Process** (per SEC Release No. 34-67091):

1. **Limit State Entered**: Stock price reaches upper or lower band
2. **15-Second Window**: Trading centers have 15 seconds to clear the Limit State
3. **Two Possible Outcomes**:
   - **Cured within 15 seconds**: If quotes at the band are canceled or executed, the SIPs immediately publish new Reference Price and bands, trading continues
   - **Persists for 15 seconds**: If Limit State continues for full 15 seconds, a 5-minute trading pause triggers across all exchanges

**Why This Matters for August 24:**

During normal markets, the 15-second window often allows prices to self-correct without triggering halts. But on August 24, 2015:

- Markets were moving so violently that Limit States couldn't be cured
- Sellers kept hitting bids, buyers kept lifting offers
- Each 15-second countdown resulted in a halt
- This created the cascade: **1,278 trading halts** in the first hour

**Example - RSP Timeline:**
```
9:35:12 AM  Hits lower band at $69.12
9:35:13-27  Limit State persists (orders keep hitting band)
9:35:27 AM  15 seconds elapsed → 5-minute halt triggered
9:40:27 AM  Reopens, immediately gaps down
9:40:42 AM  Hits band again → Limit State
9:40:57 AM  Another halt (15 seconds later)
```

This explains why RSP had **10 separate halts** but only **2.29 minutes of actual trading** in the first hour.

### Opening Period Vulnerability (9:30-9:35 AM)

The opening period has a critical regulatory gap that amplified the August 24 crisis.

**The Rule** (FINRA Rule 6190):

If the primary exchange (typically NYSE, NYSE Arca, or Nasdaq) has not opened a stock or ETP by **9:35 AM**, other trading venues (BATS, EDGX, IEX, etc.) can trade it **without LULD price bands**.

**What This Means:**

- Between 9:30:00 and 9:35:00 AM: No price protection if primary hasn't opened
- Reference Price hasn't been established yet
- Trading can occur at any price on secondary venues
- No bands, no Limit States, no circuit breakers

**August 24, 2015 Timeline:**

| Time        | Event                                                         |
|-------------|---------------------------------------------------------------|
| 9:30:00 AM  | Markets open, massive sell pressure from overnight Asia fears|
| 9:30-9:33   | **Hundreds of stocks can't open on NYSE** (order imbalances) |
| 9:31-9:35   | **ETFs start trading on BATS/EDGX** without underlying stocks open |
| 9:31-9:35   | **No LULD protection** - secondary venues trading without bands |
| 9:35+       | Primary exchanges finally open, LULD bands activated          |
| 9:35+       | **Damage already done** - prices severely dislocated          |

**Why ETFs Were Especially Vulnerable:**

Market makers faced an impossible situation:

1. **Can't calculate fair value**: iNAV requires current prices for all components
2. **60% of components halted**: No way to price DVY when 60% of holdings aren't trading
3. **Can't hedge positions**: Can't buy/sell halted stocks to offset ETF positions
4. **But must decide**: Quote the ETF anyway? At what price?
5. **Rational response**: Withdraw completely or quote with massive spreads ($50 bid, $70 ask)
6. **Result**: ETFs trade at arbitrary prices with no arbitrage enforcement

**Real Example - DVY:**

```
9:31 AM: DVY starts trading on BATS
- 60% of DVY's component stocks: halted on NYSE
- iNAV shows $75.50 (using stale pre-market prices)
- Bid: $50 (no market makers willing to buy)
- Ask: $70 (no market makers willing to sell)
- First trade executes: $62 (-17.8% from stale iNAV)
- No LULD protection yet - primary exchange not open
```

By the time NYSE Arca opened DVY at 9:33 AM and LULD bands activated, the price had already dislocated to levels that immediately triggered halts.

**Post-Crisis Note:**

This vulnerability still exists in current regulations. The 9:30-9:35 window remains a critical risk period during highly volatile openings.

### Precise Band Percentages and Time-of-Day Adjustments

LULD bands are not fixed - they vary by **security tier**, **price level**, and **time of day**.

**Band Percentages by Tier and Price** (SEC Release No. 34-67091):

| Price Range     | Tier 1 (S&P 500, Russell 1000, Select ETPs) | Tier 2 (All Other NMS) |
|-----------------|---------------------------------------------|------------------------|
| **Above $3**    | **5%**                                      | **10%**                |
| **$0.75 - $3**  | **20%**                                     | **20%**                |
| **Below $0.75** | **75% or $0.15** (whichever is less restrictive) | **75% or $0.15** |

**Time-of-Day Multiplier** (FINRA Rule 6190):

LULD bands are **DOUBLED** during two periods:

1. **Opening Period**: 9:30 AM - 9:45 AM (first 15 minutes)
2. **Closing Period**: 3:35 PM - 4:00 PM (last 25 minutes)

**Why Bands Are Doubled:**

These periods naturally have higher volatility due to:
- Opening: Overnight news, order imbalances, price discovery
- Closing: Index rebalancing, fund redemptions, closing auctions

Regulators widened bands to prevent halts from normal end-of-day volatility.

**Impact Table - Tier 1 Stock Above $3:**

| Time Period              | Normal Band | Actual Band (if opened/closing) |
|--------------------------|-------------|----------------------------------|
| 9:30 - 9:45 AM (Opening) | 5%          | **10%** (doubled)                |
| 9:45 AM - 3:35 PM        | 5%          | **5%** (normal)                  |
| 3:35 - 4:00 PM (Closing) | 5%          | **10%** (doubled)                |

**Leveraged ETP Adjustment:**

For leveraged ETPs (2x, 3x, inverse), bands are multiplied by the leverage factor:

- 2x S&P 500 ETP: 5% × 2 = **10% bands** (normal hours)
- 3x S&P 500 ETP during opening: 5% × 2 (opening) × 3 (leverage) = **30% bands**

**August 24 Timing Was Worst-Case Scenario:**

The crash occurred primarily between **9:30-10:00 AM**, when:

1. **Bands were at their WIDEST** (opening period = doubled)
2. **Volatility was at HIGHEST** (overnight panic)
3. **Coordination was at WORST** (staggered openings)

**DVY Example:**

| Time    | Period  | Band % | Lower Band | Upper Band | Actual Price | Status  |
|---------|---------|--------|------------|------------|--------------|---------|
| 9:31 AM | Opening | 10%    | $67.95     | $83.05     | $72.15       | Trading |
| 9:33 AM | Opening | 10%    | $67.95     | $83.05     | $65.20       | HALT #1 |
| 9:38 AM | Opening | 10%    | (new ref)  | (new ref)  | $58.00       | Reopen  |
| 9:45 AM | Normal  | 5%     | (new ref)  | (new ref)  | $49.14       | LOW     |

**Key Insight:**

The doubled opening-period bands **allowed ETFs to fall further** before triggering halts. While intended to prevent nuisance halts from normal opening volatility, this timing:

- Let DVY fall 10% (vs 5% normally) before first halt
- Created larger gaps when halts finally triggered
- Triggered more severe stop-loss cascades
- Made recovery more difficult

If the crash had occurred at 10:00 AM (normal 5% bands), halts might have triggered earlier, potentially limiting the cascade. The timing at 9:30-9:45 AM with doubled bands was the worst possible scenario.

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
