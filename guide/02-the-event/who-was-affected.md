# Who Was Affected

## Retail Investors — Catastrophic Losses

**Stop-Loss Order Failures:**

The hardest hit were retail investors using stop-loss orders as "protection."

**IUSV (iShares Core S&P U.S. Growth ETF):**
- Closed 8/23 at $126.80
- Investor's stop-loss set at $108.69 (14% loss limit)
- Stop triggered, converted to market order
- **Executed at $87.32** (31% below close, 20% below stop price)
- "Protection" became devastation

**DVY (iShares Select Dividend ETF):**
- Closed near $75
- Conservative dividend investors with stops around $70
- Executions occurred around **$49** (35% below close)
- Underlying dividend stocks declined only 5%
- Many positions liquidated permanently at worst prices

**SPLV (PowerShares S&P 500 Low Volatility ETF):**
- Marketed specifically to risk-averse investors
- Stop-losses executed after **46% decline**
- Underlying low-volatility index fell merely 4%
- Product promise utterly failed

**Common Pattern:**
- Stop-loss orders executed **20-40% below trigger prices**
- "Protective" mechanisms became instruments of destruction
- Losses far exceeded investor risk tolerances
- Positions liquidated at exact worst moment
- Recovered by afternoon, but forced sellers locked in losses

---

## Financial Advisors and Their Clients

**Client Relationship Damage:**

**PJP (Invesco Pharmaceuticals ETF) Example:**
- Advisors reported clients losing ~$10,000 on single positions
- Stop-losses triggered at market open
- Algorithms priced ETF at 40% discount because three underlying stocks hadn't opened
- Within hours, ETF recovered to down only 5%
- Permanent $10,000 loss on temporary dislocation

**Fiduciary Challenges:**
- Advisors had recommended "protective" stop-losses
- Standard risk management turned toxic
- Difficult client conversations explaining:
  - How "low volatility" products dropped 46%
  - Why stops executed 35% below trigger prices
  - How $65B funds could dislocate 26% in minutes

**Trust Erosion:**
- Clients questioned advisor competence
- Industry questioned ETF safety during stress
- Regulatory scrutiny on suitability of ETF recommendations
- Many advisors stopped using stop-loss orders entirely

---

## Market Makers and Authorized Participants

**Impossible Choices:**

**Pricing Uncertainty:**
- iNAV showed $71 for RSP trading at $50
- Is that $21 spread (30% arbitrage) or mirage from stale data?
- If underlying stocks gap lower when reopened, "arbitrage" = huge loss
- No way to verify without current prices

**Inventory Risk:**
- Taking ETF positions required directional market exposure
- Normal hedges unavailable:
  - Can't short halted stocks
  - Futures at limit down
  - Options markets dislocated
- Unhedged exposure violated fundamental risk management principles

**Automated Systems Shutdown:**
- Algorithms detected impossibilities (40% discounts to fair value)
- Pre-programmed safety mechanisms triggered
- Required human review before resuming
- Humans faced same impossible situation, chose to step away

**Career Risk vs Profit Opportunity:**
- Attempting to "catch falling knives" = potential career-ending losses
- Stepping away = foregone profits but capital preservation
- With Jane Street's $6.4B liquidity buffer, could afford to withdraw
- Smaller firms without such cushions might have faced existential risk

**Liquidity Withdrawal Vicious Cycle:**
- Market makers withdrew → liquidity vanished
- Reduced liquidity → wider dislocations
- Wider dislocations → more market makers withdrew
- Precisely when liquidity most needed, it disappeared

---

## Institutional Investors

**Portfolio Valuation Chaos:**
- Holdings displayed unrealistic intraday losses
- 40% drawdowns in core S&P 500 ETF positions
- Risk management systems flashing red
- Real-time P&L swings of millions

**Risk Management Protocols:**
- Many institutions have rules: liquidate if losses exceed X%
- Aug 24 triggered automated selling
- Forced to sell into illiquid markets at terrible prices
- Violating own risk limits = fiduciary breach
- Selling at 40% discount = locking in losses

**Hedging Complications:**
- Institutions attempting to buy protective puts created more selling pressure
- Dealers who sold puts needed to hedge by selling stock
- Hedging amplified downward momentum
- Options skew went extreme

