# Role of ETF Market Makers

## The Core Function

**Continuous Two-Sided Quoting:**
- Post bid prices (what they'll pay to buy)
- Post ask prices (what they'll charge to sell)
- Maintain quotes continuously throughout trading day
- Provide liquidity: ready buyer when investors want to sell, ready seller when investors want to buy

**Economic Model:**
- Revenue from bid-ask spread
- Example: Bid $100.00, Ask $100.05
- Buy at $100.00, sell at $100.05, capture $0.05 spread
- Repeat thousands of times daily
- Manage inventory and risk throughout

**Not Directional Bets:**
- Market makers don't bet on market direction (up/down)
- Aim to remain market-neutral through hedging
- Profit from providing liquidity, not from market moves
- Risk comes from inventory management, not directional exposure

---

## Fair Value Determination

**iNAV as Primary Reference:**
- Intraday indicative value updated every 15 seconds
- Last available price for each basket component
- Most direct measure of ETF fair value
- Market makers monitor iNAV constantly

**Cross-Validation Methods:**
1. **Direct underlying pricing** - Independent calculation from constituent prices
2. **Futures** - S&P 500 E-Mini futures for equity ETF benchmarks
3. **Options** - Implied prices from options markets
4. **Related ETFs** - Compare SPY vs IVV vs VOO (all track S&P 500)
5. **Statistical relationships** - Historical correlations and patterns

**Synthesizing Signals:**
- Multiple inputs provide confidence
- Disagreement among signals = uncertainty
- Wider spreads when uncertainty higher
- Tighter spreads when all signals align

**Quote Determination:**
- Fair value estimate: $100.00
- Transaction costs: $0.02
- Risk premium: $0.01
- Bid: $99.97, Ask: $100.03
- Spread: $0.06 (6 basis points)

---

## Hedging and Risk Management

**Delta Hedging (Primary Tool):**
- Buy ETF from client → simultaneously short underlying basket
- Sell ETF to client → simultaneously buy underlying basket
- Eliminates directional market risk
- Example: Buy 100,000 SPY shares → short S&P 500 futures or individual stocks
- Net position: market-neutral

**Gamma Management:**
- Delta changes as market moves (convexity)
- Use options to manage gamma risk
- Protect against rapid price changes
- Dynamic hedging adjusts positions continuously

**Inventory Management:**
- Accumulate ETF inventory throughout day
- Can't always hedge immediately (transaction costs)
- End of day: Create or redeem to flatten inventory
- Large inventory = higher risk = wider spreads

**Cross-Asset Hedging:**
- Equity ETFs: hedge with stocks, futures, options
- Bond ETFs: hedge with Treasuries, futures, swaps
- Commodity ETFs: hedge with futures, physical holdings
- International ETFs: hedge with local market instruments + currency forwards

---

## Authorized Participant (AP) Role

**Primary Market Operations:**
- APs can create and redeem ETF shares directly with issuer
- Creation: deliver basket of securities → receive ETF shares
- Redemption: deliver ETF shares → receive basket of securities
- Occurs end-of-day (around 4 PM), in-kind exchange

**Creation Process:**
1. ETF trades at **premium** (above NAV)
2. AP identifies arbitrage opportunity
3. Buy underlying securities in open market
4. Short ETF shares as hedge
5. End of day: deliver basket to issuer
6. Receive new ETF shares (creation unit: 25,000-100,000 shares)
7. Use new shares to cover short
8. Profit = premium spread minus transaction costs

**Redemption Process:**
1. ETF trades at **discount** (below NAV)
2. AP identifies arbitrage opportunity
3. Buy undervalued ETF shares in market
4. Short underlying basket as hedge
5. End of day: deliver ETF shares to issuer
6. Receive basket of underlying securities
7. Use securities to cover short
8. Profit = discount spread minus transaction costs

**Economics:**
- Creation units: $2.5-10 million value
- Typical spreads: 0.10-0.50% for equity ETFs
- Potential profit: $25,000-50,000 per cycle
- HFT firms work tighter spreads (0.01-0.05%) but higher volume
- Transaction costs: 10-50 basis points (must exceed this for profitability)

---

## Voluntary Nature of Liquidity Provision

**Critical Point: No Obligation**
- Market makers are **not required** to provide liquidity
- APs are **not required** to create or redeem
- Participation is **voluntary** and **profit-motivated**
- When conditions make activity too risky or unprofitable, they withdraw

**Requirements for AP Status:**
- U.S. registered broker-dealer
- Self-clearing capability
- Full NSCC (National Securities Clearing Corporation) membership
- Full DTC (Depository Trust Company) membership
- Sufficient capital for multi-million dollar transactions
- **But no obligation to actually transact**

**Why This Matters:**
- Liquidity appears deep during normal conditions
- Everyone assumes it will always be there
- **But liquidity is discretionary service, not guaranteed**
- During stress (like Aug 24), rational to withdraw
- **"Liquidity illusion" exposed during crises**

---

## Multiple Market Participants

**Lead Market Makers:**
- Designated by ETF issuer for each product
- Often multiple market makers per ETF (competition)
- Largest ETFs (SPY): dozens of market makers
- Smaller ETFs: maybe 1-3 market makers

**Jane Street's Position:**
- Lead market maker on ~640 U.S. ETFs (20% of market)
- But many other firms also provide ETF liquidity:
  - Citadel Securities
  - Virtu Financial
  - Flow Traders
  - GTS
  - Susquehanna (SIG)
  - Two Sigma
  - Traditional bank trading desks

**Competition Dynamics:**
- Tight spreads on high-volume ETFs (intense competition)
- Wider spreads on complex/illiquid products (fewer competitors)
- Jane Street dominates complex products where capital and sophistication matter most

---

## Normal Market Operation

**SPY Example (High Liquidity):**
- Dozens of market makers competing
- Bid-ask spread: 1 cent ($0.01) on $500 ETF = 0.002%
- Millions of shares of displayed liquidity
- Can trade $100 million with minimal market impact
- iNAV, futures, options all aligned
- Hedging instruments liquid and available
- **Appears perfectly efficient**

**Complex Bond ETF Example:**
- Fewer market makers (maybe 3-5)
- Bid-ask spread: 0.10-0.25%
- Less displayed liquidity
- Underlying bonds trade OTC (less liquid than stocks)
- More skill required to price and hedge
- Jane Street advantage stronger in these products

---

## What Makes Market Making Possible

**Four Requirements:**

**1. Accurate Fair Value:**
- Need reliable price signals
- iNAV must reflect current market
- Multiple cross-references available
- Confidence in valuation

**2. Hedging Capability:**
- Can trade underlying securities
- Derivatives markets functioning
- Able to eliminate directional risk
- Transaction costs acceptable

**3. Liquidity in Constituent Markets:**
- Underlying securities trading normally
- Sufficient depth to execute hedges
- Minimal market impact
- Predictable execution quality

**4. Profit Opportunity:**
- Spread exceeds transaction costs + risk premium
- Volume sufficient to generate revenue
- Risk acceptable relative to reward
- Capital available for positions

**When Any Requirement Fails:**
- Market makers widen spreads (compensation for uncertainty/risk)
- Or withdraw entirely if risk too high
- **On Aug 24, all four requirements failed simultaneously**

---

## August 24: When Market Making Became Impossible

**Fair Value Unknowable:**
- iNAV based on stale prices
- Underlying stocks halted or not opened
- Futures at limit down
- Options dislocated
- **No reliable reference for "true" ETF value**

**Hedging Impossible:**
- Can't short halted stocks
- Futures unavailable
- Options showing extreme skew
- **Taking ETF position = unhedged directional bet**

**Constituent Liquidity Gone:**
- Hundreds of stocks not trading
- Those trading showing huge gaps
- Order books sparse
- **Can't execute hedges even if wanted to**

**Profit Uncertain, Risk Unlimited:**
- Spread at $50 vs $71 iNAV looks profitable
- But is $71 accurate or mirage?
- If wrong, potential loss hundreds of millions
- **"Arbitrage" actually speculation on stale data**

**Rational Response: Withdraw**
- Preserve capital
- Wait for hedging to become possible
- Resume when fair value calculable
- **But withdrawal amplified crisis**

---

## The Liquidity Provision Dilemma

**Social Function:**
- Market makers provide valuable service
- Enable investors to trade when needed
- Price discovery through continuous quoting
- Stabilize markets during normal volatility

**Private Risk:**
- Market makers are private, for-profit businesses
- Owe duty to shareholders/partners, not to market stability
- Must manage risk prudently
- Survival takes priority over public service

**Conflict on August 24:**
- Markets **needed** liquidity most during crisis
- Providing liquidity was **most dangerous** during crisis
- Social need and private incentive misaligned
- **No regulatory obligation to maintain markets**

**Result:**
- Market makers withdrew when most needed
- Vicious cycle: withdrawal → reduced liquidity → worse volatility → more withdrawal
- Exposed fundamental fragility in voluntary liquidity model

---

**See also:**
- [Jane Street Overview](jane-street-overview.md)
- [Hedging Under Stress](hedging-under-stress.md)
- [How Market Makers Price ETFs](../01-background/how-market-makers-work.md)
