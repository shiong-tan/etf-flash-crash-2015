# How Market Makers Price ETFs

## Market Maker Role
- Provide continuous two-sided quotes (bid and ask) for ETFs
- Buy from sellers, sell to buyers, manage inventory
- Generate profit from bid-ask spread capture
- Manage risk through hedging and position management
- **No obligation** to provide liquidity—participation is voluntary and profit-motivated

## Fair Value Determination

**Normal Conditions:**
Market makers calculate ETF fair value using multiple inputs:

1. **iNAV (Intraday Indicative Value)**
   - Real-time estimate updated every 15 seconds
   - Last available price for each basket component
   - Most direct fair value reference

2. **Direct Pricing of Underlying Securities**
   - Cross-reference iNAV against actual constituent prices
   - Identify stale or questionable data points
   - Independent validation

3. **Futures and Derivatives**
   - S&P 500 E-Mini futures as proxy for equity ETFs
   - Options markets provide additional price signals
   - Multi-asset perspective reduces single-point failure risk

4. **Related Products**
   - Compare similar ETFs (SPY vs IVV vs VOO)
   - Sector ETF relationships
   - Statistical arbitrage signals

**Result:** Tight bid-ask spreads
- Liquid equity ETFs: 0.01-0.05% spreads
- Standard equity ETFs: 0.10-0.50% spreads
- Less liquid/complex products: wider spreads

## Hedging and Risk Management

**Delta Hedging:**
- Short underlying stocks when buying ETF shares
- Buy underlying stocks when selling ETF shares
- Eliminates directional market risk
- Leaves only spread revenue

**Gamma Management:**
- Use options to manage convexity risk
- Adjust delta hedges as market moves
- Protect against rapid price changes

**Cross-Asset Hedges:**
- Index futures for broad market exposure
- Sector ETFs for diversified positions
- Bonds, currencies, commodities for multi-asset ETFs
- Integrated approach across asset classes

## Creation/Redemption Arbitrage

**When ETF trades at premium above NAV:**
1. Authorized participant (AP) buys underlying basket in open market
2. Simultaneously shorts ETF shares to hedge
3. End of day: delivers basket to issuer
4. Receives new ETF shares (creation unit: 25,000-100,000 shares)
5. Uses new shares to cover short position
6. Profit = premium spread minus transaction costs

**When ETF trades at discount below NAV:**
1. AP buys undervalued ETF shares in market
2. Shorts underlying basket as hedge
3. End of day: delivers ETF shares to issuer
4. Receives basket of underlying securities
5. Uses securities to cover short positions
6. Profit = discount spread minus transaction costs

**Economics:**
- Typical spreads: 0.10-0.50% for equity ETFs
- Creation units: $2.5-10 million value
- Potential profit: $25,000-50,000 per cycle
- High-frequency traders work tighter spreads (0.01-0.05%) but execute thousands of cycles daily
- Transaction costs: 10-50 basis points (bid-ask spreads, exchange fees, market impact)

## Authorized Participant Requirements
- U.S. registered broker-dealer
- Self-clearing capability
- Full NSCC (National Securities Clearing Corporation) membership
- Full DTC (Depository Trust Company) membership
- Sufficient capital to handle multi-million dollar transactions
- **Critical: No contractual obligation to provide liquidity**
- APs participate voluntarily when profit opportunities exist

## Why This Matters for August 24, 2015

**Fair Value Calculation Broke Down:**
- iNAV relied on stale prices from halted stocks
- Underlying securities couldn't be priced accurately
- Futures hit limit down, providing no price signal
- Options markets were dislocated
- Normal toolkit of fair value inputs all failed simultaneously

**Hedging Became Impossible:**
- Can't short halted stocks for delta hedge
- Futures unavailable at limit down
- Options showed extreme skew and dislocation
- Taking ETF positions = unhedged directional risk
- Violated fundamental market-making principles

**Arbitrage Mechanisms Failed:**
- Couldn't simultaneously trade ETF and underlying basket
- RSP at $50 vs $71 iNAV looked like 30% arbitrage
- Reality: impossible to hedge, pure directional bet on stale data
- When arbitrage becomes speculation, rational APs withdraw

**Voluntary Nature Exposed:**
- Market makers have no obligation to catch falling knives
- Stepped away to preserve capital vs capture uncertain profits
- Liquidity vanished precisely when most needed
- Vicious cycle: volatility → uncertainty → withdrawal → reduced liquidity → more volatility

---

**See also:**
- [Hedging Under Stress](../04-market-maker-perspective/hedging-under-stress.md)
- [Jane Street Overview](../04-market-maker-perspective/jane-street-overview.md)
- [ETF Pricing Basics Notebook](../../notebooks/01-etf-pricing-basics.ipynb)
