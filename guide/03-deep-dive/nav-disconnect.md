# NAV Disconnect: Why ETFs Traded 30-40% Below Fair Value

## The Central Mystery

On August 24, 2015, major S&P 500 ETFs traded at discounts of 26-43% to their underlying value while the index itself fell only 5.3%. This wasn't a failure of the ETFs themselves—they held the correct securities—but a catastrophic breakdown in market structure.

---

## How iNAV Calculations Failed

**Normal iNAV Process:**
1. Take last available price for each security in basket
2. Multiply by shares held in creation unit
3. Sum all components including cash
4. Subtract liabilities
5. Divide by creation unit size
6. Update every 15 seconds

**August 24 Breakdown:**
- Step 1 failed: "last available price" was **stale from 15-30 minutes earlier**
- Hundreds of underlying stocks halted or not yet opened
- iNAV calculations used pre-market or previous day's closing prices
- Mixed current prices (for opened stocks) with stale prices (for halted stocks)
- Result: iNAV showed values based on demonstrably outdated information

**RSP Example:**
- iNAV showed $71 throughout crisis
- Based partially on stale prices from before massive selloff
- True fair value unclear: Was it $71, $65, $50?
- Market makers couldn't verify accuracy
- Trading RSP at $50 vs $71 iNAV might be arbitrage or catastrophic mispricing

---

## Why Market Makers Couldn't Determine Fair Value

**Four Critical Inputs All Failed:**

**1. iNAV (Primary Reference)**
- Relied on stale prices for halted stocks
- Mixed fresh and stale data
- Unreliable for decision-making
- Garbage in, garbage out

**2. Direct Pricing of Underlying Securities**
- Hundreds of stocks not trading
- Last prints from 15-30 minutes ago
- No way to cross-reference iNAV
- Independent validation impossible

**3. Futures and Derivatives**
- E-Mini S&P 500 futures hit **limit down at 9:25 AM**
- Halted before equities even opened
- Provided zero price discovery
- Normal hedging instrument unavailable

**4. Options Markets**
- Extreme volatility skew
- Dislocated pricing
- Unreliable signals
- Added confusion rather than clarity

**When all four inputs fail simultaneously, fair value becomes unknowable**

---

## The Hedging Impossibility

**Normal Arbitrage Process:**
1. ETF trades at discount (say $95 vs $100 NAV)
2. Buy ETF at $95
3. Simultaneously short underlying basket at $100 equivalent
4. End of day: redeem ETF for basket worth $100
5. Cover short with received securities
6. Profit = $5 minus transaction costs

**August 24 Reality:**
1. RSP trades at $50, iNAV shows $71 (apparent $21 opportunity)
2. Buy RSP at $50
3. **Can't short underlying basket—stocks are halted**
4. Even if you could, is basket really worth $71 or will it gap down?
5. Taking ETF position = unhedged directional bet on stale data
6. "Arbitrage" becomes speculation with unknown risk

**Risk Management Implication:**
- Unhedged directional exposure violates fundamental market-making principles
- Potential loss: unlimited if market continues falling
- Even with Jane Street's $41.6B capital, can't risk hundreds of millions on single bet
- Rational choice: step away until hedging becomes possible again

---

## Circuit Breakers Created Information Vacuums

**5-Minute Trading Halts:**
- No trading = no price discovery
- Exactly when markets needed information most, trading stopped
- Uncertainty increased rather than decreased during pauses
- Reference prices became stale during halts

**Brief Trading Windows:**
- RSP had **only 2.29 minutes of actual trading** in one hour
- 10 separate LULD halts
- Trading windows lasted 15-30 seconds before next halt
- Insufficient time for rational price formation

**Coordin

ation Failures:**
- Different exchanges used different reopening procedures
- NYSE: auctions with price collars
- Other venues: varied mechanisms
- Same security showed different prices on different exchanges
- Arbitrage between venues impossible during rapid halt cycles

---

## Dual Pricing Failure: IVV vs SPY

**The Anomaly:**
- Both track identical S&P 500 index
- Near-identical holdings and methodology
- At their respective lows:
  - **SPY priced S&P 500 at 1,829**
  - **IVV priced S&P 500 at 1,480**
  - **349-point discrepancy**

