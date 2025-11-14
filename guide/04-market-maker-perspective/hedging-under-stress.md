# Hedging and Liquidity Under Stress

## The Fundamental Challenge

On August 24, 2015, market makers faced impossible conditions: ETFs trading 30-40% below apparent fair value, suggesting massive arbitrage opportunities, but hedging tools unavailable and fair value unverifiable. The rational response was to withdraw—but withdrawal amplified the crisis.

---

## Pricing Uncertainty: The Core Problem

**The RSP Dilemma:**
- RSP (S&P 500 Equal Weight ETF) trading at **$50**
- iNAV showing **$71**
- Apparent opportunity: **$21 profit per share** (30% return!)
- On 100,000 share position: **$2.1 million profit**

**But:**
- Is iNAV actually $71?
- iNAV calculated from mix of current and stale prices
- Many underlying stocks halted or not yet opened
- "Last available price" might be 15-30 minutes old
- What if stocks gap sharply lower when they reopen?

**The Unknowable:**
- True fair value could be $71, $65, $55, or $50
- No way to verify without current prices
- Taking position at $50 might be genius or catastrophe
- **Transformed "arbitrage" into speculation on stale data**

---

## Inventory Risk Without Hedging

**Normal Market Making:**
1. Client sells 100,000 SPY shares to market maker at $500
2. Market maker immediately shorts equivalent:
   - S&P 500 futures: 20 contracts
   - Or short basket of underlying stocks
   - Or combination of both
3. Net position: market neutral (no directional risk)
4. End of day: Create or redeem to flatten inventory

**August 24 Reality:**
1. Client sells 100,000 RSP shares at $50 (buy order hits market maker)
2. **Can't short underlying equal-weight basket** (stocks halted)
3. **Can't short S&P 500 futures** (limit down at 9:25 AM)
4. **Can't use options** (markets dislocated, extreme skew)
5. Market maker holds **$5 million unhedged position**

**The Risk:**
- If market falls another 10%: lose $500,000+
- If "fair value" was actually $45, not $71: lose $500,000 immediately
- If circuit breakers trigger more halts: trapped in position
- If prime broker demands additional margin: capital squeezed
- **Unlimited downside, unknowable risk**

---

## Automated Safety Mechanisms

**Why Systems Have Circuit Breakers:**
- Algorithms trade based on statistical models
- Models assume prices reflect fair value
- When prices show "impossibilities," flag for human review
- Prevent catastrophic losses from data errors or extreme events

**What Algorithms Saw on August 24:**
- $10 billion S&P 500 ETF trading 40% below fair value
- Statistically: 20+ standard deviation event (should never happen)
- Price movements violating historical correlations
- Multiple contradictory signals across related instruments

**Automated Response:**
- **Pull quotes immediately**
- Halt automated trading
- Flag for human review
- Require manual override to resume
- **Better to miss profits than risk catastrophic loss**

**Jane Street's Likely Experience:**
- Sophisticated algorithms with well-tested safety protocols
- Systems detected anomalies exceeding parameters
- Automatic shutdown of quote submission
- Human teams called to assess situation
- Could override manually, but faced same uncertainty
- **Even with humans, rational choice was to step away**

---

## Cross-Asset Complexity Breakdown

**Jane Street's Normal Advantage:**
- Multi-asset expertise
- When equity hedges unavailable, use:
  - Index futures
  - Equity options
  - Related ETFs
  - International markets
  - Fixed income correlations
- Sophisticated cross-asset models

**August 24: All Tools Failed Simultaneously**

**Equities:**
- Hundreds of stocks halted
- Those trading showing huge gaps
- Stale prices unusable
- ✗ Primary hedge unavailable

**Futures:**
- E-Mini S&P 500 hit limit down 9:25 AM
- Trading halted
- Zero price discovery
- ✗ Key hedging tool gone

**Options:**
- Extreme volatility skew (VIX spiked)
- Put-call parity broke down
- Wide bid-ask spreads
- Unreliable pricing signals
- ✗ Cannot use for hedging

