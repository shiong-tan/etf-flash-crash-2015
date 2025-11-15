# Notebooks Directory

This directory contains Jupyter notebooks organized into two learning tracks:

## 📚 Two-Track Learning System

### **Core Track** → For General Learners
👥 **Who**: Students, educators, anyone curious about the flash crash
🎯 **Goal**: Understand what happened and why
⏱️ **Time**: 2-3 hours total
📖 **Path**: Start here if you're new to finance or market microstructure

[**→ Start Core Track**](core/)

---

### **Extensions Track** → For Quantitative Professionals
👥 **Who**: Quants, traders, researchers, grad students
🎯 **Goal**: Deep market microstructure analysis
⏱️ **Time**: 6-10 hours total
📖 **Path**: Complete Core Track first, then advance here

[**→ Start Extensions Track**](extensions/)

---

## Quick Navigation

| Track | Notebook | Topic | Difficulty | Time |
|-------|----------|-------|------------|------|
| **Core** | [01-understanding-the-crash](core/01-understanding-the-crash.ipynb) | ETF mechanics, crash timeline | ⭐ | 45-60min |
| **Core** | [02-real-market-data-analysis](core/02-real-market-data-analysis.ipynb) | Real data analysis | ⭐⭐ | 30-45min |
| **Core** | 03-hands-on-exercises | Interactive practice | ⭐⭐ | 60-90min |
| **Extensions** | 01-market-maker-simulation | MM P&L, hedging | ⭐⭐⭐⭐ | 90-120min |
| **Extensions** | 02-liquidity-microstructure | Kyle's lambda, Amihud | ⭐⭐⭐⭐ | 90-120min |
| **Extensions** | 03-research-questions | Open research | ⭐⭐⭐⭐⭐ | 2-4hrs |

---

## Which Track is Right for You?

### Choose **Core Track** if:
- ✅ You want to understand the flash crash at a high level
- ✅ You're learning Python for data analysis
- ✅ You don't need deep quantitative models
- ✅ You prefer intuition over equations
- ✅ You're teaching or learning about market structure

### Choose **Extensions Track** if:
- ✅ You completed the Core Track
- ✅ You have market microstructure knowledge
- ✅ You want to implement trading strategies
- ✅ You need production-ready risk models
- ✅ You're conducting academic research

---

## Directory Structure

```
notebooks/
├── README.md (you are here)
│
├── core/
│   ├── README.md
│   ├── 01-understanding-the-crash.ipynb
│   ├── 02-real-market-data-analysis.ipynb
│   └── 03-hands-on-exercises.ipynb
│
├── extensions/
│   ├── README.md
│   ├── 01-market-maker-simulation.ipynb
│   ├── 02-liquidity-microstructure.ipynb
│   └── 03-research-questions.ipynb
│
└── solutions/
    ├── core/
    │   └── 03-hands-on-exercises-solutions.ipynb
    └── extensions/
        └── (research questions have multiple valid approaches)
```

---

## Getting Started

### 1. Install Dependencies

**Core Track** (minimal):
```bash
pip install -r requirements.txt
```

**Extensions Track** (full):
```bash
pip install -r requirements-full.txt
```

### 2. Launch Jupyter

```bash
jupyter notebook
```

### 3. Navigate to Your Track

- **Core**: `notebooks/core/01-understanding-the-crash.ipynb`
- **Extensions**: `notebooks/extensions/01-market-maker-simulation.ipynb` (after Core)

---

## Google Colab Support

All notebooks support Google Colab with automatic setup:

1. Click "Open in Colab" badge at top of notebook
2. Notebook auto-detects Colab environment
3. Automatically clones repo and installs dependencies
4. Ready to run!

---

## Additional Resources

### Guide Files
Detailed explanations in [`guide/`](../guide/) directory:
- 01-background: ETF mechanics, LULD, market makers
- 02-the-event: Timeline, opening chaos
- 03-deep-dive: NAV disconnect, RSP case study
- 04-market-maker-perspective: Jane Street, hedging
- 05-aftermath: Regulatory changes, lessons

### Python Modules
Source code in [`src/`](../src/) directory:
- `etf_pricing.py`: NAV/iNAV calculations
- `order_book.py`: Basic order book simulation
- `order_book_dynamics.py`: Advanced flash crash modeling
- `market_maker_pnl.py`: Market maker simulation
- `visualization.py`: Plotting functions

### Test Data
Sample data in [`assets/data/`](../assets/data/):
- `aug24_price_data.csv`: Simulated Aug 24 prices
- `luld_halts.csv`: Trading halt timeline
- Real data fetched via yfinance in notebooks

---

## Learning Path Recommendations

### For Students (2-week plan):
- Week 1: Core notebooks + guide files
- Week 2: Hands-on exercises + additional case studies

### For Researchers (1-month plan):
- Week 1: Core track
- Week 2-3: Extensions track + implement own models
- Week 4: Research questions + extend codebase

### For Traders (1-week intensive):
- Day 1-2: Core track (quick review)
- Day 3-4: Extensions track (focus on market maker simulation)
- Day 5-7: Apply to your trading strategies

---

## Contributing

Found an error? Have suggestions? Want to add notebooks?

1. Check [CONTRIBUTING.md](../CONTRIBUTING.md)
2. Open an issue
3. Submit a pull request

---

## Citation

If you use these notebooks in research or teaching:

```bibtex
@software{etf_flash_crash_2015,
  title = {ETF Flash Crash 2015: Educational Analysis},
  author = {ETF Flash Crash Educational Project},
  year = {2024},
  url = {https://github.com/yourusername/etf-flash-crash-2015}
}
```

---

## Support

- 📖 Documentation: See main [README](../README.md)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/etf-flash-crash-2015/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/etf-flash-crash-2015/discussions)
- 📧 Contact: [Your contact info]

---

**Ready to learn?** → [Start with Core Track](core/) or [Jump to Extensions Track](extensions/)
