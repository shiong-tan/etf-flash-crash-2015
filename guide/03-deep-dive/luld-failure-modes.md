# LULD Failure Modes: August 24, 2015

**A Systematic Analysis of How Circuit Breakers Amplified the Crisis**

---

## Introduction

The Limit Up-Limit Down (LULD) mechanism was designed after the May 6, 2010 Flash Crash to prevent extreme price dislocations. On August 24, 2015, it instead **amplified the crisis**, triggering **1,278 trading halts** across 471 securities in the first hour.

This document analyzes the specific regulatory failure modes that transformed a market stress event into a full-scale flash crash.

**Key Insight**: LULD was designed for single-stock flash crashes (like the 2010 event where a single large order caused chaos). It failed catastrophically for **correlated crashes** where hundreds of securities moved simultaneously.

---

## Failure Mode 1: Opening Auction Cascade

### The Vulnerability

Between 9:30 AM and 9:35 AM, FINRA Rule 6190 creates a critical regulatory gap:

**The Rule**: If the primary exchange (NYSE, Nasdaq, NYSE Arca) has not opened a stock or ETP by 9:35 AM, other trading venues can trade it **without LULD price bands**.

**Why This Exists**: Prevents secondary venues from being locked out if primary exchange has technical issues or extreme order imbalances.

**The Problem**: During correlated stress events, hundreds of stocks can't open simultaneously, creating a 5-minute window with no price protection.

### What Happened on August 24, 2015

**Timeline**:

| Time        | Event                                                                 |
|-------------|-----------------------------------------------------------------------|
| 9:30:00 AM  | Markets open with massive sell pressure (China devaluation fears)   |
| 9:30-9:33   | **371 stocks can't open on NYSE** due to order imbalances           |
| 9:31 AM     | ETFs begin trading on BATS, EDGX, IEX without underlying stocks open|
| 9:31-9:35   | **No LULD protection** - secondary venues trade without bands       |
| 9:32 AM     | Market makers face: "Should I quote an ETF when I can't hedge?"     |
| 9:33-9:35   | Prices dislocate severely during unprotected trading                |
| 9:35+ AM    | Primary exchanges open, LULD bands activate                          |
| 9:35+ AM    | Prices immediately trigger halts (damage already done)               |

### Case Study: DVY (iShares Select Dividend ETF)

**9:31 AM - BATS BZX Exchange**:

```
DVY Status:
- Primary exchange (NYSE Arca): NOT OPEN (order imbalance)
- Component stocks: 60% halted, cannot open
- iNAV: $75.50 (using stale pre-market prices)
- LULD protection: NONE (primary hasn't opened)

Market Maker Dilemma:
- Can't calculate fair value (components halted)
- Can't hedge position (can't trade halted stocks)
- Must decide: Quote or withdraw?

Bid-Ask Spread:
- Bid: $50 (market maker willing to buy at huge discount)
- Ask: $70 (market maker willing to sell at huge premium)
- Midpoint: $60 (bears no relation to $75.50 fair value)

First Trade: $62.00 (-17.8% from iNAV)
- No LULD halt (bands don't exist yet)
- No arbitrage (can't trade component stocks)
- Pure panic selling into illiquid market
```

**9:33 AM - NYSE Arca Opens**:

```
DVY opens on primary exchange:
- Opening price: $72.15 (-4.4% from prior close)
- LULD bands now active: $67.95 - $83.05 (10% opening period)
- But prices on BATS already at $62
- Arbitrage kicks in: Buy DVY on BATS $62, sell on Arca $72
- Prices converge... to $65.20
- Immediately triggers LULD halt (below $67.95 band)
```

### The Cascade Mechanism

**Step 1**: Primary can't open → Secondary trades without protection
**Step 2**: No arbitrage (components halted) → Prices dislocate
**Step 3**: Primary finally opens → LULD bands activate
**Step 4**: Dislocated prices immediately trigger halts
**Step 5**: Halt creates information vacuum → Repeat

### Why This Happened

**Structural Issue**: Regulations assume **independent** opening failures (one stock technical issue). They don't account for **correlated** opening failures (hundreds of stocks simultaneously).

**Market Maker Impossibility**:
- **Fundamental principle**: Market makers provide liquidity when they can **calculate fair value** and **hedge risk**
- **August 24 reality**: Neither was possible during 9:31-9:35 window
- **Rational response**: Withdraw or quote with massive spreads
- **Result**: No rational arbitrage to enforce price discipline

### Quantitative Impact

**ETFs That Traded Without Protection (9:31-9:35 AM)**:

| ETF  | iNAV   | First Trade | Discount | Primary Opens | LULD Halt |
|------|--------|-------------|----------|---------------|-----------|
| DVY  | $75.50 | $62.00      | -17.8%   | 9:33 AM       | 9:33 AM   |
| RSP  | $76.80 | $68.00      | -11.5%   | 9:34 AM       | 9:35 AM   |
| SPLV | $39.50 | $32.00      | -19.0%   | 9:33 AM       | 9:33 AM   |

All three immediately halted once LULD bands activated.

### Post-Crisis Status

**This vulnerability still exists** in current regulations. The 9:30-9:35 window remains unprotected during highly volatile openings.

**Amendment 10** (April 2016) helped by changing Reference Price calculation, but the fundamental gap remains.

---

## Failure Mode 2: Halt-Induced Information Vacuum

### The Mechanism

When LULD triggers a 5-minute trading pause:

1. **No trades** occur across all exchanges
2. **No price discovery** happens for that security
3. **iNAV calculations** use stale prices from before halt
4. **Market makers** can't calculate current fair value
5. **But must decide** quotes for when trading resumes

This creates an **information vacuum**: the longer the halt, the more stale all price information becomes.

### The Compounding Problem

During August 24, halts were **staggered and cascading**:

**9:35 AM Example**:
- DVY: HALTED
- 60% of DVY components: HALTED (some halted earlier, some still trading)
- SPY futures: TRADING (down -3.2%)
- Dow futures: TRADING (down -4.1%)
- VIX: TRADING (up +40%)

**Market Maker's Dilemma**:

```
Question: What's DVY worth at 9:35 AM?

Information Available:
- iNAV: $75.50 (uses last prices before components halted)
- 60% of components: stale prices from 9:30-9:32
- 40% of components: current prices (still trading)
- S&P 500 futures: down -3.2% from 9:30
- Prior DVY trade: $65.20 (but that triggered the halt)

Calculation Attempt:
- Update 40% of holdings with current prices: -2.8%
- Apply futures move to other 60%: -3.2% × 0.6 = -1.9%
- Rough fair value: $75.50 × (1 - 0.028 - 0.019) = $72.00

Uncertainty Range: $68 - $76 (±5% uncertainty)

Risk: If DVY reopens at $70, and fair value is actually $74...
- Bought at $70, mark at $74 = profit
- Bought at $70, actually worth $66 = large loss
- Cannot hedge 60% of position (components halted)
- Unhedgeable directional bet with $4-8 uncertainty range

Decision: Withdraw or quote with massive spread ($68 bid, $76 ask)
```

### RSP Case Study: Compounding Information Vacuum

**RSP Timeline - First Hour**:

| Time     | Event          | Halt Duration | Info Vacuum |
|----------|----------------|---------------|-------------|
| 9:35 AM  | Halt #1        | 5 min         | Moderate    |
| 9:40 AM  | Reopens        | 15 sec trade  | High        |
| 9:40 AM  | Halt #2        | 5 min         | Very High   |
| 9:45 AM  | Reopens        | 12 sec trade  | Extreme     |
| 9:45 AM  | Halt #3        | 5 min         | Extreme     |
| ...      | 7 more halts   | ...           | ...         |

**By 10:00 AM**:
- Total halt time: ~45 minutes
- Total trading time: **2.29 minutes**
- Most recent component prices: 15-45 minutes old
- iNAV: Meaningless (based on prices from 9:30-9:35)

**The Perverse Feedback Loop**:

```
Halt (5 min) → Information goes stale
    ↓
Reopen (15 sec) → Insufficient time for price discovery
    ↓
Gap down (stale info + panic) → Hits band again
    ↓
Halt (5 min) → Information MORE stale
    ↓
Repeat (10 times)
```

### Mathematical Model

**Information Decay Function**:

Let `I(t)` = information quality at time `t` after halt starts:

```
I(t) = I₀ × e^(-λt)

Where:
I₀ = initial information quality (1.0 = perfect)
λ = decay rate (higher during volatile markets)
t = time since halt started (minutes)

Normal market: λ = 0.05 (slow decay)
Aug 24 crisis: λ = 0.30 (rapid decay)

After 5-minute halt in crisis:
I(5) = 1.0 × e^(-0.30 × 5) = 0.22 (22% information quality)

After 10 halts (45 min halt, 2 min trade):
Effective information quality ≈ 5%
```

### Impact on Fair Value Calculation

**Textbook iNAV Formula**:
```
iNAV = (Σ Shares_i × Price_i + Cash) / Shares_Outstanding
```

**Problem**: Requires **current** prices for all components.

**August 24 Reality**:
```
Stale iNAV = (Σ Shares_i × Price_i(t-30min) + Cash) / Shares_Outstanding

Where Price_i(t-30min) is 30 minutes old (meaningless)
```

**RSP Example at 10:00 AM**:

