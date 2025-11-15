# IVV vs SPY: Same Index, Different Flash Crash

## Overview

SPY and IVV both track the S&P 500 Index. Same 500 stocks, similar weights, nearly identical holdings. Yet on August 24, 2015, they experienced dramatically different trading patterns. This comparison reveals how **ETF-specific factors** (liquidity, market maker relationships, investor base) matter as much as underlying holdings during market stress.

---

## The Two Funds

### SPY (SPDR S&P 500 ETF Trust)

**Profile:**
- **Launched**: 1993 (first U.S. ETF ever)
- **Issuer**: State Street Global Advisors
- **AUM (Aug 2015)**: $185 billion
- **Average Daily Volume**: 85 million shares ($16 billion/day)
- **Expense Ratio**: 0.09%
- **Status**: Most liquid security in the world

**Market Structure:**
- 50+ market makers actively quoting
- Institutional arbitrage infrastructure
- Futures markets for S&P 500 (deep hedging options)
- Decades of operational history
- Ultra-tight bid-ask spreads (often $0.01 = 0.0005%)

### IVV (iShares Core S&P 500 ETF)

**Profile:**
- **Launched**: 2000
- **Issuer**: BlackRock (iShares)
- **AUM (Aug 2015)**: $73 billion
- **Average Daily Volume**: 3.5 million shares ($650 million/day)
- **Expense Ratio**: 0.07% (lower than SPY)
- **Status**: Second-largest S&P 500 ETF

**Market Structure:**
- 15-20 market makers (fewer than SPY)
- Less institutional arbitrage activity
- Same underlying index and hedge instruments as SPY
- Lower trading volumes = slightly wider spreads in normal times
- Still highly liquid in absolute terms

**Key Similarity**: Both hold virtually identical baskets of S&P 500 stocks.

**Key Difference**: SPY has 24× higher daily trading volume.

---

## August 24, 2015: Divergent Experiences

### SPY Performance

**Price Action:**
- **Previous Close**: $198.45
- **Opening Print**: $193.80 (-2.3%)
- **Intraday Low**: $182.42 (-8.1%)
- **Recovery**: $195.22 by 10:30 AM
- **End of Day**: $189.55 (-4.5%)

**LULD Halts:**
- **1 brief halt** at approximately 9:42 AM
- **Trading duration**: 5 minutes
- Minimal interruption to price discovery

**Spread Dynamics:**
- Normal spread: $0.01 (0.0005%)
- Widest intraday spread: $0.50 (0.27%)
- Average spread during crash: $0.15-0.25 (0.08-0.13%)
- **Relatively tight** given conditions

**Disconnect from NAV:**
- Maximum discount: **3.2%** below fair value
- Brief: lasted ~5 minutes
- Arbitrage opportunities quickly exploited
- Market makers maintained continuous presence

### IVV Performance

**Price Action:**
- **Previous Close**: $198.08
- **Opening Print**: $191.20 (-3.5%)
- **Intraday Low**: $166.25 (-16.1%)**
- **Recovery**: $193.50 by 11:00 AM
- **End of Day**: $189.02 (-4.6%)

**LULD Halts:**
- **5 separate halts** between 9:30-10:15 AM
- **Trading duration**: ~8 minutes total out of 45 minutes
- Substantial interruption to price discovery

**Spread Dynamics:**
- Normal spread: $0.02-0.05 (0.01-0.025%)
- Widest intraday spread: **$3.50 (1.8%)**
- Average spread during crash: $1.25-2.00 (0.65-1.05%)
- **14× wider than normal conditions**

**Disconnect from NAV:**
- Maximum discount: **13.8%** below fair value
- Duration: ~30 minutes below 10% discount
- Slower arbitrage correction
- Some market makers stepped back temporarily

---

## Side-by-Side Comparison

| Metric | SPY | IVV | Difference |
|--------|-----|-----|------------|
| **Intraday Low** | -8.1% | -16.1% | **2× worse** |
| **Max NAV Discount** | -3.2% | -13.8% | **4.3× worse** |
| **LULD Halts** | 1 | 5 | **5× more** |
| **Widest Spread** | $0.50 | $3.50 | **7× wider** |
| **Recovery Time** | 20 min | 90 min | **4.5× longer** |
| **Executions <-10%** | Rare | Common | Significant |

