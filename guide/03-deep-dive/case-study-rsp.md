# Case Study: RSP (S&P 500 Equal Weight ETF)

## The Fund

**Guggenheim S&P 500 Equal Weight ETF (RSP)**
- $9.5 billion in assets under management
- Tracks S&P 500 Equal Weight Index
- Each of 500 stocks weighted equally (~0.2% each)
- Contrast with SPY: market-cap weighted (top 10 stocks = ~30%)
- Designed to reduce concentration risk in mega-cap tech

**Normal Behavior:**
- Liquid, mainstream product
- Tight bid-ask spreads (typically 0.05-0.10%)
- Tracks index closely
- Widely held by institutional and retail investors

---

## August 24, 2015: Catastrophic Dislocation

**The Numbers:**
- **Closed August 23** at approximately **$76**
- **Low on August 24**: **$43.77**
- **Decline**: **-43%** (from close to intraday low)
- **Underlying equal-weight S&P 500 index decline**: **-4%**
- **iNAV (intraday indicative value)**: Never dropped below **$71**

**The Disconnect:**
- RSP traded at **$43.77** while fair value was **$71**
- **38% discount** to demonstrable intrinsic value
- Most underlying stocks declined only 3-5%
- Fund held appropriate securities, calculated NAV correctly
- Problem was market structure, not fund operations

---

## Timeline of RSP's Hour of Chaos

**9:30-9:35 AM:**
- Market opens with extreme volatility
- Many underlying S&P 500 stocks fail to open on time
- iNAV calculations rely on mix of current and stale prices
- RSP begins sharp decline

**9:31-10:30 AM:**
- **Experienced 10 separate LULD (Limit Up-Limit Down) halts**
- **Total actual trading time: 2.29 minutes** out of entire hour
- **Average trading window: 15-30 seconds** before next halt
- Each brief window saw violent price swings
- Insufficient time for rational price formation

**9:35 AM (approximate):**
- **Hit low of $43.77**
- 43% below previous close
- 38% below concurrent iNAV of $71
- Underlying index down only 4%

**9:40-10:15 AM:**
- More underlying stocks achieved price discovery
- iNAV calculations became more reliable
- Market makers cautiously returned
- RSP began snapping back toward fair value

**10:15 AM onward:**
- Price largely recovered to $71+ range
- Those who bought at $43.77 captured massive gains
- Those forced to sell suffered permanent losses

---

## Why the Dislocation Occurred

**1. iNAV Calculation Failure**
- Equal-weight index has 500 components
- On Aug 24, hundreds hadn't opened or were halted
- iNAV for unopened stocks = stale prices from 15-30 minutes earlier
- Mixed current prices (down 5-10%) with stale prices (down 0-2%)
- Result: iNAV showed $71 but accuracy highly questionable

**2. Hedging Impossibility**
- To arbitrage RSP at $43.77 vs $71 iNAV:
  - Buy RSP at $43.77
  - Short equal-weight basket of 500 stocks at $71 equivalent
  - Redeem RSP for basket at day's end
  - Cover short, capture spread
- **Problem: Can't short stocks that aren't trading**
- Many of the 500 components were halted
- "Arbitrage" without hedge = directional bet on unknown fair value

**3. Circuit Breaker Cascade**
- First LULD halt triggered quickly
- 5-minute trading pause
- Brief 15-30 second trading window
- Immediately hit band again
- Repeat 10 times in one hour
- No sustained price discovery possible

**4. Order Book Air Pockets**
- Market makers withdrew due to hedging impossibility
- Bid-ask spreads widened dramatically
- Order book had large gaps between bids
- Market sell orders fell through "air pockets"
- Each execution triggered more stop-losses
- Cascade effect accelerated decline

---

## The "Arbitrage" That Wasn't

**What Looked Like Opportunity:**
- RSP trading at $43.77
- iNAV showing $71
- Apparent **$27.23 profit per share** (38% return!)
- On 100,000 share position: **$2.7 million profit**
- Seemingly obvious arbitrage

**The Reality:**
- Is iNAV actually $71 or will it gap lower when stocks reopen?
- Can't hedge by shorting basket (stocks halted)
- Taking $4.4 million position in RSP at $43.77 unhedged
- If market falls another 10%, lose $440,000+
- If iNAV was stale and true value $50, "arbitrage" = $600,000 loss
- Unknown risk, not risk-free arbitrage