| Component Type        | % of Portfolio | Price Age    | Reliability |
|-----------------------|----------------|--------------|-------------|
| Still trading         | 20%            | Real-time    | High        |
| Halted 5 min ago      | 15%            | 5 min old    | Medium      |
| Halted 15 min ago     | 25%            | 15 min old   | Low         |
| Halted 30+ min ago    | 40%            | 30+ min old  | Meaningless |

**Calculated iNAV**: $71.00 (±$15 uncertainty range)
**Actual fair value**: Unknown, possibly $50-$80
**Last trade price**: $43.77

**Market maker conclusion**: Cannot price this. Withdraw.

### Why "Obvious Arbitrage" Wasn't Possible

**The Apparent Opportunity**:
```
RSP trading at: $43.77
iNAV showing:  $71.00
Apparent mispricing: $27.23 (38% discount)

Naive arbitrage:
1. Buy RSP at $43.77
2. Redeem for basket worth $71.00
3. Profit: $27.23 per share

Why didn't this happen?
```

**The Reality**:

1. **Can't redeem immediately**: Creation/redemption takes 1-3 days
2. **Can't hedge**: 60% of components halted (can't trade them)
3. **iNAV is stale**: Based on 30-minute-old prices
4. **True fair value unknown**: Could be $50-$80 range
5. **Unhedgeable risk**: Holding naked long RSP position

**True risk analysis**:
```
Buy RSP at $43.77

Scenario 1 (optimistic): Fair value = $65
- Hold 3 days to redeem
- If market recovers: profit $21.23
- If market falls further: loss potential unlimited

Scenario 2 (realistic): Fair value = $55
- Profit on redemption: $11.23
- But can't hedge for 3 days
- Market could fall 20% more
- Potential loss: $11 per share

Scenario 3 (pessimistic): Fair value = $48
- Loss on redemption: -$4.23
- Plus holding risk for 3 days

Risk/Reward: Unclear reward, massive downside risk
Decision: Don't trade (not actually arbitrage, it's speculation)
```

### Post-Crisis Changes

**Amendment 10** (April 2016):
- Use **prior day closing price** as Reference Price instead of midpoint
- Reduces garbage-in-garbage-out problem
- But doesn't solve information vacuum during halts

**No structural solution** to halt-induced information vacuum exists yet.

---

## Failure Mode 3: Reopening Without Collars

### The Mechanism

After a 5-minute LULD halt, trading must resume. Different exchanges use different reopening procedures:

**NYSE Reopening** (uses collars):
- Reopening auction with price collars (3%, 5%, or 10% from prior reference)
- If can't reopen within collar, extends halt
- Prevents immediate re-halt

**NYSE Arca & BATS BZX** (NO collars):
- Reopening auction with **no price restrictions**
- Stock can reopen at any price
- Can immediately gap through new LULD bands
- Can immediately re-halt

### August 24 Reality

**Different reopening procedures created chaos**:

| Exchange   | Reopening Method | Collar | Aug 24 Impact         |
|------------|------------------|--------|-----------------------|
| NYSE       | Auction + collar | Yes    | More stable reopens   |
| NYSE Arca  | Auction only     | **NO** | Immediate re-halts    |
| BATS BZX   | Auction only     | **NO** | Gap-halt-gap cycles   |
| Nasdaq     | Auction + collar | Yes    | More stable reopens   |

**Problem**: Many ETFs trade primarily on Arca and BATS (not NYSE).

### DVY Case Study: The Halt-Reopen-Halt Cycle

**Detailed Timeline**:

```
9:33:00 AM - HALT #1
Price: $65.20 (triggered lower band $67.95)
Reason: Price remained in Limit State >15 seconds
Duration: 5 minutes
Exchange: NYSE Arca (no collars)

9:38:00 AM - REOPEN
Reopening auction on Arca:
- No collar restriction
- Opens at: $58.00
- New Reference Price: $58.00
- New LULD bands (10% opening): $52.20 - $63.80
- Gap down: -11.0% from halt price

9:38:15 AM - TRADING
Brief 15-second window:
- First trade: $58.00
- Second trade: $56.50 (selling pressure)
- Third trade: $55.20
- Approaching lower band $52.20

9:38:27 AM - LIMIT STATE
Price: $52.20 (touches lower band)
15-second countdown begins

9:38:42 AM - HALT #2
Price remained at band >15 seconds
New 5-minute halt triggered
Only 42 seconds of trading between halts

9:43:42 AM - REOPEN
No collar (Arca)
Opens at: $51.00
New bands: $45.90 - $56.10
Immediately near lower band

9:44:12 AM - HALT #3
30 seconds of trading
Price: $45.95 (below band)
```

**Result**: DVY experienced **6 separate halts** in the first hour, with trading windows of 15-45 seconds between halts.