**Identical underlying holdings. Massively different outcomes.**

---

## Why Did IVV Fare Worse?

### 1. Lower Trading Volume = Thinner Market Making

**SPY Market Making:**
- 50+ firms actively making markets
- Multiple large institutional arbitrageurs
- Continuous two-sided quotes
- Deep bench of capital deployed
- **High liquidity = many buyers for forced selling**

**IVV Market Making:**
- 15-20 market makers
- Less institutional arbitrage infrastructure
- Some firms went "quote-only" (no trades)
- Smaller capital commitment
- **Lower liquidity = forced selling hit air pockets**

**Result**: When selling pressure hit, SPY absorbed it better.

### 2. SPY Futures and Options Ecosystem

**SPY Hedging Instruments:**
- SPX options (S&P 500 index options) - massive liquidity
- ES futures (E-mini S&P 500) - most liquid futures contract
- SPY-specific options - huge volume
- Can hedge SPY exposure dozens of ways
- **Easy to establish arbitrage with protection**

**IVV Hedging Instruments:**
- Same SPX options and ES futures available
- IVV-specific options - much lower volume
- Fewer sophisticated option strategies traded
- **Same tools available, less market familiarity**

**Result**: Market makers more comfortable with SPY arbitrage during dysfunction.

### 3. Investor Base Differences

**SPY Investors:**
- 60% institutional (hedge funds, market makers, traders)
- 40% retail (mix of sophisticated and unsophisticated)
- Heavy day trading / algorithmic activity
- Less use of stop-loss orders (institutional preference for limits)
- **More sophisticated = fewer cascading stops**

**IVV Investors:**
- 40% institutional
- 60% retail (401(k), IRAs, long-term holders)
- More buy-and-hold behavior normally
- **Higher percentage of stop-loss orders**
- Less day trading infrastructure

**Result**: IVV had more stop-loss cascades from retail base.

### 4. Market Maker Relationships and History

**SPY:**
- 1993-2015: 22 years of market making
- Standardized arbitrage mechanisms
- Well-established trading protocols
- Market makers know each other, trust liquidity
- **"Muscle memory" for handling stress**

**IVV:**
- 2000-2015: 15 years (still mature)
- Less institutional trading infrastructure
- Slightly less standardized
- Fewer long-standing market maker relationships
- **Less practiced at extreme stress**

**Result**: SPY market makers stayed engaged longer.

### 5. Opening Auction Dynamics

**SPY Opening:**
- Massive volume (20-40 million shares typical)
- Opening auction at 9:30 AM had deep order book
- Wide participation from market makers
- Absorbed early selling pressure better

**IVV Opening:**
- Lower volume (1-2 million shares typical)
- Opening auction thinner
- Less deep order book
- **Greater price impact from same absolute selling**

**Result**: IVV gapped down more at open, triggering more stops.

---

## Arbitrage Opportunity: Buy IVV, Short SPY

**Theoretical Trade at 9:40 AM:**

**Market Prices:**
- IVV: $166.25
- SPY: $185.50
- **Spread: $19.25 (11.6% dislocation)**

**Trade Mechanics:**
1. Buy 10,000 IVV at $166.25 = $1,662,500
2. Short 8,390 SPY at $185.50 = $1,555,645
   - (Equivalent $ exposure: $1,662,500 / $198 = 8,396 shares of SPY)
3. Wait for convergence
4. Unwind at equal prices

**Expected Profit:**
- IVV and SPY should converge (track same index)
- Profit from $19.25/share narrowing to $0
- On 10,000 IVV shares: ~$96,000 profit (5.8% return)
- **Time horizon: Minutes to hours**

**Risks:**
1. Could IVV fall further? (Had already fallen 16%, SPY only 8%)
2. Borrow cost for shorting SPY during chaos
3. Margin requirements could change mid-trade
4. Execution risk on unwind

**Real-World Execution:**
- Some sophisticated traders executed versions of this
- Required:
  - Available capital ($1.6M+)
  - Ability to borrow SPY shares (locate)
  - Risk tolerance during apparent crisis
  - Understanding both ETFs track same index

**Actual Outcome:**
- IVV recovered to $193 by 11 AM
- SPY at $195 by 11 AM
- Spread narrowed from $19 to $2
- Those who executed captured most of theoretical profit

