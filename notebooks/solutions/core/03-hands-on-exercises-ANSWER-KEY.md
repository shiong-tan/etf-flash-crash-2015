# Hands-On Exercises - Answer Key

This document shows the expected outputs for each exercise in `03-hands-on-exercises.ipynb`.

For complete working code, see: `03-hands-on-exercises-solutions.ipynb`

---

## Exercise 1: NAV and iNAV Calculation

### Part A: Normal Market Conditions

**Expected Output:**
```
NAV (end of yesterday): $74.90
iNAV (current 10:00 AM): $75.06

📊 Analysis:
   ETF value increased $0.16 per share (+0.21%)
   This reflects the overnight price movements in holdings
```

**Calculations:**
- NAV = (Total holdings value + Cash - Liabilities) / Shares outstanding
- Holdings value = AAPL(100×$150) + MSFT(80×$300) + GOOGL(50×$140) + NVDA(60×$450) + META(70×$320)
- Holdings value = $15,000 + $24,000 + $7,000 + $27,000 + $22,400 = $95,400
- NAV = ($95,400 + $5,000 - $1,000) / 10,000 = $9.94

**For iNAV:**
- Use current prices instead of closing prices
- Formula accounts for creation unit size and cash component

---

### Part B: Flash Crash Scenario

**Expected Output:**
```
Reported iNAV (with stale prices): $75.04
True fair value (if all trading): $73.68

iNAV Calculation Error: 1.85%

⚠️  Market makers see $75.04 but true value is $73.68!
This is why arbitrage breaks down during flash crashes.

📊 Analysis:
   Stale prices overstate iNAV by $1.36
   60% of holdings (GOOGL, NVDA, META) are halted
   Market makers can't trust iNAV for arbitrage pricing
```

**Key Insight:** When 60% of holdings use stale prices, iNAV overstates true value by $1.36, making arbitrage impossible.

---

## Exercise 2: Order Book Simulation

### Part A: Build a Normal Order Book

**Expected Output:**
```
=== NORMAL ORDER BOOK ===
Order Book:
----------------------------------------
     Price       Size |      Price       Size
                BIDS |                 ASKS
----------------------------------------
    199.99        500 |     200.01        500
    199.98        750 |     200.02        750
    199.95      1,000 |     200.05      1,000
    199.92        800 |     200.08        800
    199.90        600 |     200.10        600

Bid-Ask Spread: $0.02 (1.0 basis points)

📊 Analysis:
   Tight spread indicates healthy liquidity
   Deep order book (3,650 shares on bid side)
   Ready to handle normal trading volume
```

**Explanation:** Normal market with tight 1 bps spread and good depth at each level.

---

### Part B: Execute Market Orders

**Expected Output:**
```
100 shares executed at: $199.99
  Filled against best bid at $199.99

2000 shares executed at average: $199.94
  Walked through 5 price levels
  Execution breakdown:
    500 shares @ $199.99
    750 shares @ $199.98
    1000 shares @ $199.95
    800 shares @ $199.92
    600 shares @ $199.90

⚠️  Slippage from large order: 0.02%
On 2000 shares: Loss of $50.00

📊 Analysis:
   Large order consumed multiple price levels
   Average execution $0.05 worse than small order
   This is normal price impact - liquidity has depth but not infinite
```

**Key Insight:** Large orders experience slippage as they "walk the book" through multiple price levels.

---

### Part C: Flash Crash Order Book

**Expected Output (typical run):**
```
=== FLASH CRASH SIMULATION ===
Starting fair value: $75.50

Trade 1: 100 shares @ $75.49 - FILLED
Trade 2: 100 shares @ $75.49 - FILLED
Trade 3: 100 shares @ $75.48 - FILLED
Trade 4: 100 shares @ $75.47 - FILLED
Trade 5: 100 shares @ $75.45 - FILLED
Trade 6: 100 shares @ $75.42 - FILLED
  ⚠️  Price $75.42 (-0.1%) approaching LULD band!
Trade 7: 100 shares @ $75.38 - FILLED
Trade 8: 100 shares @ $75.33 - FILLED
Trade 9: 100 shares @ $75.26 - FILLED
  ⚠️  Price $75.26 (-0.3%) breached LULD band!
Trade 10: 100 shares @ $75.18 - FILLED

=== RESULTS ===
Average execution price: $75.37
Worst execution price: $75.18
Decline from fair value: -0.4%
```

**Note:** Actual results vary due to stochastic order book simulation.

---

## Exercise 3: Stop-Loss Order Analysis

### Scenario Setup

Price path visualization shows DVY crashing from $75.50 to $49.00, then recovering to $71.50.

**Initial position:** 1,000 shares @ $75.50 = $75,500.00

---

### Strategy 1: Stop-Loss Order