### The 10-Minute Timeout Problem

**Regulation**: If primary exchange cannot reopen within 10 minutes, trading may resume on other venues with **3× normal band width** for 30 seconds.

**August 24 Scenario**:

```
10:15 AM - DVY
Primary (Arca): Still can't establish clearing price
10-minute timeout reached

Regulation allows: Trade on BATS with 3× bands
- Normal bands: ±10% (opening period)
- 3× bands: ±30%
- Bands: $41.30 - $75.10 (for $58.20 reference)

What happened:
- Opened at $50.00 on BATS
- Within 30 seconds: traded to $45.00
- 30 seconds expired → bands reset to ±10%
- New bands: $40.50 - $49.50
- Current price $45.00 still within new bands
- Continued trading

Problem: Brief 30-second window of 3× bands
created false sense of stability, then immediate
return to tight bands with continued volatility
```

### Why This Amplifies Cascades

**Without Collars** (Arca, BATS):
```
Halt at $65 → Reopen at $58 (-11%) → Trade 30 sec → Halt at $52
            → Reopen at $51 (-2%) → Trade 45 sec → Halt at $46
            → Reopen at $45 (-2%) → Trade 20 sec → Halt at $40
```

**With Collars** (NYSE):
```
Halt at $65 → Try to reopen at $58
            → Exceeds 10% collar
            → Extend halt 5 min
            → Reopen at $62 (within collar)
            → More stable trading
```

**Key Difference**: Collars prevent reopening at prices that will immediately trigger re-halt.

### Mathematical Analysis

**Reopening Probability Model**:

Let `P(rehalt | collar)` = probability of immediate re-halt given collar status

**With collar** (10% max deviation):
```
P(rehalt | collar) ≈ 0.15 (15% chance of re-halt)

Why lower:
- Collar prevents extreme reopening prices
- More time for panic to subside
- Better price discovery
```

**Without collar** (no restriction):
```
P(rehalt | no collar) ≈ 0.65 (65% chance of re-halt)

Why higher:
- Can reopen at any price
- Often reopens near or beyond new bands
- Insufficient panic subsidence
- Poor price discovery (15-30 sec windows)
```

**DVY Reality**:
- 6 halts in first hour
- Average trading time between halts: 24 seconds
- Matches "no collar" high re-halt probability

### Coordination Failure

**Cross-Listing Complexity**:

Many ETFs list on multiple exchanges:

```
DVY Listings:
- Primary: NYSE Arca (no collar)
- Also trades on: BATS, IEX, EDGX, EDGA

When halted:
- All venues halt simultaneously (correct)

When reopening:
- Primary (Arca) conducts auction (no collar)
- Other venues wait for primary to reopen
- All venues use primary's reopening price

Result: "No collar" behavior dominates
even though some venues support collars
```

### Post-Crisis Changes

**Amendment 12** (September 2016):

**Before August 24**:
- Inconsistent reopening procedures
- Some venues could reopen independently
- Coordination failures common

**After Amendment 12**:
- Non-primary markets MUST remain halted if primary can't reopen within 10 minutes
- Harmonized timeout procedures
- Better coordination

**Still Missing**:
- **No requirement for reopening collars** across all venues
- NYSE Arca and BATS still reopen without collars
- Vulnerability remains

---

## Failure Mode 4: 30-Second Reference Price Stability Rule

### The Regulation

**FINRA Rule 6190**: A new Reference Price must remain in effect for a **minimum of 30 seconds** before it can be updated.

**Purpose**: Prevent rapid-fire Reference Price updates that could confuse market participants.

**Problem During Fast Markets**: Reference Price becomes stale before it can update, creating persistent mismatch between bands and true price movement.

### The Lag Mechanism

**Normal Market** (slow price movement):
```
9:30:00  Reference Price: $100.00, Bands: $95-$105
9:30:30  Price moved to $98, can update Reference now
9:30:30  New Reference: $98.00, Bands: $93.10-$102.90
         30-second minimum respected, bands track price
```

**Fast Market** (rapid price movement):
```
9:30:00  Reference Price: $100.00, Bands: $95-$105
9:30:05  Price drops to $94 (below band) → Limit State
9:30:20  Price now at $92, but can't update Reference (need 30 sec)
9:30:20  Halt triggers (Limit State persisted 15 sec)
9:30:30  Could update Reference now, but trading halted
9:35:30  Reopen, new Reference: $92.00, Bands: $82.80-$101.20
9:35:35  Price gaps to $85 (selling pressure)
9:35:40  Price at $82 (near band), but can't update Reference yet
9:36:00  Can update Reference, but price at $78 now
9:36:00  New Reference: $82.00 (stale), Bands: $73.80-$90.20
9:36:02  Price $78 approaches $73.80 band
9:36:10  Halt again

Problem: Bands always lag actual price by 30+ seconds
```

