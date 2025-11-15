"""
ETF Flash Crash 2015 - Educational Utilities

This package provides utilities for understanding ETF pricing, order book mechanics,
and market microstructure related to the August 24, 2015 flash crash.

Modules:
    etf_pricing: NAV and iNAV calculations, arbitrage spread functions
    order_book: Order book simulation and market order execution
    order_book_dynamics: Advanced order book simulation with LULD circuit breakers
    market_maker_pnl: Market maker P&L simulation and risk analysis
    visualization: Plotting helpers for educational visualizations
"""

__version__ = "1.0.0"
__author__ = "ETF Flash Crash Educational Project"

# Core ETF pricing functions
from .etf_pricing import (
    calculate_nav,
    calculate_inav,
    arbitrage_spread,
    creation_profit,
    redemption_profit,
)

# Basic order book
from .order_book import OrderBook

# Advanced order book dynamics (Extensions Track)
from .order_book_dynamics import (
    OrderBookSnapshot,
    FlashCrashOrderBook,
    calculate_kyle_lambda,
    calculate_amihud_illiquidity,
    identify_liquidity_gaps,
)

# Market maker P&L and risk analysis (Extensions Track)
from .market_maker_pnl import (
    HedgeStatus,
    MarketMakerPosition,
    MarketMakerSimulator,
    simulate_market_maker_crisis,
)

# Arbitrage analysis (Extensions Track)
from .arbitrage_analysis import (
    ArbitrageType,
    BarrierType,
    ArbitrageOpportunity,
    ETFArbitrageAnalyzer,
    calculate_no_arbitrage_bounds,
    identify_arbitrage_barriers,
)

# Data loading and preprocessing (Extensions Track)
from .data_loader import (
    Aug24DataLoader,
    calculate_fair_value_timeline,
)

# Optional visualization imports (requires matplotlib)
_visualization_available = False
_advanced_visualization_available = False

try:
    from .visualization import (
        plot_price_vs_inav,
        plot_order_book,
        plot_luld_bands,
        plot_halt_timeline,
    )
    _visualization_available = True
except ImportError:
    # Matplotlib not installed - visualization functions unavailable
    pass

try:
    from .advanced_visualizations import (
        plot_liquidity_heatmap,
        plot_multi_etf_comparison,
        plot_stop_loss_waterfall,
        plot_market_maker_spread_evolution,
        plot_halt_timeline_gantt,
        plot_arbitrage_barrier_timeline,
    )
    _advanced_visualization_available = True
except ImportError:
    # Advanced visualization requires matplotlib/seaborn
    pass

# Core functionality (always available)
__all__ = [
    # ETF Pricing
    "calculate_nav",
    "calculate_inav",
    "arbitrage_spread",
    "creation_profit",
    "redemption_profit",
    # Basic Order Book
    "OrderBook",
    # Advanced Order Book Dynamics
    "OrderBookSnapshot",
    "FlashCrashOrderBook",
    "calculate_kyle_lambda",
    "calculate_amihud_illiquidity",
    "identify_liquidity_gaps",
    # Market Maker P&L
    "HedgeStatus",
    "MarketMakerPosition",
    "MarketMakerSimulator",
    "simulate_market_maker_crisis",
    # Arbitrage Analysis
    "ArbitrageType",
    "BarrierType",
    "ArbitrageOpportunity",
    "ETFArbitrageAnalyzer",
    "calculate_no_arbitrage_bounds",
    "identify_arbitrage_barriers",
    # Data Loading
    "Aug24DataLoader",
    "calculate_fair_value_timeline",
]

# Add visualization functions if available
if _visualization_available:
    __all__.extend([
        "plot_price_vs_inav",
        "plot_order_book",
        "plot_luld_bands",
        "plot_halt_timeline",
    ])

# Add advanced visualization functions if available
if _advanced_visualization_available:
    __all__.extend([
        "plot_liquidity_heatmap",
        "plot_multi_etf_comparison",
        "plot_stop_loss_waterfall",
        "plot_market_maker_spread_evolution",
        "plot_halt_timeline_gantt",
        "plot_arbitrage_barrier_timeline",
    ])
