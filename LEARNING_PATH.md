# Learning Path Guide

**ETF Flash Crash 2015: Educational Analysis**

This guide helps you navigate the repository based on your background and learning goals.

---

## 📚 Quick Start by User Type

### 👥 Students & Educators
**Goal**: Understand what happened and why
**Time**: 3-5 hours
**Path**: Core Track → Case Studies

**Start here**: [`notebooks/core/01-understanding-the-crash.ipynb`](notebooks/core/01-understanding-the-crash.ipynb)

### 💼 Finance Professionals & Traders
**Goal**: Apply lessons to portfolio risk management
**Time**: 6-8 hours
**Path**: Core Track → Case Studies → Portfolio Analysis

**Start here**: [`notebooks/core/README.md`](notebooks/core/README.md)

### 🎓 Researchers & Quants
**Goal**: Deep market microstructure analysis
**Time**: 15-20 hours
**Path**: Full Core Track → Extensions Track → Source Code

**Start here**: Complete Core Track, then [`notebooks/extensions/README.md`](notebooks/extensions/README.md)

### 🏫 Teachers Preparing Course Materials
**Goal**: Adapt content for classroom use
**Time**: 2-3 hours review
**Resources**: Guide files + Core notebooks (all have teaching notes)

**Start here**: [`guide/README.md`](guide/README.md)

---

## 🎯 Learning Tracks

### **Core Track** (Production-Ready ✅)

**Target Audience**: General learners, students, finance professionals

**Prerequisites**:
- Basic understanding of stocks and ETFs
- Python basics (helpful but not required)
- No math/finance background needed

**Time Commitment**: 2-3 hours

**Learning Path**:

#### 1. Background Concepts (30-45 minutes)
Start with foundational knowledge:

- **[What Are ETFs?](guide/01-background/what-are-etfs.md)** (10 min)
  - NAV vs iNAV calculation
  - Creation/redemption mechanism
  - Dual market structure

- **[Order Types Explained](guide/01-background/order-types.md)** (12 min)
  - Market orders vs limit orders
  - Stop-loss orders (critical for crash understanding)
  - Why stop-losses cascaded on August 24

- **[How Market Makers Work](guide/01-background/how-market-makers-work.md)** (15 min)
  - Role in providing liquidity
  - Inventory management
  - Why they withdrew on August 24

#### 2. Interactive Notebooks (90-120 minutes)

**Notebook 01: Understanding the Crash** (45-60 min)
- [`notebooks/core/01-understanding-the-crash.ipynb`](notebooks/core/01-understanding-the-crash.ipynb)
- ETF pricing mechanics
- August 24, 2015 timeline
- LULD circuit breakers
- Order book dynamics

**Notebook 02: Real Market Data Analysis** (30-45 min)
- [`notebooks/core/02-real-market-data-analysis.ipynb`](notebooks/core/02-real-market-data-analysis.ipynb)
- Fetch historical data with yfinance
- Analyze actual August 24 prices
- Compare to other crashes (COVID, SVB)

**Notebook 03: Hands-On Exercises** ✅ (60-90 min)
- [`notebooks/core/03-hands-on-exercises.ipynb`](notebooks/core/03-hands-on-exercises.ipynb)
- Calculate NAV and iNAV
- Simulate order books
- Analyze stop-loss cascades
- Compare order type outcomes
- **Status**: Production-ready with correct API usage

#### 3. Deep Dive Case Studies (60-90 minutes)

**DVY (Dividend ETF)** - [Case Study](guide/03-deep-dive/case-study-dvy.md)
- 35% intraday crash despite "defensive" positioning
- Stop-loss massacre: intended 10% loss → actual 31% loss
- Retail investor impact analysis

**SPLV (Low Volatility ETF)** - [Case Study](guide/03-deep-dive/case-study-splv.md)
- Ultimate irony: "low volatility" fund dropped 46%
- Risk-averse investor paradox
- How defensive positioning backfired