**Concentration Risk Revealed:**
- Many institutions assumed large S&P 500 ETFs were ultra-safe
- IVV ($65B AUM) and SPY (even larger) both dislocated severely
- Size provided zero protection
- Questioned fundamental assumptions about ETF liquidity

---

## ETF Issuers

**Reputational Damage:**
- **302 of 1,569 ETFs triggered circuit breakers** (19% of all ETFs)
- Funds marketed as "low volatility" experienced extreme volatility
- Equal-weight S&P 500 fund dislocated 43% vs 4% index decline
- Questioned whether ETFs could be trusted during stress

**Technical Operations:**
- Issuers had to explain to investors why:
  - ETF prices diverged 40% from NAV
  - "Low volatility" products were most volatile
  - Large, liquid funds became illiquid instantly

**No Direct Fault:**
- Issuers calculate NAV correctly daily
- Hold appropriate underlying securities
- Problem was market structure, not fund operations
- But suffered reputational consequences anyway

**Industry-Wide Implications:**
- **85% of circuit breaker halts (1,046 of 1,237) affected ETPs** rather than stocks
- Suggested systematic vulnerability in ETF structure
- Led to questions about ETF design and regulation
- Some investors questioned whether to use ETFs at all

---

## The Exchanges

**Technical Coordination Failures:**
- Staggered stock openings prevented coherent price discovery
- Different exchanges used different reopening procedures
- Some returned orders during halts, others held them
- No synchronization across venues

**LULD Implementation Problems:**
- Reference price calculations used wide bid-ask midpoints
- Garbage-in-garbage-out: reference prices bore no relation to fair value
- 5-minute halts created information vacuums
- ETFs repeatedly triggered halts (10-11 times in hour)

**Fragmentation Issues:**
- Over 40% of trading off-exchange
- Reduced displayed liquidity on public markets
- Made coordination even harder
- Difficult to see where true liquidity resided

**Post-Event Response:**
- SEC research note (December 2015)
- Amendment 10 and 12 to LULD plan (2016)
- Rule 48 repealed
- But fundamental architecture unchanged

---

## Market Structure Itself

**Dual Market Vulnerability:**
- Primary market (creation/redemption) occurs end-of-day
- Secondary market (exchange trading) opens immediately
- Temporal gap exploited on Aug 24
- ETFs trading before fair value calculable

**Voluntary Liquidity Provision:**
- APs have no obligation to provide liquidity
- Withdraw when profit opportunities become too risky
- "Liquidity illusion": deep markets under normal conditions
- Vanishes precisely when most needed

**Circuit Breaker Design Flaw:**
- Stop trading but don't create liquidity
- Mask underlying problems rather than solving them
- 5-minute pauses when markets need information most
- Reference price calculations inadequate for extreme conditions

---

## Short-Term Winners

**Patient Capital:**
- Investors who bought at lows captured huge gains
- RSP at $43.77 recovered to $71+ within hour
- Required nerves of steel and available capital
- Most retail investors lacked information or courage

**High-Frequency Traders:**
- Some HFT firms profited from brief arbitrage windows
- Required sophisticated systems and risk management
- Many shut down rather than risk catastrophic losses
- Winners were exception, not rule

---

## Long-Term Impact on All Participants

**Retail:**
- Lost confidence in stop-loss orders
- Many switched to limit orders exclusively
- Avoid trading during first/last 30 minutes
- Some abandoned ETFs entirely

**Advisors:**
- Revised risk management protocols
- Client education on order types
- More conservative ETF usage
- Heightened awareness of market structure risk

**Market Makers:**
- Reinforced need for massive capital buffers
- Validated automated safety mechanisms
- Demonstrated importance of stepping away vs catching falling knives
- No regulatory obligation imposed to maintain liquidity

**Regulators:**
- Minimal structural changes despite severity
- Incremental LULD improvements
- Education emphasized over regulation
- Fundamental vulnerabilities remain

---

**See also:**
- [Retail Stop-Loss Case Study](../03-deep-dive/case-study-retail.md)
- [Hedging Under Stress](../04-market-maker-perspective/hedging-under-stress.md)
- [Lasting Lessons](../05-aftermath/lasting-lessons.md)
