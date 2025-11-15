# Extensions Track Notebooks

**Target Audience**: Quantitative analysts, market microstructure researchers, institutional traders, graduate students

**Prerequisites**:
- **REQUIRED**: Complete the Core Track first
- Python proficiency (NumPy, Pandas)
- Understanding of market microstructure concepts
- Familiarity with financial modeling
- Statistics/econometrics background helpful

**Learning Path**:

## 1. Market Maker Simulation
**File**: `01-market-maker-simulation.ipynb`

**What You'll Learn**:
- Market maker P&L calculation and risk management
- Hedging strategies and inventory constraints
- Spread widening dynamics during crisis
- Capital requirements for providing liquidity
- Break-even spread analysis

**Key Concepts**:
- Inventory risk and position limits
- Delta hedging with ETF vs underlying
- VaR, Expected Shortfall, Sharpe Ratio
- Market maker withdrawal triggers

**Time**: 90-120 minutes
**Difficulty**: ⭐⭐⭐⭐ Advanced

**Python Modules Used**: `market_maker_pnl.py`

---

## 2. Liquidity Microstructure Analysis
**File**: `02-liquidity-microstructure.ipynb`

**What You'll Learn**:
- Kyle's lambda (price impact coefficient)
- Amihud illiquidity measure
- Order book depth decay (power-law)
- Liquidity gap identification
- Stop-loss cascade mechanics

**Key Concepts**:
- Market impact models
- Price discovery vs liquidity provision
- Order flow toxicity
- Informed vs noise traders

**Time**: 90-120 minutes
**Difficulty**: ⭐⭐⭐⭐ Advanced

**Python Modules Used**: `order_book_dynamics.py`

**Academic References**:
- Kyle (1985): Continuous Auctions and Insider Trading
- Amihud (2002): Illiquidity and Stock Returns
- Glosten-Milgrom (1985): Bid-Ask Spreads

---

## 3. Research Questions (Coming Soon)
**File**: `03-research-questions.ipynb`

**What You'll Explore**:
- What capital was needed to prevent the crash?
- Alternative circuit breaker designs
- Optimal market maker obligations
- Network contagion pathways
- Systemic risk measurement

**Approach**: Open-ended explorations, no "correct" answers

**Time**: 2-4 hours
**Difficulty**: ⭐⭐⭐⭐⭐ Research-Level

**Python Modules Used**: All modules + extensions modules

---

## Advanced Features (Future)

### Adverse Selection Module
- Informed vs noise trader modeling
- Probability of Informed Trading (PIN)
- Glosten-Milgrom spread decomposition

### Inventory Optimization
- Avellaneda-Stoikov market making
- Optimal quoting strategies
- Dynamic programming solver

### Contagion Analysis
- Cross-asset correlation networks
- CoVaR and Marginal Expected Shortfall
- Feedback loop modeling

---

## Required Knowledge

Before starting the Extensions Track, ensure you understand:

### Market Microstructure:
- Bid-ask spread components (inventory, adverse selection, order processing)
- Market impact and price discovery
- Liquidity provision vs liquidity consumption

### Statistics:
- Regression analysis
- Time series (autocorrelation, volatility)
- Extreme value theory (helpful for tail risk)

### Risk Management:
- Value at Risk (VaR)
- Expected Shortfall (CVaR)
- Greeks (delta, gamma)
- Sharpe ratio and risk-adjusted returns

### ETF Mechanics:
- Creation/redemption process
- NAV vs iNAV
- Arbitrage boundaries
- Authorized Participants

---

## Recommended Readings

### Books:
1. **Market Microstructure Theory** - O'Hara (1995)
2. **Trading and Exchanges** - Harris (2003)
3. **Algorithmic and High-Frequency Trading** - Cartea et al. (2015)

### Papers:
1. Kyle (1985) - Continuous Auctions and Insider Trading
2. Glosten-Milgrom (1985) - Bid-Ask Spreads and Transaction Prices
3. Amihud (2002) - Illiquidity and Stock Returns: Cross-Section and Time-Series Effects
4. SEC (2015) - Research Note on August 24, 2015 Market Volatility

### Regulatory:
1. SEC LULD Plan (2012)
2. SEC Rule 611 (Regulation NMS)
3. FINRA Market Maker Rules

---

## Next Steps

After completing the Extensions Track:
1. Implement your own market microstructure models
2. Extend the code with additional features
3. Apply concepts to other flash crash events (2010, 2020)
4. Contribute to the repository with improvements
5. Publish research findings

## Getting Help

- Review academic papers cited in code docstrings
- Check [CONTRIBUTING.md](../../CONTRIBUTING.md) for code guidelines
- Open issues for technical questions
- Join discussions for research questions