**SPY vs IVV Comparison** - [Analysis](guide/03-deep-dive/comparison-spy-ivv.md)
- Same index, 2× different crash severity
- Liquidity premium: worth 400× expense ratio savings
- Market maker infrastructure differences

**RSP (Equal-Weight S&P 500)** - [Case Study](guide/03-deep-dive/case-study-rsp.md)
- 43% crash (500 stock index down only 4%)
- Why arbitrage broke down
- Hedging impossibility

#### 4. Timeline & Aftermath (30 minutes)

- **[August 24 Timeline](guide/02-the-event/timeline.md)** - Minute-by-minute breakdown
- **[Lessons Learned](guide/05-aftermath/lessons-learned.md)** - What changed afterward
- **[Regulatory Response](guide/05-aftermath/regulatory-response.md)** - Rule changes

---

### **Extensions Track** (Advanced - Work in Progress ⚠️)

**Target Audience**: Quantitative professionals, researchers, graduate students

**Prerequisites**:
- ✅ **REQUIRED**: Complete Core Track first
- Python proficiency (NumPy, Pandas)
- Market microstructure knowledge
- Statistics/econometrics background
- Familiarity with options Greeks, VaR, Sharpe ratio

**Time Commitment**: 10-15 hours

**Status**:
- ✅ Infrastructure ready (modules exist)
- ⚠️ Notebooks need API corrections
- 🚧 Some modules planned but not implemented

**Learning Path**:

#### 1. Market Maker Simulation ⚠️
- **Notebook**: [`notebooks/extensions/01-market-maker-simulation.ipynb`](notebooks/extensions/01-market-maker-simulation.ipynb)
- **Status**: Draft - needs API fixes before usable
- **Topics**: P&L calculation, inventory management, hedging strategies, VaR analysis
- **Module**: `src/market_maker_pnl.py` (549 lines, production-ready)

#### 2. Liquidity Microstructure 🚧
- **Notebook**: `notebooks/extensions/02-liquidity-microstructure.ipynb` (planned)
- **Status**: Not yet created
- **Topics**: Kyle's lambda, Amihud measure, order flow toxicity
- **Module**: `src/order_book_dynamics.py` (575 lines, production-ready)

#### 3. Research Questions 🚧
- **Notebook**: `notebooks/extensions/03-research-questions.ipynb` (planned)
- **Status**: Not yet created
- **Topics**: Open-ended explorations, no "correct" answers
- **Examples**:
  - What capital was needed to prevent the crash?
  - Alternative circuit breaker designs
  - Optimal market maker obligations

#### 4. Advanced Modules (Planned) 🚧

**Adverse Selection** - `src/extensions/adverse_selection.py`
- Probability of Informed Trading (PIN)
- Glosten-Milgrom spread decomposition
- Informed vs noise trader modeling

**Inventory Optimization** - `src/extensions/inventory_optimization.py`
- Avellaneda-Stoikov market making model
- Optimal quoting strategies
- Dynamic programming solver

**Contagion Analysis** - `src/extensions/contagion_analysis.py`
- Cross-asset correlation networks
- CoVaR and Marginal Expected Shortfall
- Feedback loop modeling

---

## 🗓️ Recommended Schedules

### One-Day Intensive (6-8 hours)

**For**: Professionals needing quick understanding

**Morning (3-4 hours)**:
1. Background reading (45 min): ETFs, order types, market makers
2. Notebook 01 (60 min): Understanding the crash
3. Notebook 02 (45 min): Real data analysis
4. Notebook 03 (90 min): Hands-on exercises

**Afternoon (3-4 hours)**:
5. Case studies (90 min): DVY, SPLV, SPY vs IVV
6. Timeline & aftermath (30 min)
7. Review source code (60 min): `order_book_dynamics.py`, `market_maker_pnl.py`

---

### Two-Week Course (10-15 hours total)

**For**: University courses, study groups

**Week 1: Foundations**
- **Day 1-2**: Background reading + Notebook 01
- **Day 3**: Notebook 02 (real data analysis)
- **Day 4-5**: Notebook 03 (hands-on exercises)

