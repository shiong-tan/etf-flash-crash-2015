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

## Responsibility Assignment: Who Enforces LULD?

### Regulatory Framework Clarity

**Common Misconception**: Market makers are responsible for preventing trades outside LULD bands.

**Regulatory Reality** (FINRA Rule 6190 and SEC Release No. 34-67091):

**Trading Centers** enforce LULD, not individual market makers:
- **Trading Centers**: Exchanges (NYSE, Nasdaq, BATS/Cboe), ATSs (Alternative Trading Systems), OTC Market Makers **acting as venues**
- **Responsibility**: Prevent execution of trades that would occur outside price bands
- **Enforcement**: Trading centers must reject or cancel orders that would execute outside bands

**Market Makers** (as liquidity providers):
- **Obligation**: Provide continuous two-sided quotes when **able to calculate fair value and manage risk**
- **NOT Responsible**: Enforcing LULD price bands
- **NOT Obligated**: Providing liquidity when unable to hedge or price accurately

### What This Means for August 24

**Market Maker Decision Process**:

```
Question: Should I quote the ETF?

Regulatory Obligations:
- ✓ Must quote IF can calculate fair value
- ✓ Must quote IF can hedge position
- ✓ Must comply with Reg NMS best execution

NOT Obligated To:
- ✗ Quote when fair value unknowable (components halted)
- ✗ Quote when cannot hedge (unmanageable risk)
- ✗ Enforce LULD bands (exchange's job)

August 24 Reality:
- Cannot calculate fair value (60% components halted, iNAV stale)
- Cannot hedge (stocks halted, can't short basket)
- Quoting would be irresponsible capital management

Conclusion: Withdrawal is RATIONAL and APPROPRIATE
```

**Why This Distinction Matters**:

**Misguided Criticism** (August 24):
- "Market makers abandoned their responsibilities"
- "They should have provided liquidity during crisis"
- "Withdrawal was predatory behavior"

**Accurate Understanding**:
- **Market makers fulfilled their responsibilities**: Don't quote when can't price or hedge
- **Exchanges fulfilled LULD enforcement**: Prevented trades outside bands (when bands existed)
- **Problem**: Regulations created impossible situation, not market maker behavior

### Key Regulatory Principles

**Market Maker Obligations** (Regulation NMS):
1. **Best Execution**: Execute orders at best available price
2. **Continuous Quotes**: Provide two-sided markets when feasible
3. **Fair Pricing**: Quotes must reflect reasonable assessment of fair value

**When Withdrawal is Appropriate**:
1. **Cannot calculate fair value**: Stale data, halted components, information vacuum
2. **Cannot hedge risk**: Underlying markets halted or dysfunctional
3. **Existential capital risk**: Potential losses threaten firm survival

**August 24 Met All Three Criteria** → Withdrawal was prudent risk management, not market failure by market makers.

### Comparison: Market Maker vs Exchange Obligations

| Aspect | Market Maker | Exchange (Trading Center) |
|--------|--------------|---------------------------|
| **LULD Enforcement** | Not responsible | **Primary responsibility** |
| **Halt Triggers** | No control | Controls halt mechanism |
| **Band Calculation** | Uses bands for quoting | **Calculates and publishes bands** |
| **Reopening** | Participates if able | **Conducts reopening auction** |
| **Liquidity Provision** | **Voluntary, when feasible** | Platform for liquidity |
| **Fair Value** | **Must assess accurately** | No fair value obligation |
| **Risk Management** | **Must preserve capital** | No trading risk |

**Critical Insight**: August 24 was primarily a **regulatory failure** (LULD system design) and **market structure failure** (halt cascades), not market maker misconduct.

---

## Decision Framework: Quote or Withdraw?

### Systematic Decision Matrix

Market makers face a continuous decision: provide liquidity or withdraw? Here's the rational framework used during August 24.

### Framework Components

**1. Fair Value Calculation**
```
CAN calculate fair value IF:
- All or most component prices are current (not stale)
- iNAV is reliable (not based on halted stocks)
- Futures/baskets provide cross-check
- Historical volatility provides confidence interval

CANNOT calculate fair value IF:
- >40% of components halted (stale prices)
- iNAV based on 30+ minute old data
- No reliable cross-checks available
- Volatility too extreme for models
```

**2. Hedging Ability**
```
CAN hedge IF:
- Underlying stocks are trading (can short basket)
- Futures markets functioning (can use S&P futures)
- Sufficient time window (>2 minutes) to execute hedge
- Correlation stable (normal market conditions)

CANNOT hedge IF:
- Underlying stocks halted (can't access components)
- Futures at limit (can't use for hedge)
- Time window <1 minute (next halt imminent)
- Correlation breakdown (crisis conditions)
```

**3. Risk Assessment**
```
ACCEPTABLE risk IF:
- Position size < 1% of capital
- Maximum loss < 10% of position
- Hedge coverage > 80% of exposure
- Profit margin > 3× expected loss

UNACCEPTABLE risk IF:
- Potential loss > 5% of capital
- Unhedged exposure > $50M
- No reliable stop-loss mechanism
- Halt could trap position
```

### Decision Matrix

**The Four Scenarios**:

