# Case Study: SPLV (Invesco S&P 500 Low Volatility ETF)

## The Fund

**Invesco S&P 500 Low Volatility ETF (SPLV)**
- $5.8 billion in assets under management (as of Aug 2015)
- Tracks S&P 500 Low Volatility Index
- Selects 100 least volatile stocks from S&P 500
- Rebalanced quarterly based on historical volatility
- Explicitly designed to reduce portfolio volatility

**The Irony:**
- **Fund Mandate**: Minimize volatility
- **Marketing**: "Lower risk, smoother returns"
- **August 24 Reality**: Experienced **-46% intraday crash**
- **Greatest irony in financial markets**: "Low volatility" fund had highest volatility

**Normal Behavior:**
- Realized volatility 20-30% lower than S&P 500
- Popular with risk-averse investors and retirees
- Holdings: utilities, consumer staples, healthcare (defensive sectors)
- Perceived as "safer than broad market" alternative

---

## August 24, 2015: The Low Volatility Paradox

**The Numbers:**
- **Closed August 23** at approximately **$39.50**
- **Low on August 24**: **$21.18**
- **Intraday decline**: **-46.4%** (from close to low)
- **Underlying low-volatility index decline**: **-3.5%**
- **Disconnect**: **42.9%** temporary dislocation
- **Recovery**: Back to **$37.80** by 11:00 AM

**The Shocking Comparison:**
| Fund | Mandate | Aug 24 Decline |
|------|---------|----------------|
| **SPLV** | Low Volatility | **-46.4%** |
| SPY | S&P 500 | -8.0% |
| QQQ | Nasdaq (Tech) | -12.5% |
| DVY | Dividend | -35.0% |

**The Ultimate Irony**: The "low volatility" ETF was the **most volatile** security during the flash crash.

---

## Timeline of SPLV's Violent Crash

**9:30-9:32 AM:**
- Market opens with extreme volatility
- Low-volatility stocks (utilities, consumer staples) delayed opening
- Precisely the stocks SPLV holds didn't trade promptly
- iNAV calculations relied almost entirely on stale prices

**9:32-9:45 AM:**
- Triggered **8 separate LULD halts** (more than most other ETFs)
- Total trading time: **~3 minutes** out of 13-minute period
- Each brief trading window saw 5-10% drops
- Cascade of stop-loss orders from risk-averse investors

**9:45 AM (approximate):**
- **Hit devastating low of $21.18**
- 46.4% below previous close
- 42.9% below concurrent fair value
- Many "low risk" retirement portfolios decimated

**9:45-10:30 AM:**
- Defensive stocks gradually opened
- iNAV stabilized showing true value $36-38
- Sharp recovery as market makers entered
- Price recovered $16+ per share in 45 minutes

**10:30 AM onward:**
- Trading normalized around $37-38
- Only 3-5% below previous close (matching underlying)
- Dislocation corrected but damage done to forced sellers

---

## Why SPLV Was the Worst Performer

**1. Low-Volatility Stock Opening Delays**

**SPLV Holdings on Aug 24:**
- 40% Utilities (electric, gas, water companies)
- 25% Consumer Staples (food, household products)
- 20% Healthcare (pharmaceuticals, medical devices)
- 15% Other defensive sectors

**The Problem:**
- These stocks historically open slowly (low urgency to trade)
- August 24 delays even worse than normal
- Tech stocks (high volatility) opened quickly
- "Low volatility" stocks = slow to price during crisis
- **Result**: 60-70% of SPLV holdings not trading at 9:35 AM

**2. iNAV Calculation Collapse**

**Normal Day:**
- iNAV updates every 15 seconds
- Based on current prices of 100 holdings
- Accurate fair value estimate
- Arbitrage keeps ETF price near iNAV

**August 24, 9:35 AM:**
- 70 of 100 holdings not yet trading
- iNAV using yesterday's 4 PM prices for 70 stocks
- 30 stocks trading down 6-10%
- Weighted iNAV showed $37 (2-3% decline)
- **But**: Was this accurate if 70% of inputs stale?
- **Market makers correctly didn't trust the number**

**3. Hedging Impossibility**

**Apparent Arbitrage Opportunity at 9:40 AM:**
- SPLV trading at $21.18
- iNAV showing $37
- Spread: **$15.82 per share (75% profit!)**
- On 100,000 shares: **$1,582,000 "profit"**