---

## Lessons from SPY vs IVV

### Lesson 1: Liquidity Matters More Than Holdings

**Same Index, Different Liquidity:**
- Both held identical S&P 500 stocks
- Both had same NAV at every point
- **SPY's higher liquidity = 2× better performance**

**Implication**: During stress, choose **most liquid** ETF for exposure, not lowest expense ratio.

**Example**: IVV saves 0.02% in fees vs SPY (2 basis points). On August 24, liquidity difference cost 8% (800 basis points). **Fee savings: 0.02%. Liquidity cost: 8%. Ratio: 400:1.**

### Lesson 2: Market Maker Infrastructure Is Critical

**Why SPY Performed Better:**
- More market makers = more liquidity providers
- Decades of relationships and infrastructure
- Standardized arbitrage mechanisms
- **Network effects in market making**

**Implication**: "Second best" ETF in a category can have substantially worse outcomes during stress, even with same underlying.

### Lesson 3: Investor Base Composition Affects Price Stability

**SPY (Institutional Heavy):**
- Less stop-loss usage
- More sophisticated order types
- Limit orders provide price support
- **Demand curve more stable**

**IVV (Retail Heavy):**
- More stop-loss cascades
- Market orders during dysfunction
- Less price support
- **Demand curve more fragile**

**Implication**: ETF with same holdings but different investor base = different crash behavior.

### Lesson 4: Trading Volume Matters for Arbitrage Speed

**SPY:**
- 85M shares/day volume
- Arbitrageurs enter quickly (high conviction from liquidity)
- Dislocations corrected in minutes

**IVV:**
- 3.5M shares/day volume
- Arbitrageurs more cautious (lower normal liquidity)
- Dislocations corrected in hours

**Implication**: Higher volume = faster mean reversion during stress.

### Lesson 5: "Close Enough" Isn't Good Enough

**Pre-August 24 Thinking:**
- "IVV and SPY basically the same, I'll buy IVV for lower fees"
- "2 basis points savings over 30 years = thousands of dollars"
- **Focused on normal market conditions**

**Post-August 24 Reality:**
- 8% worse performance in single day
- Years of fee savings wiped out in hours
- **Tail risk matters more than marginal cost**

**Implication**: Liquidity premium worth paying for potential crisis scenarios.

---

## Advisor and Institutional Response

### Before August 24, 2015

**Typical Recommendation:**
- "IVV has lower expense ratio (0.07% vs SPY's 0.09%)"
- "Both track S&P 500, go with cheaper one"
- "2 basis points = $200/year on $1M portfolio"
- **Fee optimization was primary consideration**

### After August 24, 2015

**Updated Recommendation:**
- "SPY provides superior liquidity during stress"
- "2 basis point fee difference negligible vs liquidity risk"
- "For large accounts or active trading, SPY essential"
- "IVV acceptable for buy-and-hold with no stop-losses"
- **Risk management became primary consideration**

**Institutional Changes:**
- Many 401(k) plans switched from IVV to SPY
- Trading desks required SPY for tactical positions
- IVV usage limited to long-term passive allocations
- **Liquidity now explicitly valued**

---

## When to Choose SPY vs IVV Today

### Choose SPY if:
- ✅ Trading actively or tactically
- ✅ Using stop-loss orders (despite risks)
- ✅ Account over $500K (liquidity matters more)
- ✅ Options strategies planned
- ✅ Concerned about crisis liquidity
- ✅ Institutional or sophisticated investor

**Priority: Liquidity > Fees**

### Choose IVV if:
- ✅ Buy-and-hold only (no trading)
- ✅ Never using stop-losses
- ✅ Small account (<$100K)
- ✅ Fee conscious for long horizon
- ✅ Won't panic sell during crashes
- ✅ Understand and accept lower liquidity

**Priority: Fees > Liquidity**

### Never Choose IVV if:
- ❌ Day trading or frequent rebalancing
- ❌ Using leverage
- ❌ Options strategies
- ❌ Tight stop-losses
- ❌ Risk of forced liquidation

**Risk exceeds fee savings.**

---

## Quantitative Analysis

### Historical Spread Analysis

