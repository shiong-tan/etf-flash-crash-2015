# ETF Flash Crash 2015 – Educational Repository

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/etf-flash-crash-2015/blob/master/notebooks/core/01-understanding-the-crash.ipynb)

A comprehensive, production-ready learning resource explaining the ETF Flash Crash of August 24, 2015, when exchange-traded funds experienced catastrophic price dislocations despite functioning markets for their underlying securities.

**Try it now in Google Colab** - Click the badge above to open the interactive notebook directly in your browser (no installation required!)

---

## 🎯 Quick Start

### Choose Your Learning Track:

**👥 Core Track** (3-5 hours) - ✅ Production Ready
- For students, educators, finance professionals
- Interactive Python notebooks + comprehensive guides
- Real market data analysis
- No advanced math required

**🎓 Extensions Track** (10-15 hours) - ⚠️ Work in Progress
- For quants, researchers, graduate students
- Advanced market microstructure
- Requires completing Core Track first
- Some notebooks need API corrections

**→ [Full Learning Path Guide](LEARNING_PATH.md)**

---

## What Happened

On August 24, 2015, **302 of 1,569 ETFs triggered circuit breakers**, creating price dislocations so severe that major S&P 500 ETFs traded at discounts exceeding 40% while their underlying stocks fell only 3-5%. The event exposed critical vulnerabilities in ETF market structure and revealed how supposedly protective mechanisms can amplify rather than dampen crises.

### Shocking Examples

| ETF | Assets | Strategy | Crash | Underlying |
|-----|--------|----------|-------|------------|
| **SPLV** | $5.8B | "Low Volatility" | **-46.4%** | -3.5% |
| **RSP** | $9.5B | Equal-Weight S&P 500 | -43.0% | -4.0% |
| **DVY** | $16.5B | Dividend Focus | -35.0% | -4.5% |
| **IVV** | $73B | S&P 500 | -16.1% | -4.0% |
| **SPY** | $185B | S&P 500 (same index!) | -8.1% | -4.0% |

**The Ultimate Irony**: The "Low Volatility" ETF (SPLV) was the **most volatile** security during the crash.

### Key Statistics