**Implications:**
- If IVV pricing correct: implies $3.2 trillion additional market cap loss
- Reality: both dislocated, IVV worse than SPY
- Demonstrated that even massive, liquid ETFs vulnerable
- **Second occurrence** of dual pricing failure (not isolated incident)
- Suggests systematic vulnerability in ETF market structure

---

## Why ETF Size Provided No Protection

**IVV: $65 Billion in Assets**
- One of largest ETFs in world
- Holds highly liquid S&P 500 stocks
- Market cap-weighted, standard index construction
- Should be most stable ETF imaginable
- **Still dislocated 26% vs 5.3% index decline**

**Size Doesn't Matter When:**
- Underlying stocks halted (can't determine fair value)
- Market makers can't hedge (unacceptable risk)
- Liquidity is voluntary (APs withdraw when unprofitable)
- Circuit breakers prevent trading (no price discovery)

**Liquidity Illusion:**
- ETFs appear ultra-liquid under normal conditions
- IVV trades hundreds of millions of shares daily
- But liquidity depends on market maker willingness to provide it
- When conditions make market-making impossible, size provides zero protection
- "Liquidity is abundant when you don't need it, scarce when you do"

---

## The Temporal Gap Vulnerability

**Dual Market Structure:**
- **Primary market (creation/redemption):** Occurs end-of-day around 4 PM
- **Secondary market (exchange trading):** Opens immediately at 9:30 AM

**The Gap:**
- ETFs begin trading at 9:30 AM
- But NAV calculated at 4 PM using closing prices
- iNAV estimates fair value intraday
- When iNAV fails, ETFs trade for hours without reliable fair value reference

**August 24 Exploitation:**
- 9:30 AM: ETFs open for trading
- 9:30-9:45 AM: Most underlying stocks not yet opened
- iNAV based on stale data
- ETFs trading blind for 15+ minutes
- By the time fair value calculable, damage already done
- 4:00 PM NAV would show ETFs had been massively mispriced

---

## Why Creation/Redemption Mechanism Failed

**Normal Operation:**
- APs profit from creating when ETF at premium
- APs profit from redeeming when ETF at discount
- Self-correcting mechanism keeps price near NAV
- Typically works within basis points

**August 24 Failure:**
- **APs have no obligation** to create or redeem
- Participation is voluntary, profit-motivated
- When profit becomes uncertain or risk too high, APs step away
- RSP at $50 vs $71 iNAV looked profitable but:
  - Can't verify if $71 is accurate (stale data)
  - Can't hedge underlying positions (stocks halted)
  - Risk of catastrophic loss if bet wrong direction
  - Rational to withdraw

**Voluntary Nature Exposed:**
- Creation/redemption is economic opportunity, not guaranteed service
- Works beautifully in normal conditions
- Breaks down precisely when most needed
- No regulatory obligation for APs to maintain liquidity during stress

---

## Statistical Evidence of Dysfunction

**SEC Research Findings:**
- ETFs with highest volume spikes **7x more likely** to trigger LULD
- ETFs with largest liquidity drops **5x more likely** to halt
- ETFs most correlated with S&P 500 **21x more likely** to pause than less correlated funds
- Pattern clear: volatility → liquidity withdrawal → halts → more volatility

**High-Frequency Trading Signatures:**
- ~50% of RSP trades flagged as Intermarket Sweep Orders
- Single-share trades (humans don't trade one share)
- Suggests algorithmic malfunction
- Broken systems dumping at any price

---

## Why This Matters

**Not an Isolated Event:**
- IVV/SPY dual pricing failure occurred twice
- Suggests repeatable vulnerability
- Conditions could recur
- Fundamental architecture unchanged

**Implications for Investors:**
- ETF price ≠ fair value during stress
- Size and liquidity provide no protection
- Stop-loss orders execute at dislocated prices
- "Safe" S&P 500 products can dislocate 40%

**Implications for Market Structure:**
- Voluntary liquidity provision fragile
- Circuit breakers mask problems rather than solve
- iNAV calculations inadequate for extreme conditions
- Need multiple simultaneous fixes, not just incremental improvements

---

**See also:**
- [LULD Mechanism](../01-background/luld-mechanism.md)
- [Case Study: RSP](case-study-rsp.md)
- [Opening Chaos](../02-the-event/opening-chaos.md)
- [Hedging Under Stress](../04-market-maker-perspective/hedging-under-stress.md)