**SPY:**
- Normal spread: 1-2 basis points (0.01-0.02%)
- Crisis spread (Aug 24): 8-13 basis points
- **Crisis premium: 6-11 basis points**

**IVV:**
- Normal spread: 1-2.5 basis points
- Crisis spread (Aug 24): 65-105 basis points
- **Crisis premium: 63-103 basis points**

**Result**: IVV crisis spreads were **10× worse** than SPY.

**Fee Savings from IVV**: 2 basis points/year
**Crisis Spread Cost**: 80 basis points one-time

**Break-Even**: Would need **40 years** of fee savings to recover one flash crash spread cost.

### Tracking Error Analysis

**Normal Conditions (2010-2015):**
- SPY tracking error: 0.02% annually
- IVV tracking error: 0.02% annually
- **Identical in normal times**

**August 24, 2015:**
- SPY maximum NAV deviation: -3.2%
- IVV maximum NAV deviation: -13.8%
- **IVV 4.3× worse during crisis**

**Implication**: Tracking error statistics in normal times don't predict crisis performance.

---

## Academic and Regulatory Analysis

**SEC Research (2015):**
- Highlighted SPY vs IVV as example of liquidity importance
- Used to argue for enhanced transparency in ETF liquidity
- Showed that identical holdings ≠ identical outcomes

**Academic Papers:**
- "ETF Liquidity and Market Stress" (2016)
  - SPY vs IVV featured prominently
  - Liquidity premium quantified
- "The Flash Crash and ETF Microstructure" (2017)
  - Market maker behavior in SPY vs IVV analyzed

**Industry Changes:**
- ETF issuers now disclose "liquidity score"
- Advisors must consider liquidity, not just expense ratios
- Regulators require stress scenario disclosures

---

## Case Study: Two Investors, Different ETFs

### Investor A: Chose SPY

**Portfolio:**
- $500,000 in SPY at $198.45
- 2,520 shares
- No stop-loss orders
- Long-term hold

**August 24 Experience:**
- Saw -8.1% intraday low ($182.42)
- Didn't panic sell
- Ended day at $189.55 (-4.5%)
- Loss: $22,500

**Recovery:**
- Held position
- Recovered to $198 within 2 weeks
- Full recovery, no permanent damage

### Investor B: Chose IVV

**Portfolio:**
- $500,000 in IVV at $198.08
- 2,524 shares
- Stop-loss at $178.30 (10% protection)
- "Safe" strategy

**August 24 Experience:**
- Saw -16.1% intraday low ($166.25)
- Stop triggered at $178.30, executed at $169.50
- **Sold all shares at $169.50**
- Proceeds: $427,818
- Loss: $72,182 (14.4% loss vs intended 10%)

**Aftermath:**
- Forced out of market
- Missed recovery
- Permanent loss

**Comparison:**
- Same index, same $ investment, same timeframe
- **Investor A (SPY): -$0 (recovered)**
- **Investor B (IVV): -$72,182 (permanent)**
- Difference: $72,182
- **Cause: ETF selection + order type**

---

## Conclusion

SPY and IVV track the same index and hold virtually identical stocks. Yet on August 24, 2015, they experienced dramatically different crashes:
- **SPY**: -8.1% low, 1 halt, tight spreads, quick recovery
- **IVV**: -16.1% low, 5 halts, wide spreads, slow recovery

**The difference: market structure, not holdings.**

Liquidity, market maker infrastructure, investor base, and trading volume determined outcomes. The lesson: **ETF wrapper characteristics matter as much as underlying assets during market stress.**

For investors:
- **Liquidity premium is worth paying** (2 basis points irrelevant vs 8% crisis gap)
- **Most liquid ETF in category** = best crisis performance
- **Don't optimize for fees** at expense of liquidity
- **Market structure matters** when markets break

August 24, 2015 taught the industry that **ETF selection requires more than comparing expense ratios and tracking error in normal times. Crisis liquidity is the hidden cost that dwarfs all other considerations.**

---

**See also:**
- [RSP Case Study](case-study-rsp.md) - Different index, similar liquidity lessons
- [Market Maker Perspective](../04-market-maker-perspective/market-maker-behavior.md)
- [Lessons Learned](../05-aftermath/lessons-learned.md)
- [Order Types](../01-background/order-types.md)
