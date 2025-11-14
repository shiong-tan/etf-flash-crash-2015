# Case Study: Retail Stop-Loss Failures

Stop-loss orders are designed to limit downside risk by automatically selling when a price threshold is breached. On August 24, 2015, they instead became instruments of devastation, causing losses far exceeding investors' intended risk tolerances.

---

## How Stop-Loss Orders Work

**Normal Operation:**
1. Investor owns security at current price
2. Sets stop-loss trigger below current price (e.g., 10% down)
3. If price touches trigger level, **order converts to market order**
4. Market order executes at best available bid
5. Intent: limit loss to ~10%

**Critical Detail:**
- Stop-loss **≠** price protection
- After trigger, becomes market order
- Market order has **no price limit**
- Fills at whatever bid is available
- In volatile/illiquid markets, can execute far below trigger

---

## August 24 Failures: Real Examples

### IUSV (iShares Core S&P U.S. Growth ETF)

**The Setup:**
- Closed August 23 at **$126.80**
- Investor sets stop-loss at **$108.69** (14.3% below close)
- Intended protection: limit loss to ~14%
- Considered conservative risk management

**What Happened:**
- Market opened with extreme volatility
- IUSV price touched $108.69
- Stop-loss triggered, **converted to market order**
- Best available bid: **$87.32**
- **Execution at $87.32**

**The Damage:**
- Closed at $126.80, sold at $87.32
- Actual loss: **$39.48 per share (-31%)**
- vs intended loss: $18.11 per share (-14%)
- **Suffered 2.2x intended loss**
- 20% worse than stop-loss protection level

**Recovery:**
- By end of day, IUSV recovered to down only ~5%
- Forced seller locked in 31% loss on temporary dislocation
- Holder who survived opening volatility fine by afternoon

---

### DVY (iShares Select Dividend ETF)

**The Setup:**
- Closed near **$75**
- Conservative dividend investors
- Many held stops around **$70** (~7% protection)
- Product marketed to income-focused, risk-averse investors

**What Happened:**
- Stops triggered at $70
- Executions occurred around **$49**
- **35% below previous close**
- Underlying dividend stocks declined only 5%

**The Irony:**
- Dividend stocks = defensive, stable companies
- "Safe" holdings that generate income
- Investors using stops for extra protection
- Protection became catastrophe
- Lost 35% on holdings down 5%

---

### SPLV (PowerShares S&P 500 Low Volatility ETF)

**The Setup:**
- Closed at **$36.90**
- Explicitly marketed to **risk-averse investors**
- Name literally includes "Low Volatility"
- Many investors chose it specifically to avoid volatility
- Stops set at $33-34 range (~8-10% protection)

**What Happened:**
- SPLV dropped **46%** from close to low
- Fell from $36.90 to **$20.00**
- Stop-losses triggered throughout cascade
- Executions at $22-26 range (30-40% below close)
- **Halted 11 separate times** due to LULD
- Underlying low-volatility index fell ~4%

**The Ultimate Irony:**
- Product promise: low volatility
- Reality: highest volatility possible
- "Safe" product became most dangerous
- Conservative investors suffered worst losses

---

### PJP (Invesco Pharmaceuticals ETF)

**Advisor-Reported Case:**
- Client portfolios showed losses of approximately **$10,000** on PJP positions
- Stops triggered at market open
- ETF priced at 40% discount because **three underlying pharmaceutical stocks hadn't opened yet**
- Algorithms calculated iNAV from stale prices
- Executions occurred at deeply dislocated levels
- **Within hours, PJP recovered to down only 5%**
- $10,000 permanent loss on 5% temporary drawdown

---

## Why Stop-Losses Failed So Catastrophically

### 1. Conversion to Market Orders
- Stop trigger at $108.69
- Becomes market order: "sell at any price"
- In calm markets, executes near trigger (say $108.50)
- On Aug 24, best bid was $87.32
- **21-point gap** ($108.69 → $87.32)

### 2. Order Book Air Pockets
**Normal Order Book:**
```
Asks: $127.00 (1000 shares)
      $126.95 (2000 shares)
      $126.90 (5000 shares)
Bids: $126.85 (5000 shares)
      $126.80 (2000 shares)
      $126.75 (1000 shares)
```
- Dense, tight markets
- 5-cent spread
- Market order fills near expected price

**August 24 Order Book:**
```
Asks: $130.00 (100 shares)
      $120.00 (500 shares)
      $110.00 (1000 shares)
Bids: $90.00 (500 shares)    ← Market sell fills here
      $87.00 (1000 shares)
      $85.00 (2000 shares)
```
- Sparse, wide gaps
- $20+ spread
- "Air pockets" between price levels
- Market order falls through gap

### 3. Cascade Effect
1. Price decline triggers first wave of stops
2. Stop-losses convert to market sells
3. Market sells push price lower
4. Lower price triggers more stops
5. **Self-reinforcing downward spiral**
6. Each execution makes next execution worse