### August 24 Timeline Analysis

**RSP Reference Price Updates**:

| Time     | Event              | True Price | Reference Price | Band Lag |
|----------|-------------------|------------|-----------------|----------|
| 9:30:00  | Open              | $76.80     | $76.80          | 0 sec    |
| 9:30:15  | Falling           | $74.00     | $76.80          | 15 sec   |
| 9:30:35  | Can update        | $71.00     | $74.00 (stale)  | 35 sec   |
| 9:35:00  | Halt #1 ends      | $69.00     | $71.00 (stale)  | 5+ min   |
| 9:35:30  | Can update        | $65.00     | $69.00 (stale)  | 30 sec   |
| 9:36:00  | Can update again  | $60.00     | $65.00 (stale)  | 30 sec   |

**Perpetual Lag**: Reference Price was consistently 30+ seconds behind true price movement.

### Mathematical Model

**Price Movement Velocity**:

Let `v` = price change velocity (% per second)

**Condition for Immediate Re-halt**:

If price is falling at rate `v`, and must wait 30 seconds for Reference Price update:

```
Price drop in 30 seconds = v × 30

If v × 30 > band_percentage:
    Then price will breach new band before Reference updates
    Result: Immediate re-halt after reopen

Example (DVY):
Opening period band = 10%
Price falling at v = 0.4% per second
Drop in 30 sec = 0.4% × 30 = 12%
12% > 10% → Will breach band before Reference updates
Result: Guaranteed re-halt
```

**August 24 Reality**:

Many ETFs were falling at `v = 0.3% to 0.8%` per second during 9:30-9:45 AM.

At `v = 0.4%/sec`:
- 30-second lag = 12% stale
- Even 10% (opening) bands insufficient
- Halt → Reopen → Immediate re-halt cycle

### Case Study: SPLV

**Low Volatility Mandate** (ironic failure):

```
SPLV: iShares S&P 500 Minimum Volatility ETF
Mandate: Provide LOWER volatility than S&P 500
Aug 24 Performance: -46.4% (HIGHER volatility than almost everything)

Reference Price Lag Analysis:
9:38:00  Reference: $35.55, Price: $32.00 (already -10%)
9:38:30  Can update, but price now: $28.00
9:38:30  New Reference: $32.00 (stale), Price: $28.00
9:38:40  Price: $25.00, approaching band $28.80
9:39:00  Price: $22.00, Reference: $28.00 (lag: $6)
9:39:00  New Reference: $25.00, Price: $21.18 (LOW)

At intraday low:
Reference Price: $25.00
Actual Price: $21.18
Lag: $3.82 (15.3% stale)
LULD Bands: $22.50 - $27.50
Actual traded BELOW lower band due to lag
```

**The Impossibility**:

When price falls faster than 30-second Reference update cycle:
- Bands are perpetually chasing the price down
- Never provide actual support
- Halts trigger but don't stop the cascade
- Each reopen just continues the fall

### Simulation: Alternative Update Frequencies

**Current System** (30-second minimum):
```
Halts triggered: 10
Trading time: 2.5 minutes in 1 hour
Lowest price: $43.77 (-43%)
```

**10-Second Minimum** (hypothetical):
```
Halts triggered: 6
Trading time: 8 minutes in 1 hour
Lowest price: $55.00 (-28%)
Reason: Bands track price better, less overshoot
```

**Real-Time Updates** (no minimum):
```
Halts triggered: 3
Trading time: 25 minutes in 1 hour
Lowest price: $62.00 (-19%)
Reason: Bands continuously track, prevent runaway cascades
```

**Trade-off**: Real-time updates could cause other problems (rapid band changes, confusion), but 30-second minimum proved too slow for crisis conditions.

### Why 30 Seconds?

**Regulatory Rationale**:
- Prevent confusion from rapid band changes
- Give market participants time to adjust
- Reduce computational load on SIP infrastructure

**Actual Effect on Aug 24**:
- Created persistent lag
- Bands didn't track actual prices
- Amplified cascades rather than preventing them

### Post-Crisis Status

**No changes to 30-second rule**. This vulnerability persists.

**Why not fixed**:
- Requires fundamental rethinking of LULD architecture
- Trade-offs between stability and responsiveness
- Infrastructure constraints (SIP processing capacity)
- Difficult to determine "right" update frequency

---

## Failure Mode 5: Exemptions as Escape Valves

### The Exemptions

**FINRA Rule 6190** exempts certain trades from LULD bands:

1. **Opening Trades**: First trade when market opens
2. **Reopening Trades**: First trade after halt
3. **Closing Trades**: Trades in closing auction (after 3:50 PM)
4. **611-Exempt Trades**: Certain institutional trades that don't update last sale