**Related ETFs:**
- IVV and SPY (both track S&P 500) showed 349-point discrepancy
- If tracking same index but pricing 19% different, which is right?
- Can't arbitrage between them (both wrong)
- ✗ Cross-ETF arbitrage impossible

**International Markets:**
- Asian markets closed (already tumbled overnight)
- European markets open but in their own stress
- Correlations breaking down
- ✗ Limited help

**Correlations Broken:**
- Relationships that held for years invalid in minutes
- Statistical models based on historical patterns useless
- Normal toolkit exhausted
- **Even Jane Street's sophisticated cross-asset approach insufficient**

---

## Balance Sheet Constraints

**Jane Street's Capital:**
- $41.6 billion total capital
- $6.4 billion liquidity buffer for stress
- Uses ~50% for current margin requirements
- **Remaining 50% cushion for unexpected events**

**But Even Massive Capital Has Limits:**
- Taking large unhedged positions across multiple ETFs
- RSP at $50: $5M position = acceptable single risk
- But what about DVY, SPLV, IVV, PJP, and 100 other ETFs?
- Cumulative exposure could reach hundreds of millions
- **Risk of loss exceeding even $6.4B buffer**

**Prime Broker Considerations:**
- Mark-to-market losses trigger margin calls
- Prime brokers tighten collateral requirements during volatility
- Using scarce balance sheet for ETF positions means:
  - Less capacity for other opportunities
  - Less buffer if conditions worsen
  - Potential forced liquidations if margin calls come

**Internal Risk Limits:**
- Firms set maximum position sizes and loss tolerances
- Aug 24 likely approached or exceeded limits
- Risk management teams can override desks
- **Preservation of firm > capturing uncertain profits**

---

## Speed of Contagion

**Timeframe of Events:**
- 9:25 AM: Futures limit down
- 9:30 AM: Market opens
- 9:31-9:40 AM: Worst dislocations
- **Most dramatic price moves occurred in 10-minute window**

**Human Decision-Making Challenges:**
- Events unfolding in minutes, not hours
- High-frequency market structure: prices cascade in milliseconds
- 15-30 second trading windows between LULD halts
- Insufficient time for comprehensive analysis

**The Speed Problem:**
1. Algorithm detects anomaly, shuts down (seconds)
2. Human team reviews situation (minutes)
3. While reviewing, more halts triggered
4. Conditions change second-by-second
5. By time human makes decision, context already different
6. **Human judgment couldn't operate fast enough**

**Jane Street's Advantage:**
- Experienced teams practiced for extreme events
- Sophisticated real-time monitoring
- Global coordination (multiple offices)
- Pre-planned protocols for crises
- **But even they couldn't fully navigate rapid chaos**

---

## Risk Management Response Mechanisms

### 1. Pulling Quotes or Widening Spreads

**Normal SPY Spread:**
- Bid: $499.99
- Ask: $500.01
- 2 cent spread = 0.004%

**August 24 Stressed Spread:**
- Fair value unknowable, assume $500 ± $20 uncertainty
- Bid: $480
- Ask: $520
- $40 spread = 8%
- **Spread wide enough to compensate for massive uncertainty**
- Effectively withdrawal (no one trades at 8% spread)

**Complete Withdrawal:**
- Remove quotes entirely
- No obligation to maintain markets
- Wait for clarity to return
- **Most common response on Aug 24**

### 2. Pre-Programmed Circuit Breakers

**Algorithm Design:**
- Detect statistical anomalies
- Compare current prices to historical patterns
- If outside parameters (e.g., 10 standard deviations), shut down
- Require manual review before resuming

**August 24 Triggers:**
- 40% discounts to fair value (unprecedented)
- Correlations between related products broken
- Volume spikes beyond historical norms
- **Systems correctly identified "something is very wrong"**

### 3. Capital Reserves

**Small Firm Problem:**
- Limited capital (say $500 million)
- Large loss could threaten survival
- Must withdraw early to protect firm
- **Fragile liquidity provision**