**Week 2: Deep Dive**
- **Day 1**: Case studies (DVY, SPLV)
- **Day 2**: Case studies (SPY vs IVV, RSP)
- **Day 3**: Market maker perspective
- **Day 4**: Timeline and regulatory aftermath
- **Day 5**: Discussion and synthesis

---

### One-Month Research Project (30-40 hours)

**For**: Graduate students, researchers

**Week 1: Core Track** (10 hours)
- Complete all core notebooks
- Read all guide files
- Review source code

**Week 2: Extensions Track** (10 hours)
- Study `market_maker_pnl.py` and `order_book_dynamics.py`
- Attempt extensions notebooks (note: may need fixes)
- Implement custom simulations

**Week 3: Original Research** (10 hours)
- Extend codebase with new models
- Apply concepts to other flash crash events
- Analyze alternative market structures

**Week 4: Writing & Synthesis** (10 hours)
- Document findings
- Create visualizations
- Prepare presentation or paper

---

## 📊 Learning Objectives by Track

### Core Track Learning Objectives

By the end of the Core Track, you will be able to:

**Conceptual Understanding**:
- ✅ Explain how ETFs are priced (NAV vs iNAV)
- ✅ Describe the creation/redemption mechanism
- ✅ Identify when iNAV calculations become unreliable
- ✅ Understand LULD circuit breaker mechanics
- ✅ Explain why market makers withdrew liquidity

**Practical Skills**:
- ✅ Calculate NAV and iNAV for ETF portfolios
- ✅ Simulate order book dynamics
- ✅ Analyze the impact of different order types
- ✅ Identify arbitrage opportunities and limitations
- ✅ Assess portfolio risk during market stress

**Critical Thinking**:
- ✅ Evaluate the trade-offs of stop-loss orders
- ✅ Understand why "obvious" arbitrage wasn't exploited
- ✅ Recognize market structure vs individual failures
- ✅ Apply lessons to current portfolio management

---

### Extensions Track Learning Objectives

By the end of the Extensions Track, you will be able to:

**Quantitative Skills**:
- ⚠️ Model market maker P&L and inventory risk
- 🚧 Calculate liquidity metrics (Kyle's lambda, Amihud)
- 🚧 Implement adverse selection models
- 🚧 Optimize market making strategies

**Research Capabilities**:
- 🚧 Design and execute market microstructure experiments
- 🚧 Extend existing models with new features
- 🚧 Analyze systemic risk and contagion
- 🚧 Contribute to academic/industry literature

---

## 🛠️ Technical Prerequisites

### Core Track

**Python Environment**:
```bash
# Minimal installation
pip install -r requirements.txt
# Includes: numpy, pandas, scipy
```

**Optional (for full experience)**:
```bash
# Full installation with visualizations
pip install -r requirements-full.txt
# Adds: matplotlib, seaborn, plotly, jupyter, yfinance
```

**No Visualization**:
- Core modules work without matplotlib
- Can run calculations programmatically
- Good for automated testing or minimal environments

---

### Extensions Track

**Required**:
```bash
pip install -r requirements-full.txt
```

**Additional (for advanced modules)**:
- Statistical libraries (scipy, statsmodels)
- Network analysis (networkx) - for contagion module
- Optimization libraries (cvxpy) - for inventory optimization

---

## 📈 Assessment & Validation

### Self-Assessment Questions

**After Core Track**:

1. Why did iNAV calculations fail during the flash crash?
2. How do stop-loss orders differ from stop-limit orders?
3. Why couldn't market makers arbitrage RSP at $43.77 vs iNAV $71?
4. What's the difference between SPY and IVV flash crash experiences?
5. How would you protect a portfolio from similar events?

**After Extensions Track**:

1. Calculate break-even spread for a market maker with $500K VaR
2. Why do market makers skew quotes based on inventory?
3. How does adverse selection increase during volatility?
4. What capital is required for market making 50K shares/day?
5. Design a circuit breaker that avoids August 24 problems

---

### Practical Exercises

**Core Level**:
- Complete all TODO sections in Notebook 03
- Replicate DVY stop-loss analysis for another ETF
- Build custom portfolio and stress-test it

**Extensions Level**:
- Implement alternative inventory management strategies
- Model market maker P&L for multi-day simulation
- Analyze contagion between correlated ETFs

---

## 🔗 External Resources

### Academic Papers

**Essential Reading**:
1. SEC (2015) - "Research Note on August 24, 2015 Market Volatility"
2. Kyle (1985) - "Continuous Auctions and Insider Trading"
3. Amihud (2002) - "Illiquidity and Stock Returns"

**Advanced**:
4. Glosten-Milgrom (1985) - "Bid-Ask Spreads and Transaction Prices"
5. Avellaneda-Stoikov (2008) - "High-Frequency Trading in a Limit Order Book"

### Books

**For Core Track**:
- Harris (2003) - "Trading and Exchanges: Market Microstructure for Practitioners"
- Hasbrouck (2007) - "Empirical Market Microstructure"

**For Extensions Track**:
- O'Hara (1995) - "Market Microstructure Theory"
- Cartea et al. (2015) - "Algorithmic and High-Frequency Trading"

### Regulatory Documents

- SEC Limit Up-Limit Down Plan (2012)
- FINRA Market Maker Rules
- SEC Rule 611 (Regulation NMS)

---

## 🤝 Getting Help

### Issues & Questions

- **Technical issues**: [GitHub Issues](https://github.com/yourusername/etf-flash-crash-2015/issues)
- **Conceptual questions**: [GitHub Discussions](https://github.com/yourusername/etf-flash-crash-2015/discussions)
- **Errors in content**: Open an issue with specific file/line reference

### Contributing

- See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines
- Extensions track welcomes contributions (notebooks, modules, tests)
- Case studies for other ETFs encouraged

---

## 📝 Certification & Citation

### For Academic Use

If using this material in courses or research:

```bibtex
@software{etf_flash_crash_2015,
  title = {ETF Flash Crash 2015: Educational Analysis},
  author = {ETF Flash Crash Educational Project},
  year = {2024},
  url = {https://github.com/yourusername/etf-flash-crash-2015}
}
```

### Teaching Materials

Educators: All materials are open for classroom use. Please:
- Cite the repository
- Share feedback on what worked/didn't work
- Contribute improvements back to the project

---

## ✅ Completion Checklist

### Core Track
- [ ] Read background guides (ETFs, order types, market makers)
- [ ] Complete Notebook 01 (Understanding the Crash)
- [ ] Complete Notebook 02 (Real Market Data)
- [ ] Complete Notebook 03 (Hands-On Exercises)
- [ ] Read at least 2 case studies
- [ ] Review August 24 timeline
- [ ] Understand lessons learned & regulatory response

### Extensions Track
- [ ] Complete Core Track (required)
- [ ] Study `market_maker_pnl.py` source code
- [ ] Study `order_book_dynamics.py` source code
- [ ] Attempt market maker simulation (⚠️ may need fixes)
- [ ] Implement custom market microstructure model
- [ ] Read academic papers (Kyle, Amihud, Glosten-Milgrom)
- [ ] Contribute to repository (optional)

---

## 🎓 Next Steps After Completion

### Apply to Other Events
- Flash Crash 2010 (Dow Jones)
- COVID-19 Crash (March 2020)
- Meme Stock Volatility (2021)
- SVB Crisis (March 2023)

### Career Applications
- **Risk Management**: Improve portfolio stress testing
- **Trading**: Understand liquidity risk in execution
- **Regulation**: Inform circuit breaker design
- **Research**: Publish market microstructure papers

### Share Your Learning
- Write blog post summarizing lessons
- Present to study group or colleagues
- Contribute case study for different ETF
- Extend codebase with new features

---

**Good luck with your learning journey! 🚀**

*Last Updated: 2024 | Status: Core Track production-ready, Extensions Track in development*
