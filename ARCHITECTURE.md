# Architecture Documentation

**ETF Flash Crash 2015 Educational Project**

This document describes the codebase structure, module relationships, and design principles.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Module Architecture](#module-architecture)
- [Data Flow](#data-flow)
- [Extension Points](#extension-points)
- [Testing Strategy](#testing-strategy)
- [Development Guidelines](#development-guidelines)

---

## Project Overview

### Purpose

Educational repository for understanding the August 24, 2015 ETF flash crash through:
1. **Core Track**: Foundational concepts (NAV, arbitrage, order books)
2. **Extensions Track**: Advanced quantitative analysis (market microstructure, risk)

### Design Principles

1. **Educational First**: Code prioritizes clarity and pedagogy over performance
2. **Modular Design**: Independent modules that can be studied separately
3. **Progressive Complexity**: Simple → intermediate → advanced
4. **Production-Quality Code**: Despite educational focus, maintains professional standards
5. **Reproducibility**: All analysis can be reproduced with provided data/code

---

## Directory Structure

```
etf-flash-crash-2015/
│
├── src/                          # Source code modules
│   ├── __init__.py              # Package initialization and exports
│   ├── etf_pricing.py           # Core: NAV, iNAV, arbitrage calculations
│   ├── order_book.py            # Core: Basic order book mechanics
│   ├── order_book_dynamics.py   # Extensions: Advanced order book simulation
│   ├── market_maker_pnl.py      # Extensions: Market maker P&L modeling
│   ├── arbitrage_analysis.py    # Extensions: Arbitrage barrier analysis
│   ├── data_loader.py           # Extensions: Data loading utilities
│   ├── advanced_visualizations.py # Extensions: Advanced plotting
│   └── visualization.py         # Core: Basic plotting functions
│
├── tests/                        # Unit and integration tests
│   ├── conftest.py              # Pytest configuration
│   ├── test_etf_pricing.py      # Tests for pricing module
│   ├── test_order_book.py       # Tests for order book module
│   ├── test_order_book_dynamics.py
│   ├── test_market_maker_pnl.py
│   └── test_arbitrage_analysis.py
│
├── notebooks/                    # Jupyter notebooks (educational content)
│   ├── core/                    # Core track (3 notebooks)
│   │   ├── 01-etf-pricing-arbitrage.ipynb
│   │   ├── 02-order-book-mechanics.ipynb
│   │   └── 03-what-happened-august-24.ipynb
│   │
│   └── extensions/              # Extensions track (3 notebooks)
│       ├── 01-market-maker-simulation.ipynb
│       ├── 02-liquidity-microstructure.ipynb
│       └── 03-research-questions.ipynb
│
├── assets/                       # Supporting files
│   ├── data/                    # Sample data (synthetic/historical)
│   │   ├── aug24_price_data.csv
│   │   ├── luld_halts.csv
│   │   └── README.md
│   │
│   └── charts/                  # Pre-generated visualizations
│
├── docs/                         # Documentation
│
├── GLOSSARY.md                  # Financial and technical terms
├── ARCHITECTURE.md              # This file
├── README.md                    # Project introduction
├── requirements.txt             # Python dependencies
└── pyproject.toml              # Package configuration
```

---

## Module Architecture

### Core Modules (Required for Basic Understanding)

#### 1. `etf_pricing.py`
**Purpose**: NAV/iNAV calculations and arbitrage spread analysis

**Key Functions**:
- `calculate_nav()`: Compute ETF net asset value
- `calculate_inav()`: Real-time indicative NAV
- `arbitrage_spread()`: Calculate deviation from fair value
- `creation_profit()` / `redemption_profit()`: Arbitrage profitability
- `simulate_stale_inav()`: Model iNAV errors when components halt

**Dependencies**: None (pure functions)

**Used By**: All notebooks, arbitrage_analysis.py

---

#### 2. `order_book.py`
**Purpose**: Basic limit order book mechanics

**Key Classes**:
- `Order`: Dataclass for limit orders
- `OrderBook`: Simulates order book with bid/ask management

**Key Functions**:
- `add_bid()` / `add_ask()`: Add limit orders
- `execute_market_buy()` / `execute_market_sell()`: Execute market orders
- `execute_limit_buy()`: Execute limit orders
- `get_spread()` / `get_spread_bps()`: Calculate spreads

**Dependencies**: None

**Used By**: Core Track notebooks, order_book_dynamics.py

---

### Extension Modules (Advanced Analysis)

#### 3. `order_book_dynamics.py`
**Purpose**: Advanced order book simulation with market microstructure realism

**Key Classes**:
- `OrderBookSnapshot`: Point-in-time order book state
  - Methods: `spread_bps()`, `depth_at_distance()`, `price_impact()`

- `FlashCrashOrderBook`: Simulates realistic order book evolution
  - Methods: `simulate_market_maker_withdrawal()`, `execute_market_order()`, `simulate_stop_loss_cascade()`

**Key Functions**:
- `calculate_kyle_lambda()`: Price impact coefficient
- `calculate_amihud_illiquidity()`: Illiquidity measure
- `identify_liquidity_gaps()`: Detect air pockets in order book

**Dependencies**: `scipy` (for regression in Kyle's lambda)

**Used By**: Extensions Track notebooks

---

#### 4. `market_maker_pnl.py`
**Purpose**: Market maker P&L simulation and risk analysis

**Key Classes**:
- `HedgeStatus` (Enum): Full/Partial/None hedging availability
- `MarketMakerPosition`: Dataclass tracking inventory and hedges
  - Methods: `net_delta()`, `inventory_risk_usd()`, `gamma_risk()`

- `MarketMakerSimulator`: Simulate market maker behavior
  - Methods: `quote_market()`, `execute_trade()`, `mark_to_market()`, `calculate_risk_metrics()`

**Key Functions**:
- `simulate_market_maker_crisis()`: Full crisis simulation with timeline

**Dependencies**: None

**Used By**: Extensions Track notebook 01

---

#### 5. `arbitrage_analysis.py`
**Purpose**: Analyze why arbitrage failed during flash crash

**Key Classes**:
- `ArbitrageType` (Enum): Creation/Redemption/None
- `BarrierType` (Enum): Types of arbitrage barriers
- `ArbitrageOpportunity`: Dataclass representing arbitrage opportunity
  - Methods: `net_profit_per_share()`, `is_executable()`

- `ETFArbitrageAnalyzer`: Analyze arbitrage and identify barriers
  - Methods: `analyze_opportunity()`, `calculate_required_capital()`

**Key Functions**:
- `calculate_no_arbitrage_bounds()`: Price bounds where arbitrage unprofitable
- `identify_arbitrage_barriers()`: Analyze time series for barriers

**Dependencies**: `pandas`, `numpy`

**Used By**: Extensions Track analysis

---

#### 6. `data_loader.py`
**Purpose**: Load and generate data for analysis

**Key Classes**:
- `Aug24DataLoader`: Load/generate August 24, 2015 data
  - Methods: `load_etf_prices()`, `load_halt_log()`, `load_sp500_futures()`, `load_etf_holdings()`
  - Synthetic generation: `_generate_synthetic_etf_data()`, `_generate_synthetic_halt_data()`

**Key Functions**:
- `calculate_fair_value_timeline()`: Compute NAV time series from holdings

**Dependencies**: `pandas`, `numpy`

**Used By**: Extensions Track notebooks, data analysis scripts

---

#### 7. `advanced_visualizations.py`
**Purpose**: Publication-quality visualizations

**Key Functions**:
- `plot_liquidity_heatmap()`: Order book depth evolution
- `plot_multi_etf_comparison()`: Compare multiple ETFs
- `plot_stop_loss_waterfall()`: Visualize stop-loss cascade
- `plot_market_maker_spread_evolution()`: Spread widening dynamics
- `plot_halt_timeline_gantt()`: Trading halts timeline
- `plot_arbitrage_barrier_timeline()`: Barrier evolution

**Dependencies**: `matplotlib`, `seaborn`, `pandas`

**Used By**: Advanced analysis, report generation

---

#### 8. `visualization.py`
**Purpose**: Basic plotting functions for Core Track

**Key Functions**:
- `plot_price_vs_inav()`: ETF price vs iNAV over time
- `plot_order_book()`: Visual representation of order book
- `plot_luld_bands()`: Visualize LULD circuit breaker bands
- `plot_halt_timeline()`: Simple halt timeline

**Dependencies**: `matplotlib`, `pandas`

**Used By**: Core Track notebooks

---

## Data Flow

### Typical Analysis Workflow

```
1. Load Data
   └→ Aug24DataLoader.load_etf_prices('RSP')
   └→ Returns DataFrame with prices, volume, iNAV

2. Calculate Metrics
   ├→ calculate_nav(holdings, prices, shares_outstanding)
   ├→ arbitrage_spread(etf_price, inav)
   └→ ETFArbitrageAnalyzer.analyze_opportunity(...)

3. Simulate Market Dynamics
   ├→ FlashCrashOrderBook.simulate_market_maker_withdrawal(stress_level)
   ├→ MarketMakerSimulator.quote_market(fair_value, hedge_status, volatility)
   └→ simulate_stop_loss_cascade(initial_book, stop_triggers, initial_price)

4. Analyze Results
   ├→ calculate_kyle_lambda(trades_df, snapshots)
   ├→ calculate_amihud_illiquidity(prices, volumes)
   └→ identify_arbitrage_barriers(etf_prices, inav_values, ...)

5. Visualize
   ├→ plot_multi_etf_comparison(etf_data, fair_values)
   ├→ plot_liquidity_heatmap(snapshots, price_range, time_range)
   └→ plot_arbitrage_barrier_timeline(arbitrage_analysis)
```

### Module Dependencies

```
Visualization Layer
├── advanced_visualizations.py (optional: matplotlib, seaborn)
└── visualization.py (optional: matplotlib)

Analysis Layer
├── arbitrage_analysis.py (pandas, numpy)
├── market_maker_pnl.py (pandas, numpy)
└── order_book_dynamics.py (scipy, numpy, pandas)

Core Layer
├── order_book.py (no dependencies)
├── etf_pricing.py (no dependencies)
└── data_loader.py (pandas, numpy)
```

**Design**: Core modules have no dependencies, extensions require scipy/pandas, visualizations require matplotlib.

---

## Extension Points

### Adding New Analysis Modules

1. **Create module in `src/`**
   ```python
   # src/my_analysis.py
   """
   My custom analysis module.
   """

   def analyze_something(data):
       """Docstring with clear explanation."""
       # Implementation
       return results
   ```

2. **Add to `src/__init__.py`**
   ```python
   from .my_analysis import analyze_something

   __all__.extend(['analyze_something'])
   ```

3. **Create tests in `tests/`**
   ```python
   # tests/test_my_analysis.py
   from src.my_analysis import analyze_something

   def test_analyze_something():
       result = analyze_something(sample_data)
       assert result == expected_output
   ```

4. **Document in notebook**
   - Create `notebooks/extensions/04-my-analysis.ipynb`
   - Include educational explanations, examples, exercises

---

### Adding New Visualizations

1. **Add function to `advanced_visualizations.py` or create new module**
   ```python
   def plot_my_visualization(data: pd.DataFrame, **kwargs) -> plt.Figure:
       """
       Plot something useful.

       Args:
           data: Input data with columns ...
           **kwargs: Optional parameters

       Returns:
           matplotlib Figure
       """
       fig, ax = plt.subplots(...)
       # Implementation
       return fig
   ```

2. **Follow style guidelines**:
   - Publication-quality defaults
   - Clear axis labels and titles
   - Legends for multi-series plots
   - Docstring with example usage

---

### Adding Synthetic Data

1. **Extend `Aug24DataLoader` class**
   ```python
   def _generate_synthetic_new_data(self):
       """Generate new type of synthetic data."""
       # Base on known facts
       # Add realistic noise
       # Return DataFrame or dict
   ```

2. **Calibrate to known facts**:
   - Use SEC reports, academic papers for ground truth
   - Add variability around known data points
   - Document assumptions in docstring

---

## Testing Strategy

### Test Coverage Goals

- **Core modules**: >90% coverage
- **Extension modules**: >80% coverage
- **Integration tests**: All notebook cells execute without error

### Test Types

1. **Unit Tests** (`tests/test_*.py`):
   - Test individual functions
   - Edge cases and error handling
   - Input validation

2. **Integration Tests**:
   - Module interactions
   - End-to-end workflows
   - Notebook execution (via nbconvert)

3. **Property-Based Tests** (optional):
   - Use `hypothesis` for property testing
   - Example: NAV must always be positive

### Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/test_etf_pricing.py

# With coverage
pytest --cov=src tests/

# Verbose output
pytest -v
```

---

## Development Guidelines

### Code Style

- **PEP 8** compliance
- **Type hints** for all public functions
- **Docstrings** in Google style:
  ```python
  def function(arg1: float, arg2: int) -> Dict[str, float]:
      """
      Brief description.

      Detailed explanation of what the function does,
      any important algorithms or assumptions.

      Args:
          arg1: Description of arg1
          arg2: Description of arg2

      Returns:
          Description of return value

      Raises:
          ValueError: When input is invalid

      Example:
          >>> result = function(1.5, 10)
          >>> print(result)
          {'key': 1.5}
      """
  ```

### Error Handling

- **Validate inputs**: Check types, ranges, required fields
- **Descriptive errors**: Explain what went wrong and how to fix
- **Fail fast**: Don't continue with invalid data

Example:
```python
def calculate_nav(holdings, prices, shares_outstanding):
    if not holdings:
        raise ValueError("Holdings cannot be empty")
    if shares_outstanding <= 0:
        raise ValueError("Shares outstanding must be greater than zero")
    # ... implementation
```

### Performance Considerations

- **Vectorize** operations using numpy/pandas when possible
- **Avoid loops** over DataFrames (use `.apply()` or vectorized ops)
- **Cache** expensive computations when appropriate
- **Profile** before optimizing (use `cProfile` or `line_profiler`)

### Documentation

- **Module docstrings**: Explain purpose, main classes/functions
- **Function docstrings**: Args, returns, raises, examples
- **Inline comments**: Explain "why", not "what"
- **Notebooks**: Balance code, explanation, and exercises

---

## Module Relationships Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  (Jupyter Notebooks: Core Track & Extensions Track)         │
└────────────────┬─────────────────────────────────────┬──────┘
                 │                                     │
        ┌────────▼─────────┐                  ┌────────▼─────────┐
        │  Visualization   │                  │  Data Loading    │
        │  Modules         │                  │  Module          │
        │ • visualization  │                  │ • data_loader    │
        │ • advanced_viz   │                  │                  │
        └────────┬─────────┘                  └────────┬─────────┘
                 │                                     │
        ┌────────▼──────────────────────────────────────▼────────┐
        │             Analysis & Simulation Layer                │
        │ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
        │ │ arbitrage    │  │ market_maker │  │ order_book   │ │
        │ │ _analysis    │  │ _pnl         │  │ _dynamics    │ │
        │ └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
        └────────┼──────────────────┼──────────────────┼─────────┘
                 │                  │                  │
        ┌────────▼──────────────────▼──────────────────▼─────────┐
        │                  Core Modules Layer                     │
        │   ┌──────────────┐          ┌──────────────┐           │
        │   │ etf_pricing  │          │ order_book   │           │
        │   │ (NAV, iNAV)  │          │ (basic)      │           │
        │   └──────────────┘          └──────────────┘           │
        └─────────────────────────────────────────────────────────┘

Legend:
  ┌─────┐
  │     │  Module/Component
  └─────┘
     │     Dependency (uses)
     ▼     Direction of dependency
```

---

## Future Extensions

### Potential Additions

1. **Real Data Integration**
   - Bloomberg/Refinitiv API integration
   - SEC Edgar filings parser
   - TAQ (Trade and Quote) data loader

2. **Machine Learning Models**
   - Predict halt probability
   - Classify market regimes
   - Anomaly detection for flash crashes

3. **Network Analysis**
   - ETF correlation networks
   - Contagion modeling
   - Systemic risk measures

4. **Agent-Based Modeling**
   - Multi-agent market simulation
   - Emergent behavior analysis
   - Policy testing framework

5. **Interactive Dashboards**
   - Streamlit or Dash web interface
   - Real-time simulation controls
   - Parameter sensitivity analysis

---

## Contributing

### How to Contribute

1. **Fork** the repository
2. **Create feature branch**: `git checkout -b feature/my-feature`
3. **Add tests** for new functionality
4. **Update documentation** (docstrings, README, this file)
5. **Run tests**: `pytest`
6. **Submit pull request** with clear description

### Code Review Criteria

- Educational value
- Code quality and style
- Test coverage
- Documentation completeness
- Performance considerations

---

## Version History

- **v1.0.0** (Nov 2024): Initial release
  - Core Track complete (3 notebooks)
  - Extensions Track complete (3 notebooks)
  - 8 source modules with comprehensive tests
  - Full documentation (GLOSSARY, ARCHITECTURE, README)

---

*For term definitions, see [GLOSSARY.md](GLOSSARY.md)*

*Last updated: November 2024*
