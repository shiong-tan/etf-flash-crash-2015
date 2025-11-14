"""
Visualization Utilities

Plotting functions for educational visualizations of ETF pricing, order books,
LULD bands, and the August 24, 2015 flash crash timeline.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import numpy as np


def plot_price_vs_inav(
    timestamps: List[datetime],
    etf_prices: List[float],
    inav_values: List[float],
    title: str = "ETF Price vs iNAV",
    etf_label: str = "ETF Price",
    inav_label: str = "iNAV",
    highlight_dislocation: bool = True
) -> plt.Figure:
    """
    Plot ETF price vs iNAV to show price dislocations.

    Demonstrates the August 24, 2015 phenomenon where ETFs traded far below iNAV.
    Example: RSP at $50 while iNAV showed $71.

    Args:
        timestamps: List of datetime objects
        etf_prices: ETF market prices at each timestamp
        inav_values: iNAV values at each timestamp
        title: Plot title
        etf_label: Label for ETF price line
        inav_label: Label for iNAV line
        highlight_dislocation: Whether to shade areas of large dislocation

    Returns:
        matplotlib Figure object

    Example:
        >>> from datetime import datetime, timedelta
        >>> times = [datetime(2015, 8, 24, 9, 30) + timedelta(minutes=i) for i in range(60)]
        >>> prices = [76 - i*0.5 for i in range(60)]  # RSP falling
        >>> inavs = [71] * 60  # iNAV stable (stale)
        >>> fig = plot_price_vs_inav(times, prices, inavs, "RSP Dislocation")
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot lines
    ax.plot(timestamps, etf_prices, label=etf_label, linewidth=2, color='#2E86AB')
    ax.plot(timestamps, inav_values, label=inav_label, linewidth=2,
            color='#A23B72', linestyle='--')

    # Highlight dislocation areas
    if highlight_dislocation:
        discount = np.array(etf_prices) < np.array(inav_values)
        ax.fill_between(timestamps, etf_prices, inav_values,
                        where=discount, alpha=0.3, color='red',
                        label='Trading at Discount')

    # Formatting
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Format x-axis for time
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    plt.tight_layout()
    return fig


def plot_order_book(
    bids: List[Tuple[float, int]],
    asks: List[Tuple[float, int]],
    title: str = "Order Book",
    highlight_air_pocket: bool = True
) -> plt.Figure:
    """
    Visualize order book depth to show "air pockets".

    Air pockets are large price gaps with little liquidity, causing market
    orders to execute far from expected prices on August 24, 2015.

    Args:
        bids: List of (price, size) tuples for buy orders
        asks: List of (price, size) tuples for sell orders
        title: Plot title
        highlight_air_pocket: Whether to highlight large gaps

    Returns:
        matplotlib Figure object

    Example:
        >>> bids = [(100, 500), (99, 300), (90, 400)]  # Air pocket between 99 and 90
        >>> asks = [(101, 500), (102, 300)]
        >>> fig = plot_order_book(bids, asks)
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Sort for display
    bids = sorted(bids, reverse=True)  # Highest first
    asks = sorted(asks)  # Lowest first

    # Extract prices and cumulative sizes
    bid_prices = [p for p, _ in bids]
    bid_sizes = [s for _, s in bids]
    bid_cumsum = np.cumsum(bid_sizes)

    ask_prices = [p for p, _ in asks]
    ask_sizes = [s for _, s in asks]
    ask_cumsum = np.cumsum(ask_sizes)

    # Plot step functions
    ax.step(bid_cumsum, bid_prices, where='post', label='Bids',
            color='green', linewidth=2)
    ax.step(ask_cumsum, ask_prices, where='post', label='Asks',
            color='red', linewidth=2)

    # Highlight air pocket if present
    if highlight_air_pocket and bids and asks:
        best_bid = max(bid_prices)
        best_ask = min(ask_prices)
        spread = best_ask - best_bid

        if spread > best_bid * 0.05:  # Spread > 5%
            ax.axhspan(best_bid, best_ask, alpha=0.3, color='yellow',
                      label=f'Air Pocket (${spread:.2f})')

    # Formatting
    ax.set_xlabel('Cumulative Size (shares)', fontsize=12)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_luld_bands(
    timestamps: List[datetime],
    prices: List[float],
    reference_price: float,
    band_width_pct: float = 5.0,
    halts: Optional[List[Tuple[datetime, datetime]]] = None,
    title: str = "LULD Price Bands"
) -> plt.Figure:
    """
    Visualize LULD price bands and trading halts.

    Shows how prices hit bands and trigger halts during August 24, 2015.
    RSP experienced 10 halts in one hour.

    Args:
        timestamps: List of datetime objects
        prices: Price at each timestamp
        reference_price: LULD reference price
        band_width_pct: Band width in percent (5% regular, 10% open/close)
        halts: List of (start_time, end_time) tuples for trading halts
        title: Plot title

    Returns:
        matplotlib Figure object

    Example:
        >>> times = [datetime(2015, 8, 24, 9, 30) + timedelta(minutes=i) for i in range(60)]
        >>> prices = [100 - i*2 for i in range(60)]  # Falling through bands
        >>> fig = plot_luld_bands(times, prices, 100, 5.0)
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Calculate band levels
    upper_band = reference_price * (1 + band_width_pct / 100)
    lower_band = reference_price * (1 - band_width_pct / 100)

    # Plot price
    ax.plot(timestamps, prices, label='Price', linewidth=2, color='#2E86AB')

    # Plot bands
    ax.axhline(y=reference_price, color='black', linestyle='--',
              linewidth=1, label='Reference Price', alpha=0.7)
    ax.axhline(y=upper_band, color='red', linestyle='--',
              linewidth=1.5, label=f'Upper Band (+{band_width_pct}%)', alpha=0.7)
    ax.axhline(y=lower_band, color='red', linestyle='--',
              linewidth=1.5, label=f'Lower Band (-{band_width_pct}%)', alpha=0.7)

    # Shade band regions
    ax.fill_between(timestamps, lower_band, upper_band,
                    alpha=0.1, color='green', label='Trading Range')

    # Mark halts
    if halts:
        for i, (start, end) in enumerate(halts):
            ax.axvspan(start, end, alpha=0.3, color='gray',
                      label='Trading Halt' if i == 0 else '')

    # Formatting
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    plt.tight_layout()
    return fig