**Jane Street Advantage:**
- $41.6 billion capital
- $6.4 billion liquidity buffer
- Could weather storm without forced liquidations
- **Robust liquidity provision**
- But even Jane Street had to be selective

### 4. Central Risk Management

**Firmwide Oversight:**
- Central team monitors aggregate exposure
- Can override individual desk limits
- Coordinates hedging across asset classes
- Critical during dislocations when normal correlations break

**Jane Street's Likely Approach:**
- Central risk team assessed aggregate positions
- Looked across all ETFs, not just single products
- Evaluated cross-asset exposure
- Made strategic decisions about which positions acceptable
- **Sophisticated, but still had to limit exposure**

### 5. Scenario Analysis and Stress Testing

**Pre-Event Preparation:**
- Model extreme market moves
- Understand maximum potential loss exposure
- Test how hedges perform under stress
- Develop protocols for various scenarios

**Jane Street Likely Had:**
- Modeled severe market crashes
- Understood ETF dislocation risk
- Pre-planned responses to LULD cascades
- **Enabled faster, more confident decision-making than competitors**

---

## "Stepping Away" Phenomenon

**The Vicious Cycle:**
1. Volatility causes uncertainty about fair value
2. Uncertainty makes hedging unreliable
3. Without hedges, providing liquidity too risky
4. Market makers withdraw
5. Withdrawal reduces liquidity
6. Reduced liquidity amplifies volatility
7. Amplified volatility causes more withdrawal
8. **Self-reinforcing spiral**

**Liquidity Vanishes When Most Needed:**
- Normal conditions: abundant liquidity
- Stressed conditions: liquidity evaporates
- Precisely when investors need to trade, can't
- Or can only trade at terrible prices
- **Exposes fundamental fragility**

---

## Jane Street's Likely Actions on August 24

**What They Probably Did:**

**1. Maintained Some Presence:**
- Didn't withdraw entirely (unlike smaller firms)
- Quoted with very wide spreads
- Selective participation in brief trading windows

**2. Analyzed Underlying Prices:**
- Monitored which stocks had opened
- Calculated fair value for components with current prices
- Identified products where valuation possible vs impossible

**3. Selective Position-Taking:**
- Accumulated positions at truly attractive prices
- Only when could verify fair value for significant portion of basket
- Used capital cushion to take measured risk
- **Not catching all falling knives, just most attractive**

**4. Global Coordination:**
- Multiple offices (New York, London, Hong Kong)
- Cross-office communication on market conditions
- International perspectives on risk
- Coordinated response

**5. Disciplined Risk Management:**
- Respected internal limits
- Preserved capital for firm survival
- Stepped away when uncertainty too high
- **Distinguished calculated risk from reckless speculation**

**Result:**
- Jane Street likely earned significant profits from Aug 24
- Not from predatory behavior
- From superior information, capital, risk management, and discipline
- Profits came from providing liquidity when others couldn't
- **But even they couldn't provide continuous liquidity throughout**

---

## Lessons for Market Structure

**Voluntary Liquidity is Fragile:**
- No regulatory obligation to maintain markets
- Rational for firms to withdraw during extreme uncertainty
- But withdrawal creates systemic risk
- **Need structural solutions, not just hoping firms will participate**

**Capital Requirements Matter:**
- Small, undercapitalized firms withdraw first
- Creates concentration risk (few large firms dominate)
- But even large firms have limits
- **Liquidity depends on market maker solvency**

**Hedging Tools are Critical:**
- Market makers need functioning underlying markets
- When stocks halted, ETF market making impossible
- **LULD circuit breakers made hedging impossible**
- Circuit breakers solved one problem, created another

**Information Quality Essential:**
- Garbage-in-garbage-out on iNAV calculations
- Stale prices made fair value unknowable
- Market makers correctly didn't trust displayed values
- **Need real-time, reliable pricing during stress**

---

**See also:**
- [Jane Street Overview](jane-street-overview.md)
- [LULD from Market Maker View](luld-from-mm-view.md)
- [NAV Disconnect](../03-deep-dive/nav-disconnect.md)
- [Opening Chaos](../02-the-event/opening-chaos.md)