**Rational Market Maker Response:**
- Step away until can verify fair value
- Wait for underlying stocks to open and trade
- Preserve capital rather than speculate
- **Liquidity withdrawal made dislocation worse**

---

## Who Was Hurt

**Stop-Loss Order Victims:**
- Investors with stops at $70 (8% below close)
- Stops triggered, converted to market orders
- Executions at $50-55 range (30%+ below close)
- Far worse than intended 8% protection
- Positions liquidated permanently

**Forced Institutional Selling:**
- Risk management rules required liquidation at certain loss thresholds
- Drawdowns exceeded limits
- Forced sales into illiquid market
- Recovered shortly after, but forced sellers locked in losses

**Market-on-Open Orders:**
- Intended to execute at opening price (~$70-72 expected)
- Executed in $50-60 range due to dislocation
- 20-30% slippage from expected price

---

## Who Benefited

**Patient Capital:**
- Investors who recognized temporary dislocation
- Bought RSP at $43.77-$55 range
- Within hour, recovered to $71+
- 30-40% return in minutes
- Required nerve, available capital, and understanding of what was happening

**Selective Market Makers:**
- Sophisticated firms like Jane Street likely made selective trades
- Bought at extreme discounts when able to verify some underlying prices
- Used massive capital buffers to take measured risk
- Not "catching falling knives" but calculated positions
- Profited from others' panic and dysfunction

---

## What Made RSP Particularly Vulnerable

**Equal-Weighting Complexity:**
- 500 components (vs SPY which is cap-weighted)
- Each stock equally important (~0.2% weight)
- Requires pricing all 500 for accurate fair value
- If 200 stocks not opened, 40% of fair value calculation compromised
- More complex than cap-weighted where top 50 stocks = 50%+ of value

**Rebalancing Requirements:**
- Equal-weight requires quarterly rebalancing
- More trading than cap-weighted
- Slightly higher transaction costs
- But none of this explains 43% dislocation

**Size Not Protective:**
- $9.5 billion AUM (very large ETF)
- Should have deep liquidity
- Held mainstream S&P 500 stocks (not exotic)
- **Size provided zero protection when market structure broke**

---

## Lessons from RSP

**1. ETF Price ≠ Fair Value During Stress**
- Can trade 38% below intrinsic value
- Even for large, liquid, mainstream products
- Market structure failure, not fund failure

**2. iNAV Unreliable When Inputs Stale**
- Garbage in, garbage out
- Showing $71 doesn't mean $71 is accurate
- Market makers correctly didn't trust it

**3. Arbitrage Requires Hedging**
- Can't arbitrage without simultaneous hedge
- "Free money" at $43.77 was actually unhedgeable speculation
- Rational to pass when risk unknowable

**4. Circuit Breakers Can Amplify Problems**
- 10 halts in one hour
- Only 2.29 minutes of trading
- Prevented rather than enabled price discovery

**5. Liquidity is Voluntary and Fragile**
- Market makers withdrew when hedging impossible
- No obligation to provide liquidity during dysfunction
- "Deep liquidity" vanished in minutes

**6. Stop-Loss Orders Dangerous in Gaps**
- Triggered at $70, executed at $50
- Converted to market orders in worst possible environment
- No price protection when needed most

**7. Recovery Doesn't Help Forced Sellers**
- RSP recovered to $71 within hour
- But those who sold at $50 locked in losses
- Temporary dislocation created permanent wealth transfer

---

## Post-Event Analysis

**SEC Research:**
- Documented RSP as exemplar of dysfunction
- Used in regulatory reports and academic papers
- Symbol of how severe dislocations can be
- Evidence for need for market structure reform

**Aftermath for RSP:**
- Fund operations continued normally
- No changes to holdings or methodology
- Still tracks equal-weight S&P 500 index
- Investors more wary of market-on-open and stop-loss orders

**Question Raised:**
- If $9.5B mainstream S&P 500 ETF can dislocate 43%, what about smaller, less liquid products?
- If RSP vulnerable, is anything safe during extreme stress?
- Highlighted that ETF market structure itself was problem, not specific funds

---

**See also:**
- [NAV Disconnect](nav-disconnect.md)
- [Timeline](../02-the-event/timeline.md)
- [RSP Case Analysis Notebook](../../notebooks/04-rsp-case-analysis.ipynb)