**Expected Output:**
```
Stop-loss set at: $67.95 (10% protection)
Stop triggered at: 9:32
Execution price: $68.00

Final value: $68,000.00
Loss: $7,500.00 (9.9%)

⚠️  Intended to limit loss to 10%, actual loss: 9.9%!

📊 Analysis:
   Stop triggered at $68.00 (9:32 AM)
   But market already falling rapidly
   Execution at same price in this simplified model
   In reality, could execute even lower due to bid-ask spread
   Stop-loss provided NO protection from deeper crash
```

**Key Insight:** Stop-loss triggered close to the 10% threshold, but in a real flash crash with wide spreads, execution could be much worse.

---

### Strategy 2: Stop-Limit Order

**Expected Output:**
```
Stop-limit did NOT execute (price gapped through $65.00)
Position held to close: $71.50
Loss: $4,000.00 (5.3%)

📊 Analysis:
   Stop triggered at $68.00
   But next trade was $62.00 - below $65 limit
   Order never filled because price gapped through limit
   Resulted in smallest loss of all strategies!
   But this is LUCKY - you could have been stuck at $49 low
```

**Key Insight:** Stop-limit didn't execute because price gapped through the limit. This was lucky in this case, but could have left you holding at the $49 low.

---

### Strategy 3: Hold Through

**Expected Output:**
```
Held position through crash
Saw low of $49.00 but didn't sell
Final close price: $71.50
Loss: $4,000.00 (5.3%)

📊 Analysis:
   Required strong conviction and nerves of steel
   Watched -35% drawdown ($49.00 low)
   But recovered to only -5.3% by close
   Best outcome of the three strategies
   Many investors could not psychologically handle this
```

**Key Insight:** Holding through was the best strategy, but required watching a -35% drawdown without panicking.

---

### Strategy Comparison

**Expected Output:**
```
=== STRATEGY COMPARISON ===
        Strategy  Execution Price  Final Value  Loss Amount  Loss %
 Stop-Loss (10%)             68.0      68000.0       7500.0    -9.9
Stop-Limit ($65)             71.5      71500.0       4000.0    -5.3
    Hold Through             71.5      71500.0       4000.0    -5.3

📊 Key Findings:
   1. Stop-loss caused WORST outcome: -9.9% vs intended -10%
   2. Stop-limit got lucky by NOT executing: -5.3%
   3. Holding through was also -5.3%
   4. All strategies underperformed their intent during flash crash
   5. Best strategy depended on LUCK, not design!
```

**Chart:** Bar chart shows stop-loss (-9.9%) performed worst, while stop-limit and hold-through both ended at -5.3%.

---

## Exercise 4: Arbitrage Opportunity Analysis

**Expected Output:**
```
=== APPARENT ARBITRAGE OPPORTUNITY ===
RSP trading at: $43.77
iNAV showing: $71.00
Apparent spread: $27.23 per share (62.2%)
Arbitrage spread %: -38.35%
Profitable creation: False

On 10,000 shares:
Cost: $437,700.00
Apparent profit: $272,300.00

=== RISK ANALYSIS ===
Hedgeable exposure: $175,080.00 (40%)
Unhedged exposure: $262,620.00 (60%)

If halted stocks fall another 10% when they open:
Potential loss: $26,262.00

Apparent profit: $272,300.00
Potential loss: $26,262.00
Net outcome: $246,038.00
```

**Analysis:** Even after accounting for 10% further decline in halted stocks, apparent arbitrage still looks profitable. However:
- 60% of position is unhedged
- Halted stocks could fall much more than 10%
- Uncertain when halts will lift
- Potential for unlimited losses if market continues falling

**Answer to Question:** Market makers didn't arbitrage because:
1. Can't hedge 60% of position (stocks halted)
2. iNAV is unreliable (uses stale prices)
3. Risk of further decline >> apparent profit
4. Uncertain timeline for halts to lift
5. Capital requirements and margin stress

---

## Exercise 5: Portfolio Stress Test

**Expected Output (with example portfolio):**
```
=== PORTFOLIO STRESS TEST ===
Initial value: $48,600.00

Position breakdown:
  SPY: 100 shares @ $200.00 = $20,000.00 (41.2%)
  DVY: 200 shares @ $75.50 = $15,100.00 (31.1%)
  RSP: 150 shares @ $76.80 = $11,520.00 (23.7%)
  SPLV: 300 shares @ $39.50 = $11,850.00 (24.4%)

Value at intraday low: $31,960.20 (-34.2%)
Value at close: $45,557.50 (-6.3%)

Recovery from low to close: $13,597.30 (+42.5%)

⚠️  If stop-loss forced exit at low: Lost $16,639.80
    If held through to close: Lost $3,042.50
    Stop-loss cost extra: $13,597

📊 Analysis:
   Portfolio had 4 different ETFs
   Diversification did NOT help - all crashed simultaneously
   Intraday low: -34.2% drawdown
   Close loss: -6.3%
   Recovery: 42.5% from low to close
   Selling at the low would have locked in 13,597 extra loss

🔍 Worst performers:
   SPY: -8.8% decline to $182.42
   DVY: -35.0% decline to $49.14
   RSP: -43.0% decline to $43.77
   SPLV: -46.4% decline to $21.18

💡 Key Lesson:
   Traditional diversification (multiple S&P 500-based ETFs)
   provided NO protection during the flash crash
   All ETFs hit simultaneously due to structural issues
```

