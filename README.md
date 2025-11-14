# ETF Flash Crash 2015 – Educational Repository

A comprehensive learning resource explaining the ETF Flash Crash of August 24, 2015, when exchange-traded funds experienced catastrophic price dislocations despite functioning markets for their underlying securities.

---

## What Happened

On August 24, 2015, **302 of 1,569 ETFs triggered circuit breakers**, creating price dislocations so severe that major S&P 500 ETFs traded at discounts exceeding 40% while their underlying stocks fell only 3-5%. The event exposed critical vulnerabilities in ETF market structure and revealed how supposedly protective mechanisms can amplify rather than dampen crises.

### Key Facts

- **1,278 trading halts** across 471 securities in the first hour
- **RSP** (S&P 500 Equal Weight ETF, $9.5B AUM): Crashed from $76 to **$43.77** (43% decline) while underlying index fell only 4%
- **IVV** ($65B) and **SPY** tracked the same S&P 500 index but showed a **349-point discrepancy** at their lows
- Stop-loss orders executed **20-40% below trigger prices**, turning "protection" into devastation
- Market makers withdrew liquidity when hedging became impossible, amplifying the crisis
- Conservative "low volatility" products experienced the most extreme volatility

---

## What You'll Learn

This repository provides a structured learning path through the event, its causes, and its implications:

### Market Structure Fundamentals
- How ETFs actually work (NAV vs iNAV, creation/redemption mechanism)
- Market maker role and fair value determination
- Order types and their behavior during volatility
- Limit Up-Limit Down (LULD) circuit breakers

### The Event Itself
- Chronological timeline of August 24, 2015
- Why ETFs traded 30-40% below fair value
- Case studies: RSP dislocation and retail stop-loss failures
- Who was affected and how

### Market Maker Perspective
- Jane Street's role and competitive position
- Why hedging became impossible during the crisis
- How LULD circuit breakers constrained market-making
- Why liquidity vanished when most needed

### Aftermath and Lessons
- Limited regulatory response (Amendments 10 and 12 to LULD)
- Broker improvements and client education
- Lasting lessons for investors and market structure
- Why another flash crash remains possible

---

## Learning Path

This repository is designed for sequential learning. Start at the beginning and work through each section:

### 1. **Start Here: Background** (`guide/01-background/`)
Learn the foundational concepts you'll need to understand what went wrong.

- **[What Are ETFs?](guide/01-background/what-are-etfs.md)** – NAV vs iNAV, dual market structure, creation units
- **[Order Types Explained](guide/01-background/order-types.md)** – Market, limit, stop-loss, and their behavior during gaps
- **[LULD Mechanism](guide/01-background/luld-mechanism.md)** – Circuit breakers, price bands, trading halts
- **[How Market Makers Work](guide/01-background/how-market-makers-work.md)** – Fair value pricing, hedging, arbitrage

### 2. **The Story: What Happened** (`guide/02-the-event/`)
Follow the chronological narrative of August 24, 2015.

- **[Timeline](guide/02-the-event/timeline.md)** – Hour-by-hour breakdown from pre-open through recovery
- **[Pre-Crash Conditions](guide/02-the-event/pre-crash-conditions.md)** – Futures limit down, Rule 48, order buildup
- **[Opening Chaos](guide/02-the-event/opening-chaos.md)** – 1,278 halts, staggered openings, algorithmic breakdown
- **[Who Was Affected](guide/02-the-event/who-was-affected.md)** – Retail investors, advisors, market makers, institutions

### 3. **Deep Dive: Why It Happened** (`guide/03-deep-dive/`)
Understand the technical mechanisms that caused the dislocations.

- **[NAV Disconnect](guide/03-deep-dive/nav-disconnect.md)** – Why ETFs traded 38% below fair value
- **[Case Study: RSP](guide/03-deep-dive/case-study-rsp.md)** – $76 → $43.77: 10 halts in one hour
- **[Case Study: Retail Stop-Loss](guide/03-deep-dive/case-study-retail.md)** – How "protection" became catastrophe

### 4. **Inside View: Market Makers** (`guide/04-market-maker-perspective/`)
See the crisis from the perspective of firms providing liquidity.

- **[Jane Street Overview](guide/04-market-maker-perspective/jane-street-overview.md)** – 14% ETF volume, $41.6B capital, OCaml
- **[Role of Market Makers](guide/04-market-maker-perspective/role-of-market-makers.md)** – Continuous quoting, hedging, creation/redemption
- **[Hedging Under Stress](guide/04-market-maker-perspective/hedging-under-stress.md)** – Why RSP at $50 vs $71 wasn't arbitrage
- **[LULD from MM View](guide/04-market-maker-perspective/luld-from-mm-view.md)** – How circuit breakers prevented hedging

### 5. **Aftermath: What Changed (and Didn't)** (`guide/05-aftermath/`)
Examine the response and ongoing vulnerabilities.

- **[Regulatory Changes](guide/05-aftermath/regulatory-changes.md)** – Limited SEC response, Amendments 10 & 12
- **[Broker Reforms](guide/05-aftermath/broker-reforms.md)** – Order handling improvements, education campaigns
- **[Lasting Lessons](guide/05-aftermath/lasting-lessons.md)** – What we learned and what remains unfixed

