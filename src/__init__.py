"""
ETF Flash Crash 2015 - Educational Utilities

This package provides utilities for understanding ETF pricing, order book mechanics,
and market microstructure related to the August 24, 2015 flash crash.

Modules:
    etf_pricing: NAV and iNAV calculations, arbitrage spread functions
    order_book: Order book simulation and market order execution
    visualization: Plotting helpers for educational visualizations
"""

__version__ = "1.0.0"
__author__ = "ETF Flash Crash Educational Project"

from .etf_pricing import (
    calculate_nav,
    calculate_inav,
    arbitrage_spread,
    creation_profit,
    redemption_profit,
)

from .order_book import OrderBook

from .visualization import (
    plot_price_vs_inav,
    plot_order_book,
    plot_luld_bands,
    plot_halt_timeline,
)

__all__ = [
    "calculate_nav",
    "calculate_inav",
    "arbitrage_spread",
    "creation_profit",
    "redemption_profit",
    "OrderBook",
    "plot_price_vs_inav",
    "plot_order_book",
    "plot_luld_bands",
    "plot_halt_timeline",
]