---

## Reflection Questions - Sample Answers

### 1. iNAV Reliability

**Answer:** iNAV is reliable when:
- All components are trading actively
- Prices are fresh (within seconds)
- Normal market conditions

iNAV breaks down when:
- Components are halted (stale prices)
- High volatility causes price delays
- Market stress prevents arbitrage
- Circuit breakers freeze some stocks

### 2. Stop-Loss Orders

**Answer:** Stop-loss orders are appropriate for:
- Protecting against gradual declines
- Enforcing discipline in normal markets
- Assets with continuous liquidity

NOT appropriate for:
- Flash crash scenarios
- Low liquidity securities
- Gap-prone markets
- When you want to hold long-term

**Alternatives:**
- Options (protective puts)
- Position sizing
- Diversification across asset classes
- Trailing stops with wider bands

### 3. Arbitrage

**Answer:** Arbitrage failed because:
- Can't hedge halted stocks (60% unhedged risk)
- iNAV unreliable (stale prices)
- Execution risk (wide spreads, no liquidity)
- Capital constraints (margin calls during stress)
- Uncertain timeline (when will halts lift?)
- Risk of further crash >> potential profit

**Key lesson:** Arbitrage requires ability to hedge ALL risk. When you can't hedge, it's speculation, not arbitrage.

### 4. Liquidity

**Normal times liquidity:**
- Tight spreads (1-5 bps)
- Deep order books
- Rapid execution
- Predictable price impact
- Many market makers competing

**Crisis liquidity:**
- Wide spreads (100-1000+ bps)
- Thin order books with gaps
- Uncertain execution
- Extreme price impact
- Market makers withdraw

**Key insight:** Liquidity is abundant when you don't need it, and vanishes when you do.

### 5. Personal Strategy

**Sample Answer:**
To protect an ETF portfolio from flash crash risk:

1. **Don't rely on stop-losses** - They fail during gaps and extreme volatility
2. **Use protective puts** - Options provide actual price protection
3. **Maintain cash reserves** - Don't be forced to sell at the low
4. **True diversification** - Not just multiple S&P 500 ETFs
5. **Avoid leverage** - Leverage amplifies flash crash losses
6. **Size positions appropriately** - Only invest what you can afford to see drop 50% intraday
7. **Understand mechanics** - Know how ETFs work and when they break
8. **Long-term focus** - If you can't handle watching -35%, don't check intraday prices

---

## Summary Statistics

### Expected Performance Metrics

**Exercise 1:**
- NAV: ~$74.90
- iNAV (normal): ~$75.06
- iNAV (flash crash with stale prices): ~$75.04
- iNAV (true value): ~$73.68
- Error from stale prices: ~1.85%

**Exercise 2:**
- Normal spread: 1-2 basis points
- Small order execution: Best bid/ask
- Large order slippage: 0.02-0.05%
- Flash crash price impact: 0.3-1.0%

**Exercise 3:**
- Stop-loss outcome: -9.9%
- Stop-limit outcome: -5.3% (got lucky)
- Hold through outcome: -5.3%
- Maximum intraday drawdown: -35.1%

**Exercise 4:**
- Apparent arbitrage profit: $272,300
- Unhedged risk: $262,620 (60%)
- Risk/reward: Highly unfavorable

**Exercise 5:**
- Portfolio drawdown: -30% to -40% (depends on mix)
- Recovery by close: +35% to +45% from low
- Stop-loss cost: ~$10,000-$15,000 extra loss

---

## Common Mistakes to Avoid

1. **Exercise 1:** Forgetting to account for shares outstanding when calculating NAV
2. **Exercise 2:** Not rebuilding order book before second execution (order book gets depleted)
3. **Exercise 3:** Confusing stop-loss trigger price with execution price
4. **Exercise 4:** Thinking apparent profit means actual profit (ignoring unhedged risk)
5. **Exercise 5:** Not accounting for position weights when calculating portfolio impact

---

## Additional Resources

- **Function signatures:** Check `src/etf_pricing.py` and `src/order_book.py` for exact parameter names
- **Real data:** See `notebooks/core/02-real-market-data-analysis.ipynb` for actual August 24 prices
- **Deep dive:** Read case studies in `guide/03-deep-dive/`
- **Extensions:** Advanced analysis in `notebooks/extensions/`

---

*Answer Key for ETF Flash Crash 2015 Hands-On Exercises*
*Last Updated: 2025*