- **1,278 trading halts** across 471 securities in the first hour
- Stop-loss orders executed **20-40% below trigger prices**
- **$27.23 gap** between RSP price ($43.77) and iNAV ($71.00)
- Market makers withdrew when **60% of components** were halted (couldn't hedge)
- **IVV vs SPY divergence**: Same holdings, 8% different outcomes due to liquidity

---

## 📚 What You'll Learn

### Core Track (Production-Ready ✅)

#### Market Structure Fundamentals
- How ETFs actually work (NAV vs iNAV, creation/redemption)
- Market maker role and liquidity provision
- Order types and their behavior during volatility
- Limit Up-Limit Down (LULD) circuit breakers

#### The Event Itself
- Minute-by-minute timeline of August 24, 2015
- Why ETFs traded 30-40% below fair value despite accurate iNAV
- **New Case Studies**:
  - **DVY**: How "defensive" dividend ETF crashed 35%
  - **SPLV**: The "low volatility" -46% paradox
  - **SPY vs IVV**: Why liquidity matters more than fees
  - **RSP**: 43% crash with 500 stocks down only 4%

#### Hands-On Analysis
- ✅ Calculate NAV and iNAV for ETFs
- ✅ Simulate order book dynamics
- ✅ Analyze stop-loss cascades with real data
- ✅ Compare order type outcomes
- ✅ Portfolio stress testing

#### Lessons & Implications
- Why stop-loss orders backfired
- Liquidity premium quantified (400× expense ratio difference)
- Market structure vs individual failures
- How to protect portfolios

### Extensions Track (Advanced - ⚠️ WIP)

#### Market Maker Economics
- P&L calculation and inventory management
- Hedging strategies and VaR analysis
- Capital requirements
- Break-even spread calculations

#### Liquidity Microstructure
- Kyle's lambda (price impact)
- Amihud illiquidity measure
- Order flow toxicity
- Market impact models

#### Research Topics
- Adverse selection modeling
- Inventory optimization (Avellaneda-Stoikov)
- Contagion analysis
- Alternative circuit breaker designs

---

## 🚀 Getting Started

### Installation

**Minimal (Core Track)**:
```bash
git clone https://github.com/yourusername/etf-flash-crash-2015.git
cd etf-flash-crash-2015
pip install -r requirements.txt
```

**Full Experience (with visualizations)**:
```bash
pip install -r requirements-full.txt
```

**Google Colab** (no installation):
- Click "Open in Colab" badges in notebooks
- Automatic setup and dependency installation

### First Steps

**New to ETFs?** Start here:
1. Read [`guide/01-background/what-are-etfs.md`](guide/01-background/what-are-etfs.md)
2. Open [`notebooks/core/01-understanding-the-crash.ipynb`](notebooks/core/01-understanding-the-crash.ipynb)

**Finance Professional?** Jump to:
1. [`notebooks/core/03-hands-on-exercises.ipynb`](notebooks/core/03-hands-on-exercises.ipynb) (portfolio analysis)
2. Case studies in [`guide/03-deep-dive/`](guide/03-deep-dive/)

**Researcher/Quant?** Complete Core Track, then:
1. Review [`notebooks/extensions/README.md`](notebooks/extensions/README.md)
2. Study source code: [`src/market_maker_pnl.py`](src/market_maker_pnl.py)

---

## 📖 Repository Structure

```
etf-flash-crash-2015/
│
├── 📓 notebooks/              # Interactive Jupyter notebooks
│   ├── core/                 # ✅ General learners (PRODUCTION-READY)
│   │   ├── 01-understanding-the-crash.ipynb
│   │   ├── 02-real-market-data-analysis.ipynb
│   │   └── 03-hands-on-exercises.ipynb  ← Start here!
│   │
│   ├── extensions/           # ⚠️ Advanced (NEEDS WORK)
│   │   ├── 01-market-maker-simulation.ipynb (API corrections needed)
│   │   ├── 02-liquidity-microstructure.ipynb (planned)
│   │   └── 03-research-questions.ipynb (planned)
│   │
│   └── solutions/            # Exercise solutions
│       ├── core/
│       └── extensions/
│
├── 📚 guide/                  # Comprehensive written guides
│   ├── 01-background/        # ETFs, order types, LULD, market makers
│   ├── 02-the-event/         # Timeline, pre-crash, opening chaos
│   ├── 03-deep-dive/         # ✅ NEW CASE STUDIES
│   │   ├── case-study-dvy.md          (Dividend ETF -35%)
│   │   ├── case-study-splv.md         (Low-Vol -46% irony)
│   │   ├── comparison-spy-ivv.md      (Liquidity premium)
│   │   ├── case-study-rsp.md          (Equal-Weight -43%)
│   │   └── nav-disconnect.md
│   ├── 04-market-maker-perspective/
│   └── 05-aftermath/         # Regulatory changes, lessons
│
├── 🐍 src/                    # Python modules (production-ready)
│   ├── etf_pricing.py        # NAV/iNAV calculations
│   ├── order_book.py         # Basic order book
│   ├── order_book_dynamics.py  # Flash crash simulation (575 lines)
│   ├── market_maker_pnl.py   # Market maker modeling (549 lines)
│   └── visualization.py      # Plotting utilities
│
├── 🧪 tests/                  # Unit tests (108+ tests)
│   ├── test_etf_pricing.py
│   ├── test_order_book.py
│   ├── test_order_book_dynamics.py
│   └── test_market_maker_pnl.py
│
├── 📊 assets/data/            # Sample datasets
│   ├── aug24_price_data.csv
│   └── luld_halts.csv
│
├── 📋 LEARNING_PATH.md        # ✅ Comprehensive learning guide
├── 🤝 CONTRIBUTING.md         # How to contribute (coming soon)
└── 📄 requirements.txt        # Dependencies
```

---

## 🎓 Core Track: Complete Learning Path

### Step 1: Background (45 minutes)

**Essential Reading**:
- **[What Are ETFs?](guide/01-background/what-are-etfs.md)** (10 min)
  - NAV vs iNAV: Two ways to value an ETF
  - Creation/redemption mechanism
  - Why this matters for August 24

- **[Order Types Explained](guide/01-background/order-types.md)** (12 min)
  - Market vs limit orders
  - Stop-loss orders: intended protection vs actual disaster
  - Why stop-losses cascaded on August 24

- **[How Market Makers Work](guide/01-background/how-market-makers-work.md)** (15 min)
  - Continuous quoting and inventory management
  - Hedging strategies
  - Why they withdrew during the crash

**Optional**:
- [LULD Mechanism](guide/01-background/luld-mechanism.md) (8 min)

### Step 2: Interactive Notebooks (2-3 hours)

**Notebook 1: Understanding the Crash** (45-60 min)
- [`notebooks/core/01-understanding-the-crash.ipynb`](notebooks/core/01-understanding-the-crash.ipynb)
- ETF pricing mechanics
- August 24 timeline simulation
- Order book "air pockets"
- Circuit breaker effects

**Notebook 2: Real Market Data** (30-45 min)
- [`notebooks/core/02-real-market-data-analysis.ipynb`](notebooks/core/02-real-market-data-analysis.ipynb)
- Fetch actual August 24 data with yfinance
- Compare to COVID crash, SVB crisis
- Analyze volatility patterns

**Notebook 3: Hands-On Exercises** ✅ (60-90 min)
- [`notebooks/core/03-hands-on-exercises.ipynb`](notebooks/core/03-hands-on-exercises.ipynb)
- **Status**: Production-ready, all APIs correct
- 5 comprehensive exercises:
  1. NAV/iNAV calculation (normal vs flash crash)
  2. Order book simulation
  3. Stop-loss cascade analysis
  4. Arbitrage opportunity evaluation
  5. Portfolio stress testing

### Step 3: Deep Dive Case Studies (90 minutes)

**Required Reading** (choose at least 2):

**DVY (iShares Dividend ETF)** - [Read Case Study](guide/03-deep-dive/case-study-dvy.md)
- $16.5B "defensive" dividend fund crashed 35%
- Stop-loss massacre: 10% protection → 31% actual loss
- Retail investor impact: $200-400M in losses from stops alone

**SPLV (Low Volatility ETF)** - [Read Case Study](guide/03-deep-dive/case-study-splv.md)
- Ultimate irony: "low volatility" mandate, 46% crash
- Risk-averse investors suffered worst losses
- Defensive positioning backfired spectacularly

**SPY vs IVV Comparison** - [Read Analysis](guide/03-deep-dive/comparison-spy-ivv.md)
- Same index (S&P 500), massively different outcomes
- SPY: -8.1% | IVV: -16.1% (2× worse)
- Liquidity premium: 400× more valuable than fee savings
- Break-even: 40 years of fee savings = 1 flash crash spread cost

**RSP (Equal-Weight S&P 500)** - [Read Case Study](guide/03-deep-dive/case-study-rsp.md)
- 43% crash while 500 underlying stocks down only 4%
- 10 LULD halts in one hour (2.29 minutes actual trading)
- Why $27 arbitrage opportunity wasn't actionable

### Step 4: Timeline & Aftermath (30 minutes)

- **[August 24 Timeline](guide/02-the-event/timeline.md)** - Minute-by-minute breakdown
- **[Lessons Learned](guide/05-aftermath/lessons-learned.md)** - What changed
- **[Regulatory Response](guide/05-aftermath/regulatory-response.md)** - Limited reforms

---

## 🔬 Extensions Track (For Quantitative Professionals)

**Prerequisites**:
- ✅ Complete Core Track
- Python proficiency
- Market microstructure knowledge
- Statistics background

### Available Resources

**Production-Ready Python Modules**:
- ✅ `market_maker_pnl.py` (549 lines) - P&L calculation, inventory management
- ✅ `order_book_dynamics.py` (575 lines) - Flash crash simulation with LULD

**Notebooks** (⚠️ Need Work):
- ⚠️ `01-market-maker-simulation.ipynb` - API corrections needed
- 🚧 `02-liquidity-microstructure.ipynb` - Planned
- 🚧 `03-research-questions.ipynb` - Planned

**Planned Modules** (🚧 Not Yet Implemented):
- `src/extensions/adverse_selection.py` - Glosten-Milgrom, PIN
- `src/extensions/inventory_optimization.py` - Avellaneda-Stoikov
- `src/extensions/contagion_analysis.py` - CoVaR, network effects

**Status**: Infrastructure ready, notebooks need development

---

## 💡 Key Insights & Takeaways

### For Investors

1. **Stop-Loss Orders Are Dangerous in Gaps**
   - DVY: 10% intended protection → 31% actual loss
   - Use stop-limit orders or accept gap risk

2. **Liquidity Premium > Expense Ratio**
   - IVV saves 2 bps/year in fees
   - But cost 8% extra in flash crash (400:1 ratio)
   - Choose most liquid ETF in category

3. **"Safe" Assets Aren't Safe During Structure Failure**
   - SPLV ("low volatility"): -46%
   - DVY ("defensive dividend"): -35%
   - Market structure risk ≠ underlying asset risk

4. **ETF Price ≠ Fair Value During Stress**
   - RSP: $43.77 trading price vs $71 fair value
   - Even $185B SPY had 3.2% NAV disconnect
   - Size doesn't protect against dysfunction

### For Market Structure

5. **Liquidity is Voluntary and Conditional**
   - Market makers withdrew when couldn't hedge
   - Rational risk management, not predatory
   - No obligation to provide liquidity during dysfunction

6. **Circuit Breakers Can Amplify Crises**
   - LULD prevented continuous trading
   - Created information vacuum
   - Stopped hedging, price discovery

7. **iNAV Breaks Down When Components Halt**
   - Stale prices from halted stocks
   - "Garbage in, garbage out"
   - Market makers correctly didn't trust it

8. **Arbitrage Requires Hedging**
   - Can't arb RSP at $43.77 if 60% of stocks halted
   - "Free money" was unhedgeable speculation
   - Rational to pass when risk unknowable

---

## 📊 By the Numbers

### Event Statistics

- **302 ETFs** triggered circuit breakers
- **1,278 trading halts** in first hour
- **$1.2+ trillion** in affected ETF assets
- **5-30 seconds**: Average trading window between halts
- **20-40%**: Typical stop-loss execution slippage

### Educational Content

- **✅ 3 production-ready notebooks** (core track)
- **✅ 18 comprehensive guide files** (25,000+ words)
- **✅ 4 detailed case studies** (DVY, SPLV, SPY vs IVV, RSP)
- **✅ 2 production-ready Python modules** (1,100+ lines)
- **✅ 108+ unit tests** across 4 test files
- **⚠️ 3 extensions notebooks** (need work)
- **🚧 3 planned extension modules**

---

## 🤝 Contributing

We welcome contributions! The project is especially interested in:

**High Priority**:
- Fixing API usage in extensions notebooks
- Implementing planned extension modules
- Additional case studies (other ETFs, other countries)

**Medium Priority**:
- Improved visualizations
- Additional exercises and solutions
- Translation to other languages

**See**: `CONTRIBUTING.md` (coming soon) for guidelines

---

## 📚 Academic References

### Essential Reading

1. **SEC (2015)** - "Research Note on August 24, 2015 Market Volatility"
   - Official investigation and findings

2. **Kyle (1985)** - "Continuous Auctions and Insider Trading"
   - Market maker adverse selection

3. **Amihud (2002)** - "Illiquidity and Stock Returns"
   - Liquidity measurement

4. **Glosten-Milgrom (1985)** - "Bid-Ask Spreads and Transaction Prices"
   - Spread decomposition

### Additional Resources

- **Harris (2003)** - "Trading and Exchanges: Market Microstructure for Practitioners"
- **O'Hara (1995)** - "Market Microstructure Theory"
- **Cartea et al. (2015)** - "Algorithmic and High-Frequency Trading"

---

## 🙏 Acknowledgments

This educational project synthesizes:
- SEC research notes and regulatory filings
- Academic market microstructure literature
- Industry practitioner knowledge
- Real market data from August 24, 2015

All materials are provided for educational purposes.

---

## 📄 License

[Specify license - MIT, Apache 2.0, Creative Commons, etc.]

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/etf-flash-crash-2015/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/etf-flash-crash-2015/discussions)
- **Email**: [Your contact information]

---

## Citation

```bibtex
@software{etf_flash_crash_2015,
  title = {ETF Flash Crash 2015: Educational Analysis},
  author = {ETF Flash Crash Educational Project},
  year = {2024},
  url = {https://github.com/yourusername/etf-flash-crash-2015},
  note = {Core Track: Production-ready educational materials for understanding
          the August 24, 2015 ETF flash crash}
}
```

---

**Status**: Core Track production-ready ✅ | Extensions Track in development ⚠️

**Last Updated**: November 2024

**Start Learning**: [`notebooks/core/01-understanding-the-crash.ipynb`](notebooks/core/01-understanding-the-crash.ipynb) 🚀