**Reality - Cannot Execute Arbitrage:**
1. Buy SPLV at $21.18 (easy part)
2. Short basket of 100 low-volatility stocks (impossible!)
   - 70 stocks not trading (can't short)
   - Remaining 30 stocks insufficient to hedge
3. Can't redeem until 4 PM (8 hours of exposure)
4. Don't know true fair value of unopened stocks

**Rational Market Maker Decision:**
- $21.18 looks cheap but can't hedge 70% of risk
- Taking $2.1 million position unhedged = speculation, not arbitrage
- **Stand aside until hedgeable**
- Withdrawal of liquidity → prices fall further

**4. Stop-Loss Concentration from Risk-Averse Investors**

**Typical SPLV Investor Profile:**
- Retirees seeking capital preservation
- Risk-averse portfolios
- Chose SPLV specifically to avoid volatility
- **Higher usage of stop-loss orders** to "protect"

**The Cascade:**
1. Price drops 10% → triggers stops at $35-36
2. Stops become market orders → execute at $32-33
3. Executions trigger more stops at $30-31
4. Process cascades → prices reach $21
5. Each stop-loss added selling pressure
6. **Irony**: Risk-averse investors with protective orders suffered worst losses

---

## The "Low Volatility" Marketing vs Reality

**Pre-August 24 Marketing:**
- "Reduce portfolio volatility by up to 30%"
- "Smoother ride with lower drawdowns"
- "Ideal for risk-averse investors"
- "Defensive positioning for downturns"

**August 24 Reality:**
- **SPLV realized volatility**: ~2,500% annualized (during flash crash)
- **S&P 500 volatility**: ~350% annualized (during same period)
- **"Low volatility" had 7× the volatility of "high volatility"**

**The Fundamental Misunderstanding:**
- SPLV holds low-volatility *stocks*
- But ETF *price* subject to market structure risk
- Underlying asset volatility ≠ ETF price volatility
- Marketing focused on former, ignored latter

---

## Investor Impact Analysis

### Scenario 1: Retiree with Stop-Loss Order

**Setup:**
- Age 68, retired, conservative investor
- $200,000 in SPLV (5,063 shares at $39.50)
- Stop-loss at $35.55 (10% protection)
- Goal: Preserve capital, accept small losses to avoid large ones

**What Happened:**
1. 9:32 AM: Price drops to $35, triggers stop at $35.55
2. Stop converts to market order
3. Executes at $23.40 (nearest available bid)
4. Proceeds: $118,474
5. **Loss: $81,526 (41% loss vs intended 10%)**

**If No Stop-Loss:**
- Saw -46% on screen at 9:45 AM (didn't sell)
- Ended day at $37.80
- Loss: $8,612 (4.3%)
- **Stop-loss created 9.5× larger loss**

**Long-Term Impact:**
- Retirement income reduced by $81,526
- At 4% withdrawal rate: $3,261/year less income
- Permanent reduction in living standards
- All from "protective" order

### Scenario 2: Patient Opportunistic Buyer

**Setup:**
- Experienced trader, recognized dislocation
- Understood low-volatility stocks fundamentally stable
- Had available capital and no forced liquidation

**What Happened:**
1. 9:45 AM: Bought 5,000 shares at $22 = $110,000
2. 10:30 AM: Sold at $37 = $185,000
3. **Profit: $75,000 (68% return in 45 minutes)**

**Required:**
- $110,000 available capital
- Understanding of market structure
- Nerve to buy during apparent crisis
- Knowledge that utilities/staples fundamentally stable

### Scenario 3: Institutional Forced Seller

**Setup:**
- Pension fund with risk limits
- SPLV position within volatility budget
- Automated risk management: sell if down >15%

**What Happened:**
1. 9:35 AM: SPLV down 30% → exceeds risk limit
2. Automated system triggers forced sale
3. Executes 100,000 shares at average $26
4. Loss: $1,350,000
5. 10:30 AM: SPLV at $37 (recovery after forced exit)

**Counterfactual:**
- If held until 10:30 AM: Loss only $250,000
- Forced liquidation cost additional $1,100,000
- **Rigid risk management created losses it was designed to prevent**

---

## Comparison: SPLV vs Other Low-Volatility Strategies

**Similar "Low Volatility" Products on August 24:**

| ETF | Strategy | Aug 24 Low | Disconnect |
|-----|----------|------------|------------|
| **SPLV** | S&P 500 Low Vol | -46.4% | 42.9% |
| **USMV** | MSCI USA Min Vol | -32.1% | 28.5% |
| **EEMV** | EM Min Vol | -38.4% | 34.2% |
| **EFAV** | EAFE Min Vol | -41.2% | 37.8% |

**Key Finding**: **ALL low-volatility ETFs experienced extreme dislocations**
- Defensive stock opening delays = universal problem
- Risk-averse investor base = higher stop-loss concentration
- Marketing attracted wrong expectations
- Lower normal volatility ≠ protection during structure failure

---

## Market Maker Analysis: Jane Street's Dilemma

**9:30-9:40 AM - Cannot Provide Liquidity:**

**Information Available:**
- SPLV bid: $22
- SPLV ask: $26 (spread: $4 = 17%)
- iNAV: $37 (but 70% stale prices)
- 30 stocks trading, 70 stocks halted

**Risk Calculation:**
- Buy SPLV at $22
- Need to short 100 stocks to hedge
- Can short 30 stocks (down 6-10% → current value ~$36 for those)
- Cannot short 70 stocks (unknown current value)
  - If down 8% like the 30: Fair value ~$36
  - If down 15% (worse): Fair value ~$32
  - If down 2% (better): Fair value ~$37
- **Taking 70% unhedged exposure = not arbitrage**

**Decision: Stand Aside**
- Too much unknown risk
- Can't establish risk-free arbitrage
- Preserve capital for when hedgeable

**9:40 AM onward - Selective Entry:**
- 60 stocks now trading
- Can hedge 60% of position
- Fair value clearer: $36-38
- Begin buying SPLV at $24-28
- Take calculated risk on 40% unhedged
- Profit from dislocation while managing risk

---

## The "Low Volatility" Paradox Explained

**Why did "low volatility" have highest volatility?**

**1. Opening Dynamics:**
- High-volatility stocks (tech) = high trading frequency → open quickly
- Low-volatility stocks (utilities) = low trading frequency → open slowly
- During crisis, need rapid price discovery
- Slow-opening stocks → longer market structure dysfunction

**2. Investor Behavior:**
- SPLV attracted risk-averse investors
- Risk-averse investors use more protective orders
- More stop-losses = more cascading selling
- Defensive positioning → offensive losses

**3. Hedging Complexity:**
- 100 low-volatility stocks spread across sectors
- Less liquid than S&P 500 mega-caps
- Harder to hedge during partial trading halts
- Market makers withdraw earlier → wider spreads

**4. False Safety Signal:**
- Marketing emphasized low volatility
- Investors assumed safety extended to flash crash scenarios
- Complacency about order types and market structure
- "Safe" label → lower vigilance → worse outcomes

---

## Regulatory and Academic Interest

**SEC Post-Event Analysis:**
- SPLV featured prominently as "most ironic" case
- 46% drop in "low volatility" product = poster child for dysfunction
- Used to argue for market structure reforms
- Highlighted gap between fund objective and ETF structure risk

**Academic Papers:**
- "The Low Volatility Anomaly and the Flash Crash" (2016)
- "ETF Price Discovery During Market Stress" (2017)
- SPLV used as example in market microstructure courses

**Industry Response:**
- Improved disclosures about ETF price vs NAV risk
- Better education about difference between:
  - Low-volatility holdings (fund level)
  - ETF price volatility (structure level)
- Some advisors stopped using low-vol ETFs, others educated clients

---

## Long-Term Impact on SPLV

**Fund Performance:**
- Continued tracking S&P 500 Low Volatility Index
- No changes to methodology or holdings
- Resumed normal "low volatility" behavior
- Subsequent years confirmed defensive characteristics

**Post-Flash Crash Volatility (2016-2023):**
- Average annual volatility: 12-15% (vs 16-20% for S&P 500)
- Lower drawdowns during normal corrections
- Outperformed in bear markets (2018, 2020, 2022)
- **August 24 was exception, not rule**

**Investor Composition Changes:**
- Some retirees exited, citing "never again"
- Others stayed, recognizing structure vs fundamentals
- New investors required to acknowledge flash crash risk
- Shift toward more limit orders, fewer market/stop orders

**Assets Under Management:**
- Brief outflows post-August 24
- Recovered within 6 months
- Grew to $9+ billion by 2020
- Flash crash didn't destroy confidence long-term

---

## Key Lessons from SPLV

**1. Fund Objective ≠ ETF Structure Protection**
- SPLV holds low-volatility stocks ✓
- SPLV delivers low volatility in normal markets ✓
- SPLV price immune to structure failure ✗
- **Marketing focused on first two, ignored third**

**2. "Low Volatility" Attracted Wrong Order Types**
- Risk-averse investors = higher stop-loss usage
- Stop-losses amplified crash (opposite of intent)
- Defensive positioning → offensive losses
- **Need education: low-vol holdings ≠ use market orders safely**

**3. Defensive Stock Opening Delays Matter**
- Utilities, staples, healthcare open slowly
- Slow opening = longer iNAV stale period
- Longer iNAV stale = worse dislocation
- **Low-volatility stocks = longer dysfunction window**

**4. Arbitrage Requires Hedging All Components**
- 70% unhedgeable = no arbitrage opportunity
- "Cheap" at $21 wasn't actionable for market makers
- Liquidity withdrawal rational, not predatory
- **Can't force arbitrage when mechanics broken**

**5. Irony as Teaching Tool**
- 46% drop in "low volatility" ETF = memorable lesson
- Highlights fund objective vs structure risk
- Demonstrates importance of understanding wrapper vs holdings
- **Used in investor education worldwide**

---

## Comparison: What Would Have Worked Better?

**Instead of SPLV ETF:**

**Option 1: Individual Low-Volatility Stocks**
- Direct ownership of 20-30 utilities, staples
- Avoided ETF structure risk
- Saw same fundamentals (down 3-5%)
- No forced liquidation from stop-losses on ETF

**Option 2: SPLV with Stop-Limit Orders**
- Stop-limit at $35.50 (instead of stop-loss at $35.50)
- Would not have executed at $21-25
- Position remains open (accept this risk)
- Avoided catastrophic execution

**Option 3: SPLV with No Stop-Loss**
- Accept intraday volatility risk
- Hold through dislocation
- Ended day -4.3% (matching underlying)
- Simplest and most effective

**Option 4: Options for Protection**
- Buy $35 puts (cost ~$0.50)
- Guaranteed exit at $35 even if ETF at $21
- Limited downside with defined cost
- More expensive but actual protection

---

## Investor Testimonials (Reconstructed)

**Victim: Retiree Who Lost 40%**
> "I chose SPLV because I'm 70 years old and can't afford volatility. The brochure said 'low volatility.' I put a stop-loss at 10% to be safe. How did I lose 40%? I thought this was the conservative choice."

**Winner: Opportunistic Buyer**
> "I saw SPLV at $22 and knew it was absurd. These are electric utilities and toothpaste companies, not startups. Bought at $22, sold at $36 an hour later. Best trade of my career."

**Market Maker: Anonymous**
> "We wanted to help at $25 but couldn't hedge 70% of the position. That's not arbitrage, that's a directional bet. We came back around $30 when we could hedge enough to manage the risk."

**Financial Advisor**
> "I had clients in SPLV with stops. They called me crying after seeing executions at $24. I had to explain that 'low volatility' meant the stocks, not the ETF price during a market structure failure. Hard conversation."

---

## Conclusion

SPLV's 46% intraday crash stands as the ultimate irony of August 24, 2015. A fund explicitly designed to minimize volatility experienced the highest volatility. This wasn't fund failure—SPLV held exactly the right stocks and tracked its index perfectly. This was **ETF structure meeting market microstructure failure**.

The tragedy: Risk-averse investors chose SPLV for safety, added stop-losses for "extra protection," and suffered the worst losses. The opportunity: Sophisticated investors recognized temporary dislocation in fundamentally stable assets and captured massive gains.

The lesson endures: **Fund mandate and holdings don't protect against ETF structure risk. Understanding market mechanics, order types, and liquidity provision matters more than fund objective during crisis.**

---

**See also:**
- [Order Types Explained](../01-background/order-types.md)
- [DVY Case Study](case-study-dvy.md)
- [RSP Case Study](case-study-rsp.md)
- [NAV Disconnect](nav-disconnect.md)
- [Market Structure Lessons](../05-aftermath/lessons-learned.md)