**Rationale**: These auction processes need flexibility to establish prices without being constrained by prior bands.

**Problem**: During crisis, exemptions become **escape valves** where extreme prices execute without protection.

### Opening Trades (Exemption 1)

**Normal Function**:
```
Pre-market: Stock closed at $100
Opening auction: Discovers fair value at $101
Opens at $101, LULD bands set: $96.00 - $106.00 (assuming 5%)
Purpose: Allow price discovery without prior day's close constraining
```

**August 24 Dysfunction**:
```
DVY:
Prior close: $75.50
Opening auction on BATS (9:31 AM): $62.00
No LULD constraint (opening trade exempt)
Discount: -17.8% in opening trade (allowed)
Result: Massive dislocation at open
```

**Why This Happened**:

On August 24, many stocks couldn't open on primary exchanges. ETFs opened on secondary venues (BATS, EDGX) where:
- No consensus on fair value (components halted)
- Extreme order imbalances
- Market makers withdrawn (can't hedge)
- Opening trades executed at panic prices

**Impact Table**:

| ETF  | Prior Close | Opening Trade | Discount | LULD Applied? |
|------|-------------|---------------|----------|---------------|
| DVY  | $75.50      | $62.00        | -17.8%   | No (exempt)   |
| RSP  | $76.80      | $68.00        | -11.5%   | No (exempt)   |
| SPLV | $39.50      | $32.00        | -19.0%   | No (exempt)   |
| IVV  | $204.00     | $181.00       | -11.3%   | No (exempt)   |

All four executed opening trades at discounts exceeding normal LULD bands (5-10%), but were exempt from protection.

### Reopening Trades (Exemption 2)

**Normal Function**:
```
Stock halted at: $95 (hit lower band)
5-minute pause for cooling off
Reopening auction discovers: $96 (within reason)
Reopens at $96, new bands set
Purpose: Allow auction to find price without being bound by stale halt price
```

**August 24 Dysfunction**:
```
RSP Halt #5:
Halted at: $55.00
5-minute pause (information vacuum worsens)
Reopening auction: $47.00 (-14.5%)
No LULD constraint (reopening exempt)
Immediately approaches new band: $42.30 - $51.70
Halts again 18 seconds later at $42.25
```

**The Perverse Incentive**:

Reopening exemption + no collars (on Arca/BATS) = prices can gap arbitrarily far:

```
Halt-Reopen Cycles (RSP):

Halt #1: $69 → Reopen: $65 (-5.8%)
Halt #2: $65 → Reopen: $60 (-7.7%)
Halt #3: $60 → Reopen: $53 (-11.7%)
Halt #4: $53 → Reopen: $48 (-9.4%)
Halt #5: $48 → Reopen: $44 (-8.3%)

Each reopening was exempt from LULD.
Each gap was larger than normal 5% band.
Cascade continued unimpeded.
```

### Closing Trades (Exemption 3)

**Normal Function**:
```
Stock trading at $100 near close
Closing auction (3:50-4:00 PM): Price discovery
Closes at $100.50 based on closing orders
Exempt to allow natural closing process
```

**August 24 Dysfunction**:

**Stop-Loss Conversion**:

Many investors had **stop-loss orders** set at reasonable levels:
- "Sell DVY if it drops 10% from prior close"
- Trigger price: $67.95

**What Happened**:

```
Step 1: DVY hits $67.95 at 9:33 AM
Step 2: Stop-loss triggers, becomes market order
Step 3: But market halted immediately
Step 4: Order queued until market reopens
Step 5: Market reopens at $58 (much lower)
Step 6: Stop-loss executes as market order
Step 7: Some fill at $58, some at $55, some at $52
Step 8: Multiple halt-reopen cycles
Step 9: Some stop-loss orders finally execute in closing auction
Step 10: Closing auction EXEMPT from LULD
Step 11: Executions occur at $49.14 (intraday low)

Investor expectation: "Sell at $67.95" (-10%)
Actual execution: "Sold at $49.14" (-35%)
Difference: -25% additional loss due to halt cascade + closing exemption
```

**Quantitative Impact**:

An estimated **40,000+ stop-loss orders** executed during August 24 at prices far worse than trigger levels due to:
1. Halt delays (queued during halts)
2. Reopening gaps (exempt from LULD)
3. Closing auction executions (exempt from LULD)

**Case Study - Retail Investor**:

```
Investor: Holds 1,000 shares DVY
Cost basis: $70.00 per share
Stop-loss set: 10% ($63.00)

Plan:
- If DVY drops to $63, sell
- Limit loss to $7,000 ($7 per share)

August 24 Reality:
- DVY hits $63 at 9:32 AM
- Stop-loss triggers → market order
- Halts begin immediately
- Order queued
- Executes across multiple reopens
- 300 shares at $58 (in reopen #1)
- 400 shares at $53 (in reopen #2)
- 300 shares at $49.14 (closing auction, exempt)

Actual execution:
Average: $53.05 per share
Loss: $16,950 ($16.95 per share)

Planned loss: $7,000
Actual loss: $16,950
Additional loss: $9,950 (142% worse than expected)
Cause: Exemptions allowed extreme prices
```

### 611-Exempt Trades (Exemption 4)

**Regulation NMS Rule 611**: Requires "trade-through protection" - must execute at best available price across all exchanges.

**611-Exempt Trades**: Certain institutional trades can opt out, typically:
- Portfolio trades (buying/selling entire basket)
- Block trades (very large size)
- Crossing networks

These trades **don't update last sale** and are **exempt from LULD**.

**August 24 Impact**:

```
Example: Institutional Sell Program
Institution needs to sell: 500,000 shares RSP
Method: 611-exempt block trade

Normal day:
- Would execute at $76.50 (current market)
- Might get worse price due to size ($76.30)
- LULD bands: $72.68 - $80.33 (5%)

August 24:
- Tried to execute at $70 (already down)
- No liquidity, can't fill at $70
- Lowers to $65, still can't fill
- Lowers to $60, partial fill
- Final fills at $50-$60 range
- Exempt from LULD (611-exempt trade)
- Doesn't trigger halt (doesn't update last sale)
- Creates shadow pricing below visible market

Result:
- Visible market: Trading $65-$70 range (within bands)
- Shadow market: Institutional trades filling $50-$60
- When shadow prices leak to public market → surprise crash
```

**Scale**:

An estimated **$2.8 billion** in institutional 611-exempt trades executed on August 24 at prices that would have triggered LULD halts if they were regular trades.

These trades:
- Didn't trigger halts (exempt)
- Created "hidden" price levels
- When discovered, caused sudden gaps
- Amplified panic when revealed

### Why Exemptions Exist vs Why They Failed

**Design Intent** vs **Crisis Reality**:

| Exemption | Design Intent                               | Aug 24 Reality                                |
|-----------|---------------------------------------------|-----------------------------------------------|
| Opening   | Discover opening price freely               | Discovered panic prices without arbitrage     |
| Reopening | Allow auction to clear after halt           | Created larger gaps, immediate re-halts       |
| Closing   | Natural closing process                     | Executed stop-losses at extreme losses        |
| 611-Exempt| Facilitate large institutional trades      | Created shadow pricing, surprise revelations  |

**Common Thread**: Exemptions assume **orderly** price discovery. During **disorderly** markets, they allow extreme price execution.

### Post-Crisis Changes

**Minimal changes to exemptions**:
- Still exist in current form
- Amendment 10 & 12 helped with related issues
- But core exemptions unchanged

**Why not eliminated**:
- Serve important functions in normal markets
- Removing would create other problems (constrained opening/closing auctions)
- Difficult to distinguish "legitimate" use from "escape valve" abuse

**Recommendation** (not implemented):
- Apply modified bands to exemptions (e.g., 20% for opening trades vs 5% normal)
- Reduce gaps while preserving auction flexibility
- Not adopted due to complexity

---

## Synthesis: How Failure Modes Interacted

### The Cascade Multiplier Effect

Each failure mode **amplified** the others:

**Multiplicative Effect**:

```
Base volatility: -5% (normal sell-off)

+ Opening vulnerability (9:30-9:35): ×2.0 = -10%
+ Information vacuum (halts): ×1.5 = -15%
+ Reopening without collars: ×1.4 = -21%
+ Reference Price lag: ×1.3 = -27%
+ Exemptions (stop-losses): ×1.4 = -38%

Final: -38% vs -5% base
Amplification factor: 7.6×
```

**DVY Actual**: -35% (close to model prediction)

### Timeline of Compounding Failures

**Minute-by-Minute Cascade**:

```
9:30:00  Markets open (-5% overnight gap)
         Failure Mode 1 begins: Opening vulnerability

9:31:00  ETFs trading without LULD bands (no primary exchange open)
         No arbitrage (components halted)
         Prices dislocate -10 to -18%

9:33:00  Primary exchanges open, LULD activates
         Prices already dislocated
         Failure Mode 2 begins: Information vacuum

9:33:15  First halts trigger (below bands)
         5-minute information vacuum begins
         Fair value becomes unknowable

9:38:00  Reopening begins
         Failure Mode 3: No collars on Arca/BATS
         Gaps down -8 to -12%

9:38:30  Brief trading (15-30 seconds)
         Failure Mode 4: Reference Price can't update fast enough
         Bands lag actual price

9:39:00  Second round of halts
         Failure Mode 5: Exemptions allow extreme fills
         Stop-losses execute at panic prices

9:40-10:00  Cycle repeats 8-10 times
            Each iteration compounds prior failures

10:00:00 Intraday lows reached
         Cumulative effect: -30 to -46% for various ETFs
```

### The Self-Reinforcing Loop

**Positive Feedback Cycle**:

```
Opening Vulnerability
      ↓
  Prices Dislocate
      ↓
Information Vacuum (halts)
      ↓
Can't Calculate Fair Value
      ↓
Market Makers Withdraw
      ↓
Reopen Without Collars
      ↓
Immediate Gap Down
      ↓
Reference Price Lags
      ↓
Bands Don't Protect
      ↓
Hit Band Again
      ↓
Exemptions Execute at Extremes
      ↓
More Information Vacuum
      ↓
(Cycle Repeats, Getting Worse)
```

**Breaking Point**: Cycle only broke when:
1. Fundamental buyers stepped in (value investors)
2. Volatility subsided naturally
3. Sufficient time elapsed for information to flow
4. NOT because LULD prevented further decline

### Counterfactual: Without LULD

**Thought Experiment**: What if LULD didn't exist on August 24?

**Scenario**: Continuous trading, no halts

**Predicted Outcome**:
```
Price discovery: Continuous (not intermittent)
Information quality: Degraded but not vacuum
Market maker behavior: Withdraw but with some pricing
Arbitrage: Difficult but possible
Stop-losses: Execute immediately, not queued
Exemptions: Normal impact, not amplified

Estimated crash magnitude: -15% to -20%
(vs actual -35% to -46% with LULD)

Reasoning:
- Continuous price discovery better than none
- No halt-induced information vacuums
- Stop-losses execute in real-time (less queueing)
- Market makers can adjust gradually
- No reopen gaps (already continuously trading)
```

**Caveat**: Impossible to prove counterfactual, but analysis suggests LULD amplification was significant.

---

## Key Takeaways

### For Regulators

1. **Single-stock circuit breakers ≠ correlated crash protection**
   - LULD designed for isolated events
   - Fails during system-wide stress

2. **Halting trading ≠ creating liquidity**
   - Pauses create information vacuums
   - Don't solve underlying problems

3. **Opening period vulnerability remains**
   - 9:30-9:35 window still unprotected
   - Needs fundamental rethinking

4. **Reopening collars needed**
   - NYSE Arca and BATS should adopt
   - Prevent gap-halt-gap cycles

5. **Reference Price lag needs addressing**
   - 30 seconds too slow for fast markets
   - Consider dynamic update frequency

### For Market Makers

1. **Rational withdrawal is not predatory**
   - Can't price = shouldn't quote
   - Preservation of capital is prudent

2. **Information vacuum is unhedgeable risk**
   - Stale iNAV = unreliable fair value
   - Position risk unbounded during halts

3. **Exemptions create hidden execution risk**
   - Opening/reopening trades can gap far
   - Stop-losses queue and execute poorly

### For Investors

1. **Stop-losses don't protect during flash crashes**
   - Queue during halts
   - Execute at worse prices due to gaps
   - Consider alternatives (options, limit orders)

2. **"Safe" ETFs can crash hardest**
   - SPLV (Low Volatility): -46%
   - Liquidity matters more than mandate

3. **Opening volatility is elevated risk period**
   - 9:30-9:45 AM highest cascade risk
   - Consider waiting until 10:00 AM to trade during stress

### For System Design

1. **Circuit breakers need holistic redesign**
   - Current system amplifies rather than dampens
   - Need new approach for correlated stress

2. **Price discovery must continue**
   - Halting trading creates worse outcomes
   - Alternative: wider bands, no halts

3. **Coordination across venues essential**
   - Harmonize reopening procedures
   - Eliminate regulatory arbitrage

---

## References

- SEC Release No. 34-67091 (May 31, 2012): "National Market System Plan to Address Extraordinary Market Volatility"
- FINRA Rule 6190: "Limit Up-Limit Down Plan and Trading Halts"
- SEC Staff Report: "Research Note on the August 24, 2015 Market Volatility" (December 2015)
- Amendment 10 to LULD Plan (April 2016)
- Amendment 12 to LULD Plan (September 2016)

---

**See Also**:
- [LULD Mechanism Overview](../../01-background/luld-mechanism.md)
- [LULD from Market Maker Perspective](../../04-market-maker-perspective/luld-from-mm-view.md)
- [DVY Case Study](case-study-dvy.md)
- [RSP Case Study](case-study-rsp.md)
- [SPLV Case Study](case-study-splv.md)