### 6. **Hands-On: Interactive Exercises** (`notebooks/`)
Apply concepts through interactive Jupyter notebooks.

- **01-etf-pricing-basics.ipynb** – Calculate NAV/iNAV, creation arbitrage
- **02-order-book-simulation.ipynb** – Simulate air pockets, stop-loss cascades
- **03-luld-calculator.ipynb** – Calculate LULD bands, model halt triggers
- **04-rsp-case-analysis.ipynb** – Interactive analysis of RSP dislocation
- **05-volatility-patterns.ipynb** – Analyze August 24 volatility anomalies

---

## Installation

### Reading the Documentation
No installation needed! Simply browse the `guide/` directory in order.

### Running Interactive Notebooks

**Requirements:**
- Python 3.8 or higher
- Jupyter Notebook
- Libraries: numpy, pandas, matplotlib, seaborn, plotly

**Setup:**
```bash
# Clone the repository
git clone [repository-url]
cd etf-flash-crash-2015

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook notebooks/
```

---

## Repository Structure

```
etf-flash-crash-2015/
├── README.md                          # You are here
├── requirements.txt                   # Python dependencies
│
├── guide/                             # Educational documentation
│   ├── 01-background/                 # ETF mechanics, order types, LULD
│   ├── 02-the-event/                  # Timeline and what happened
│   ├── 03-deep-dive/                  # Technical analysis, case studies
│   ├── 04-market-maker-perspective/   # Jane Street and liquidity provision
│   └── 05-aftermath/                  # Reforms and lasting lessons
│
├── notebooks/                         # Interactive Jupyter exercises
│   ├── 01-etf-pricing-basics.ipynb
│   ├── 02-order-book-simulation.ipynb
│   ├── 03-luld-calculator.ipynb
│   ├── 04-rsp-case-analysis.ipynb
│   ├── 05-volatility-patterns.ipynb
│   └── solutions/                     # Exercise solutions
│
├── assets/                            # Visual aids and data
│   ├── charts/                        # SVG diagrams
│   └── data/                          # Sample datasets
│
├── src/                               # Python utilities
│   ├── etf_pricing.py                 # NAV/iNAV calculations
│   ├── order_book.py                  # Order book simulation
│   └── visualization.py               # Plotting helpers
│
└── tests/                             # Unit tests
    └── test_etf_pricing.py
```

---

## Prerequisites

### Required Knowledge
- Basic understanding of stock markets
- Familiarity with how stocks trade
- No prior ETF knowledge required (we'll teach you!)

### Optional but Helpful
- Python programming (for interactive notebooks)
- Basic statistics (for volatility analysis)
- Financial market microstructure (we cover the essentials)

---

## Key Takeaways

By the time you complete this repository, you'll understand:

### For Investors
- **Stop-loss orders = market orders** (no price protection after trigger)
- **Always use limit orders** for ETFs, especially during volatility
- **First/last 30 minutes** of trading day are most dangerous
- **Size provides no protection** during market structure failures
- **"Low volatility" labels** don't prevent dislocations

### For Market Structure
- **Voluntary liquidity provision** is fragile and withdraws under stress
- **Circuit breakers** can amplify rather than dampen problems
- **ETF price ≠ fair value** during crises, even for large mainstream products
- **Multiple safeguards failing simultaneously** creates catastrophic outcomes
- **Incremental improvements insufficient**; fundamental vulnerabilities remain

### For The Future
- **Another August 24 is possible** – same conditions could recur
- **Education helps individuals** but can't fix systemic problems
- **Prepare before crises**, not during them
- **Understand the mechanics** to recognize warning signs
- **Question assumptions** about market liquidity and safety

---

## Target Audience

This resource is designed for:

- **Retail investors** who use ETFs in their portfolios
- **Financial advisors** who recommend ETFs to clients
- **Finance students** studying market microstructure
- **Quantitative researchers** interested in market failure modes
- **Policymakers** evaluating regulatory responses
- **Anyone curious** about how modern markets can break

**Level:** Accessible to non-finance professionals, but comprehensive enough for experts.

---

## Data Sources and Accuracy

**Content is based on:**
- SEC Division of Economic and Risk Analysis research note (December 2015)
- Jane Street Capital public filings and interviews
- Exchange data and regulatory documents
- Academic research on the event
- Industry expert analysis

**Approach:**
- Historically accurate facts and figures
- Real examples (IUSV, RSP, DVY, SPLV, IVV)
- Simplified explanations without sacrificing technical accuracy
- Concise, bullet-point focused presentation

---

## Quick Start

**Ready to learn?**

1. **Start with [What Are ETFs?](guide/01-background/what-are-etfs.md)** if you're new to ETFs
2. **Jump to [Timeline](guide/02-the-event/timeline.md)** if you want the story first
3. **Read [Lasting Lessons](guide/05-aftermath/lasting-lessons.md)** if you want practical takeaways immediately
4. **Run notebooks** if you learn best by doing

**No matter where you start, prepare to question assumptions about market safety and liquidity.**

---

*This repository is a comprehensive educational resource about a specific historical event. It is not financial advice.*