| Scenario | Can Calculate FV? | Can Hedge? | Decision | Rationale |
|----------|------------------|------------|----------|-----------|
| **A: Normal Market** | ✓ Yes | ✓ Yes | **QUOTE** | Normal market-making, manage risk/reward |
| **B: Information Issue** | ✗ No | ✓ Yes | **WITHDRAW** | Can't price accurately → can't quote responsibly |
| **C: Hedging Issue** | ✓ Yes | ✗ No | **WITHDRAW** | Unhedgeable risk → directional bet, not market-making |
| **D: Crisis** | ✗ No | ✗ No | **WITHDRAW** | Double failure → firm survival at risk |

**August 24 Reality**: Most of the time was **Scenario D** (Crisis).

### Worked Example: RSP at 9:35 AM

**Inputs**:

```
Market Conditions:
- RSP last trade: $50
- iNAV: $71 (but stale, components halted)
- Time since last RSP trade: 5 minutes (just reopened from halt)
- Components trading: 200 of 500 (40%)
- Components halted: 300 of 500 (60%)
- S&P 500 futures: -3.2%, trading
- Next halt risk: High (volatile reopening)
- Time window estimate: 15-30 seconds before potential re-halt
```

**Step 1: Can Calculate Fair Value?**

```
iNAV Analysis:
- Official iNAV: $71
- But based on:
  - 60% stale prices (components halted since 9:30-9:32)
  - 40% current prices (showing -2.8% average)
- Stale data age: 3-5 minutes

Fair Value Estimate Attempt:
- Start with $71 iNAV
- Adjust 60% of basket down by futures move: $71 × 0.6 × (-0.032) = -$1.37
- Adjust 40% with observed component moves: $71 × 0.4 × (-0.028) = -$0.80
- Rough estimate: $71 - $1.37 - $0.80 = $68.83

Confidence Interval: ± $6 (±9%)
Range: $63 - $75

Conclusion: Cannot calculate with acceptable precision
Uncertainty too high for responsible quoting
```

**Step 2: Can Hedge?**

```
Hedging Options Assessment:

Option A: Short equal-weight basket of 500 stocks
- Status: 60% of stocks halted (cannot short)
- Hedge coverage if attempted: 40%
- Unhedged exposure: 60% of position
- Conclusion: Insufficient hedge

Option B: Short S&P 500 futures
- Status: Trading, but at-3.2% (near limit)
- Correlation: RSP normally 0.95 correlation to S&P
- Crisis correlation: Unknown, possibly broken
- Tracking error risk: High in crisis
- Conclusion: Partial hedge at best, significant basis risk

Option C: Combinations
- 40% hedge via components + futures for rest
- Complex, execution risk
- Time required: 2-3 minutes
- Time available: 15-30 seconds
- Conclusion: Insufficient time

Overall Hedging Assessment: CANNOT HEDGE ADEQUATELY
```

**Step 3: Risk Assessment**

```
If Quote $50 Bid for 10,000 Shares:

Position: Long 10,000 RSP at $50 = $500,000
Hedge: Best case 40% via components = $200,000
Unhedged: $300,000

Risk Scenarios:

Scenario 1 (Optimistic): True FV = $68, no further decline
- P&L: ($68 - $50) × 10,000 = +$180,000
- Probability: 20%
- Expected value: +$36,000

Scenario 2 (Neutral): True FV = $55, modest further decline
- Mark position at $55
- P&L: ($55 - $50) × 10,000 = +$50,000
- But if halt triggers, can't exit
- If falls further during halt to $48:
- Loss: ($48 - $55) × 10,000 × 60% (unhedged) = -$42,000
- Net: +$8,000
- Probability: 40%
- Expected value: +$3,200

Scenario 3 (Pessimistic): True FV = $48, continued crash
- Immediate mark-to-market: ($48 - $50) × 10,000 = -$20,000
- Halt triggers, trapped
- Falls to $40 during halt
- Additional loss: ($40 - $48) × 10,000 × 60% = -$48,000
- Total loss: -$68,000
- Probability: 40%
- Expected value: -$27,200

Expected Value: $36k + $3.2k - $27.2k = +$12k

Risk-Reward Analysis:
- Expected profit: $12,000
- Potential max loss: $80,000 (if extreme downside)
- Risk/Reward ratio: 6.7:1 (risk : reward)
- Capital at risk: 5% of position size could be lost
- For $100M capital firm: 0.08% of capital at risk
- For $1B capital firm: 0.008% of capital at risk

Conclusion for Different Firms:
- Jane Street ($6.4B capital): Might accept this trade (0.001% capital risk)
- Medium firm ($500M capital): Marginal (0.016% capital risk)
- Small firm ($100M capital): REJECT (0.08% capital risk + existential if worst case)
```

**FINAL DECISION**:

```
Can Calculate Fair Value? ✗ NO (±9% uncertainty)
Can Hedge? ✗ NO (only 40% hedge available)
Acceptable Risk/Reward? Depends on firm size

Recommendation:
- Large firms (>$5B): SELECTIVE QUOTING (wide spreads)
- Medium firms ($500M-$5B): WITHDRAW
- Small firms (<$500M): WITHDRAW

August 24 Reality: Most firms WITHDREW
```

**What Actually Happened**:

- Most market makers withdrew (rational given framework)
- RSP spread widened to $10-$20 (vs normal $0.01)
- Only largest, best-capitalized firms participated sporadically
- Even large firms pulled back significantly
- Liquidity essentially disappeared

**Critical Point**: This wasn't market maker failure. The decision framework clearly shows withdrawal was the ONLY prudent choice for most firms.

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