def plot_halt_timeline(
    halts: List[Tuple[datetime, datetime, str]],
    start_time: datetime,
    end_time: datetime,
    title: str = "Trading Halts Timeline"
) -> plt.Figure:
    """
    Visualize trading halt timeline for multiple securities.

    Shows the cascade of halts during August 24, 2015.
    Example: 1,278 halts across 471 securities in first hour.

    Args:
        halts: List of (start_time, end_time, ticker) tuples
        start_time: Timeline start
        end_time: Timeline end
        title: Plot title

    Returns:
        matplotlib Figure object

    Example:
        >>> from datetime import datetime, timedelta
        >>> base = datetime(2015, 8, 24, 9, 30)
        >>> halts = [(base + timedelta(minutes=i), base + timedelta(minutes=i+5), "RSP")
        ...          for i in range(0, 60, 10)]
        >>> fig = plot_halt_timeline(halts, base, base + timedelta(hours=1))
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # Group halts by ticker
    tickers = list(set(ticker for _, _, ticker in halts))
    ticker_to_y = {ticker: i for i, ticker in enumerate(tickers)}

    # Plot each halt as horizontal bar
    for start, end, ticker in halts:
        y = ticker_to_y[ticker]
        duration = (end - start).total_seconds() / 60  # Convert to minutes
        ax.barh(y, duration, left=mdates.date2num(start),
               height=0.8, color='red', alpha=0.6, edgecolor='darkred')

    # Formatting
    ax.set_yticks(range(len(tickers)))
    ax.set_yticklabels(tickers)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Security', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlim(mdates.date2num(start_time), mdates.date2num(end_time))

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    ax.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    return fig


def plot_stop_loss_cascade(
    stop_triggers: List[float],
    execution_prices: List[float],
    sizes: List[int],
    initial_price: float,
    title: str = "Stop-Loss Cascade"
) -> plt.Figure:
    """
    Visualize stop-loss cascade showing executions below triggers.

    Demonstrates August 24 retail casualties: stops at $108.69 executing at $87.32.

    Args:
        stop_triggers: Stop-loss trigger prices
        execution_prices: Actual execution prices
        sizes: Order sizes
        initial_price: Starting market price
        title: Plot title

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create index for x-axis
    x = range(len(stop_triggers))

    # Plot trigger vs execution
    ax.plot(x, stop_triggers, 'o-', label='Stop Trigger Price',
           markersize=8, color='orange', linewidth=2)
    ax.plot(x, execution_prices, 'o-', label='Actual Execution Price',
           markersize=8, color='red', linewidth=2)
    ax.axhline(y=initial_price, color='green', linestyle='--',
              label='Initial Price', alpha=0.7)

    # Shade the "slippage" area
    ax.fill_between(x, stop_triggers, execution_prices,
                    alpha=0.3, color='red', label='Slippage')

    # Annotate with sizes
    for i, size in enumerate(sizes):
        ax.annotate(f'{size:,} shares',
                   xy=(i, execution_prices[i]),
                   xytext=(0, -15),
                   textcoords='offset points',
                   ha='center', fontsize=8)

    # Formatting
    ax.set_xlabel('Stop-Loss Order Sequence', fontsize=12)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
