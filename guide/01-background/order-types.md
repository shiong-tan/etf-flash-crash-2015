# Order Types Explained

**Track**: [CORE] | **Difficulty**: ⭐⭐ Beginner-Intermediate | **Reading Time**: 8-12 minutes

**Prerequisites**: Basic understanding of stocks

**What You'll Learn**:
- Market orders vs limit orders
- Stop-loss orders (critical for understanding the crash)
- How orders interact with order books
- Why stop-losses cascaded on August 24

---

## Market Orders
**What they do:**
- Execute immediately at best available price
- Guaranteed execution, no price protection
- "Buy/sell at any price right now"

**In calm markets:**
- Executes near expected price
- Bid-ask spread typically tight (0.01-0.05% for liquid ETFs)
- Minimal slippage

**In volatile markets:**
- Can execute far from last traded price
- Thin order books create massive slippage
- Aug 24 example: Market sell orders executed 20-40% below expected prices

## Limit Orders
**What they do:**
- Execute only at specified price or better
- Price protection guaranteed, execution not guaranteed
- "Buy/sell only if price is acceptable"

**Advantages:**
- Control maximum price paid (buy) or minimum price received (sell)
- Prevent catastrophic executions during volatility
- May fill partially or not at all if price doesn't reach limit

**Disadvantages:**
- Risk missing the trade entirely
- In fast markets, may not execute at all

## Stop-Loss Orders
**What they do:**
- Set trigger price below current market (for sells)
- When touched, converts to market order
- Intended to limit losses

**How they work:**
1. Investor sets stop price (e.g., $108.69 on IUSV trading at $126.80)
2. Price hits trigger level
3. **Order becomes market order** (no price protection)
4. Executes at best available bid—which may be far below trigger

**Critical flaw:**
- Stop-loss ≠ price protection
- Guarantees execution, not price
- In Aug 24 example: IUSV stop at $108.69 executed at $87.32 (31% below close)
- Stop-loss becomes market order in worst possible conditions

## Stop-Limit Orders
**What they do:**
- Set trigger price and limit price
- When triggered, converts to limit order (not market order)
- "Sell if price drops to $X, but not below $Y"

**Advantages:**
- Provides price protection after trigger
- Won't execute at unacceptable prices

**Disadvantages:**
- May not execute at all if price gaps through limit
- Position remains open during extreme moves

## Order Type Behavior on August 24, 2015

**Market orders:**
- Executed at any available price
- Fell through "air pockets" in order books
- Created losses of 30-40% in seconds

**Stop-loss orders:**
- Converted to market orders when triggered
- Triggered early by distorted opening prints
- Executed 20-40% below trigger levels
- DVY: Stops executed at $49 vs $75 close (35% below)
- SPLV: Executes after 46% drop despite "low volatility" mandate

**Limit orders:**
- Protected investors from worst prices
- Many didn't execute but positions survived
- Avoided catastrophic liquidations

## Practical Lessons
1. **Stop-loss orders are market orders in disguise**
   - Provide no price protection when triggered
   - Most dangerous during gaps and volatility

2. **Use limit orders for price protection**
   - Accept risk of no execution vs catastrophic execution
   - Especially critical at market open/close

3. **Avoid market orders during volatile periods**
   - First/last 30 minutes of trading day
   - Around major news or economic data
   - During obvious market stress

4. **Order type choice matters as much as position size**
   - Aug 24: Identical positions, different order types = 35%+ difference in outcomes

---

**See also:**
- [Retail Stop-Loss Case Study](../03-deep-dive/case-study-retail.md)
- [Order Book Simulation Notebook](../../notebooks/02-order-book-simulation.ipynb)