### 4. Distorted Opening Prints
- Many stops triggered by opening prints that were themselves dislocated
- SPLV opening print might have been $30 (vs $36.90 close)
- Stop at $34 triggered immediately
- But opening print was artifact of dysfunction, not "real" price
- By 9:40 AM, price recovered, but forced sellers already liquidated

---

## The Slippage Math

**IUSV Example:**
- **Intended protection**: $126.80 → $108.69 = $18.11 loss (14.3%)
- **Actual execution**: $126.80 → $87.32 = $39.48 loss (31.1%)
- **Slippage**: $21.37 per share
- **Slippage rate**: 118% (slippage was bigger than intended loss!)

**On 1,000 share position:**
- Intended loss: $18,110
- Actual loss: $39,480
- Excess loss: **$21,370**
- Stop-loss "protection" **increased losses by $21,370**

---

## Who Was Affected

**Retail Investors:**
- Used stop-losses based on advisor recommendations or online guidance
- Believed they had downside protection
- Many watched helplessly as executions came through 30% below triggers
- Permanent wealth destruction on temporary dislocation

**Advised Clients:**
- Advisors had implemented "prudent" risk management
- Clients assumed sophistication meant safety
- Difficult conversations explaining how protection failed
- Trust in advisors damaged

**Conservative Investors:**
- Those who chose "low volatility" products
- Dividend-focused retirees
- Risk-averse savers
- Ironically suffered worst outcomes

---

## Limit Orders: The Alternative That Worked

**How Limit Orders Differ:**
- Set minimum acceptable sale price
- "Sell, but not below $X"
- If price gaps below limit, **order doesn't execute**
- Position remains open

**August 24 Performance:**

**Limit Order at $108:**
- IUSV gapped down to $87
- Below $108 limit
- Order didn't execute
- Position survived
- By afternoon, down only ~5%
- **Avoided 31% loss**

**Stop-Limit Order (hybrid):**
- Trigger at $108.69, limit at $105
- When triggered, becomes limit order at $105
- Won't execute below $105
- On Aug 24, price gapped to $87, below limit
- **Order didn't fill, position survived**

---

## Practical Lessons

### 1. Stop-Loss ≠ Price Protection
- **Guarantees execution**, not price
- After trigger, becomes market order
- Can execute anywhere below trigger
- Aug 24: executed 20-40% below triggers

### 2. Most Dangerous During Gaps
- Overnight news can gap stocks
- Market open after weekend buildup
- Flash crashes and circuit breakers
- Exactly when "protection" most needed, it fails worst

### 3. Limit Orders Provide True Price Protection
- Set minimum acceptable price
- Risk: order may not execute
- Benefit: won't lock in catastrophic loss
- **Better to hold -5% position than force sell at -31%**

### 4. Stop-Limit Orders: Middle Ground
- Trigger converts to limit (not market) order
- Provides price protection after trigger
- May not execute if gap too severe
- But avoids worst outcomes

### 5. Avoid Market Orders at Open/Close
- First 30 minutes: least liquidity, highest volatility
- Last 30 minutes: similar issues
- If must trade, use limit orders
- Accept risk of no execution vs catastrophic price

### 6. Order Type Matters as Much as Position Size
- Same position, different order type = 35% outcome difference
- Strategic decision, not mere technicality
- Critical component of risk management

---

## Industry Response

**Broker Education Campaigns:**
- Major brokers sent client education on order types
- Warnings about stop-loss risks during volatility
- Guidance to use limit orders instead
- Many brokers changed default order types

**Advisor Practice Changes:**
- Many stopped recommending stop-losses entirely
- Shifted to limit orders for risk management
- More emphasis on position sizing vs mechanical stops
- Client education on order type implications

**But Market Structure Unchanged:**
- No restrictions on stop-loss orders
- No requirements for investor understanding
- No changes to circuit breaker/halt procedures that caused problem
- Same conditions could recur

---

## The Counter-Narrative

**Industry Initially Blamed Retail:**
- "Unsophisticated investors caused crash with market orders"
- Suggested retail using stops was the problem
- Implied market structure was fine

**SEC Strongly Rebutted:**
- "Hard to fathom how retail investors could have caused 317 ETPs to trigger circuit breakers and trillion dollar decline"
- Real problems:
  - Off-exchange trading reducing displayed liquidity
  - Market maker internalization creating disincentives for limit orders
  - OTC dealers stepping ahead of public markets for minimal price improvement
  - Market structure, not retail behavior, was root cause

---

## Lasting Impact

**Retail Behavior:**
- Sharp decline in stop-loss order usage
- Shift toward limit orders
- More awareness of order type implications
- Greater caution during opening period

**Product Selection:**
- Skepticism toward "low volatility" marketing claims
- Recognition that ETF labels don't prevent dislocations
- More attention to market structure vs just fund characteristics

**Trust Damage:**
- Some retail investors exited ETFs entirely
- Others became much more cautious
- Industry credibility suffered
- Question raised: If stops don't protect during crashes, what does?

---

**See also:**
- [Order Types Explained](../01-background/order-types.md)
- [Who Was Affected](../02-the-event/who-was-affected.md)
- [Order Book Simulation Notebook](../../notebooks/02-order-book-simulation.ipynb)
