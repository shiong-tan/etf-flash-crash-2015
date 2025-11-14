# LULD from a Market Maker's View

## Circuit Breakers as Double-Edged Sword

Limit Up-Limit Down rules were designed to protect against erroneous trades far from fair value. On August 24, 2015, they achieved that goal—but at the cost of making rational market-making impossible. From a market maker's perspective, LULD created the worst possible environment: uncertainty maximized, hedging constrained, and timing compressed.

---

## How LULD Constrains Market Making

### Normal Market Making Process
1. Client wants to sell ETF
2. Market maker quotes bid price
3. If client accepts, market maker buys ETF
4. **Immediately hedge:** short underlying stocks or futures
5. Net position: market neutral
6. Carry inventory until can create/redeem or offset

**Time Requirement:** Seconds to minutes for hedge execution

---

### August 24 LULD Reality

**The Scenario:**
1. ETF trading in brief 15-30 second window between halts
2. Client wants to sell, market maker considers quote
3. If buy ETF, need to hedge immediately
4. **But underlying stocks are halted** (can't short)
5. Futures at limit down (can't use)
6. Next LULD halt could trigger any second
7. Would be **trapped with unhedged position** during 5-minute halt

**The Impossible Choice:**
- Quote bid and risk unhedged exposure?
- Or pull quote and provide zero liquidity?

**Rational Response:** Pull quote

---

## The Halt-Induced Hedging Problem

### RSP Example (10 Halts in One Hour)

**Trading Window Timeline:**
- **9:31-9:32**: 30 seconds of trading → HALT
- **9:32-9:37**: 5-minute trading pause
- **9:37-9:37.5**: 30 seconds of trading → HALT
- **9:37.5-9:42.5**: 5-minute trading pause
- ... repeat 8 more times ...

**Market Maker's Dilemma in Each Window:**

**Scenario A: Provide Liquidity**
1. Quote bid for RSP at $52
2. Fill order: buy 10,000 shares ($520,000 position)
3. Need to hedge by shorting equal-weight S&P 500 basket
4. **But 200 of 500 stocks are halted**
5. Can only hedge 300 of 500 components
6. 15 seconds later: **next LULD halt triggers**
7. **Trapped for 5 minutes with partial hedge**
8. If market falls during halt, **lose on unhedged 40% of position**

**Scenario B: Step Away**
1. Don't quote
2. Zero risk
3. Zero revenue
4. But preserve capital

**Which Would You Choose?**
- With Jane Street's $41.6B capital, maybe risk Scenario A
- With $500M capital (most firms), Scenario B mandatory
- **Most chose Scenario B → liquidity vanished**

---

## Information Blackouts During Halts

### 5-Minute Pause = 5-Minute Vacuum

**What Markets Need During Volatility:**
- **Information**: Current prices to assess fair value
- **Price discovery**: Trading to find equilibrium
- **Hedging**: Ability to manage risk

**What LULD Provides:**
- **No information**: No trades, no price updates
- **No price discovery**: Frozen for 5 minutes
- **No hedging**: Can't adjust positions

**Uncertainty Increases, Not Decreases:**
- Before halt: Market falling rapidly, but at least have prices
- During halt: Is it getting worse? Better? No one knows
- After halt: Pent-up uncertainty released violently
- **Halts amplify rather than resolve uncertainty**

---

## Stale Reference Prices

### LULD Reference Price Problem

**How Reference Price Calculated:**
- 5-minute average of transaction prices
- Updates when price moves >1% from current reference
- **If primary exchange can't open within 5 minutes:** uses midpoint of national best bid/offer

**August 24 Breakdown:**
1. Many stocks couldn't open within 5 minutes
2. Reference price defaulted to midpoint of bid/ask
3. **Market makers had withdrawn → spreads widened to $10-20**
4. Example: Bid $50, Ask $70 → midpoint $60
5. But true fair value perhaps $72
6. Reference price of $60 **based on dysfunctional market, not fair value**

**Market Maker Impact:**
- LULD bands calculated from garbage reference prices
- Bands placed at wrong levels
- Legitimate fair value quotes could trigger halts
- **System designed to prevent bad prints was using bad prints to set limits**

---

## Coordin

ation Failures Across Exchanges

### Fragmented Market Problem

**Multiple Exchanges Trading Same Security:**
- NYSE Arca
- Nasdaq
- BATS (now Cboe)
- IEX
- Dark pools
- Off-exchange venues

**August 24 Chaos:**

**NYSE Arca (primary market for many ETFs):**
- Uses auctions with price collars
- Might halt for 5 minutes
- Reopening process at 9:37 AM

**Nasdaq:**
- Different reopening procedure
- Might reopen at 9:37.5 AM (30 seconds later)
- Different price from NYSE

**BATS:**
- Yet another process
- Could reopen at 9:38 AM
- Third different price

**Market Maker's Nightmare:**
- Can't simultaneously see coherent market
- Same ETF shows different prices on different venues
- Which is correct? Where should hedge?
- Arbitrage between venues normally profitable
- During rapid halt cycles: **arbitrage impossible** (by time execute, another halt)

---

## The "Obvious Arbitrage" That Wasn't

### RSP at $50 vs iNAV $71: Why Not Buy?

**What Looks Like Free Money:**
- Buy RSP at $50 in market
- iNAV shows $71 fair value
- $21 profit per share (30% return)
- On 100,000 shares: $2.1 million profit
- Just redeem at day's end, receive $71 value in stocks
- **Seems like can't lose**

**Market Maker's Reality:**

**Problem 1: Can't Execute Hedge**
- To lock in arbitrage, need to simultaneously:
  - Buy RSP at $50 (can do in 15-second window)
  - Short equal-weight basket at $71 equivalent (can't—stocks halted)
- Without hedge: directional bet, not arbitrage
- If basket really worth $55 when stocks open, lose $5/share = $500K

**Problem 2: Halt Risk**
- Execute RSP buy at $50
- 10 seconds later: LULD halt
- Trapped for 5 minutes with unhedged $5M position
- If news breaks during halt (e.g., worse economic data), gap down
- Resume at $45, lose $500K before can react

**Problem 3: iNAV Reliability**
- Is $71 accurate or based on stale data?
- If many components haven't opened, iNAV using old prices
- True value might be $50, making this not arbitrage but overpaying

**Problem 4: Creation Uncertainty**
- Plan to redeem RSP at end of day
- But will get basket of stocks worth... what?
- If stocks open sharply lower, basket worth $55, not $71
- Redemption doesn't guarantee $71, just gives you stocks at their current prices

**Conclusion: Not Arbitrage, Pure Speculation**
- Can't hedge = directional risk
- Can't verify fair value = informational risk
- Can get trapped by halts = liquidity risk
- **Rational market makers passed**

---

## Amendment 10 and 12: Post-Crisis Improvements

### Amendment 10 (April 2016)

**Problem It Addressed:**
- Reference prices calculated from wide bid-ask midpoints
- Midpoint bore no relation to fair value
- Created garbage-in-garbage-out problem

**Solution:**
- Modified reference price calculation
- Use prior day's closing price instead of potentially wide midpoints
- More reliable anchor during stressed openings

**Impact:**
- Reduced worst reference price failures
- But doesn't solve underlying problem: halts still prevent hedging
- Incremental improvement, not systemic fix

### Amendment 12 (September 2016)

**Problem It Addressed:**
- Different exchanges reopened at different times
- Same security showed different prices simultaneously
- Confusion and coordination failures

**Solution:**
- Harmonized reopening procedures
- Non-primary markets must remain halted if primary can't reopen within 10 minutes
- Wait for primary market to establish price

**Impact:**
- Better coordination across venues
- Reduced fragmentation during reopenings
- But halts still stop trading when markets need information most

---

## What Market Makers Actually Need

### For Rational Market Making to Be Possible:

**1. Current, Reliable Prices**
- All underlying securities trading
- Real-time updates, not stale data
- iNAV reflecting actual market
- **LULD halts prevent this**

**2. Ability to Hedge**
- Access to underlying stocks for delta hedging
- Functioning futures markets
- Options available for gamma management
- **LULD halts stocks, making hedging impossible**

**3. Time to Analyze**
- Sufficient trading windows to assess fair value
- Opportunity to adjust positions
- Not trapped by sudden halts
- **15-30 second windows insufficient**

**4. Predictable Market Structure**
- Know reopening procedures
- Consistent rules across exchanges
- Ability to plan around constraints
- **Aug 24 procedures ad hoc and chaotic**

**5. Acceptable Risk-Reward**
- Profit opportunity exceeds risk taken
- Capital not at existential risk
- **Aug 24: Risk unknowable, reward uncertain**

---

## The Fundamental Tension

### LULD Design Goals (Regulator Perspective):
- Prevent erroneous trades far from fair value ✓
- Provide cooling off periods during volatility ✓
- Protect retail investors from extreme prices ✓

### Market Maker Needs:
- Continuous access to underlying markets ✗
- Ability to hedge positions ✗
- Real-time price discovery ✗
- Time to analyze and respond (not seconds) ✗

**These Goals Are In Direct Conflict:**
- Halting trading prevents erroneous prints
- But also prevents hedging, making market-making impossible
- Protection comes at cost of market functionality
- **Aug 24 demonstrated that circuit breakers can amplify problems**

---

## Implications for Market Stability

### Perverse Incentives:

**Risk Management Says:**
- Don't provide liquidity when can't hedge
- Don't take positions on unknowable fair value
- Preserve capital over capturing uncertain profits
- **Withdraw during extreme conditions**

**Market Needs:**
- Liquidity most needed during stress
- Someone to intermediate between panicked sellers and potential buyers
- Price discovery requires continuous trading
- **But no one obligated to provide**

### The Liquidity Spiral:
1. Volatility triggers LULD halts
2. Halts prevent hedging
3. Market makers withdraw (can't hedge safely)
4. Withdrawal reduces liquidity
5. Reduced liquidity causes more volatility
6. More volatility triggers more halts
7. **Repeat until markets dysfunctional**

---

## Jane Street's Relative Advantage

**Why Jane Street Could Participate (Selectively):**
- $6.4B liquidity buffer meant could absorb some unhedged risk
- Sophisticated models to estimate fair value despite stale data
- Cross-asset expertise provided alternative hedging (when available)
- Experience with extreme events, pre-planned protocols
- Global coordination across offices
- **But even Jane Street had to pull back significantly**

**Why Smaller Firms Couldn't:**
- Limited capital (say $500M total, $50M buffer)
- Single large unhedged loss could threaten survival
- Less sophisticated fair value estimation
- Fewer alternative hedging options
- **Had to withdraw entirely**

**Result:**
- Concentration in crisis: Only largest, best-capitalized firms participate
- Creates single-point-of-failure risk
- If even Jane Street must withdraw, who provides liquidity?
- **Exposed fundamental fragility**

---

## Lessons for Policy

**Circuit Breakers Alone Insufficient:**
- Stop trading but don't create liquidity
- Mask underlying problems
- Can amplify dysfunction during cascading halts
- **Need complementary solutions**

**Hedging Access Critical:**
- Market makers need functioning underlying markets
- If stocks halted, ETF market-making impossible
- **Coordinated halts across related products problematic**

**Information Flow Essential:**
- 5-minute information blackouts counterproductive
- Markets need continuous price discovery
- **Consider shorter halts or no halts with wider bands**

**Voluntary Liquidity Fragile:**
- No obligation to provide liquidity during stress
- Rational for firms to withdraw
- But withdrawal creates systemic risk
- **Consider market-maker obligations or backstop liquidity providers**

---

**See also:**
- [LULD Mechanism](../01-background/luld-mechanism.md)
- [Hedging Under Stress](hedging-under-stress.md)
- [Opening Chaos](../02-the-event/opening-chaos.md)
- [Regulatory Changes](../05-aftermath/regulatory-changes.md)
