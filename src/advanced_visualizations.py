"""
Advanced visualizations for market microstructure analysis.

This module provides publication-quality visualizations for analyzing
ETF flash crash market dynamics, including liquidity heatmaps, stop-loss
cascades, market maker behavior, and arbitrage barriers.

Functions:
    plot_liquidity_heatmap: Order book depth evolution over time
    plot_multi_etf_comparison: Compare multiple ETFs during crash
    plot_stop_loss_waterfall: Visualize stop-loss cascade
    plot_market_maker_spread_evolution: Market maker spread widening
    plot_halt_timeline_gantt: Gantt chart of trading halts
    plot_arbitrage_barrier_timeline: Arbitrage barriers over time
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Set publication-quality style
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    # Fallback for older matplotlib versions
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        pass  # Use default style

sns.set_context("paper", font_scale=1.2)


def plot_liquidity_heatmap(
    orderbook_snapshots: List,
    price_range: Tuple[float, float],
    time_range: Tuple[pd.Timestamp, pd.Timestamp],
    side: str = 'bid'
) -> plt.Figure:
    """
    Create heatmap showing order book depth evolution over time.

    Visualizes "liquidity evaporation" during flash crash by showing
    how available liquidity at each price level changes over time.

    Args:
        orderbook_snapshots: List of OrderBookSnapshot objects
        price_range: (min_price, max_price) to display
        time_range: (start_time, end_time)
        side: 'bid' or 'ask' - which side of book to visualize

    Returns:
        matplotlib Figure object

    Example:
        >>> from src.order_book_dynamics import FlashCrashOrderBook
        >>> book = FlashCrashOrderBook('RSP', 100.0)
        >>> # ... simulate some trading ...
        >>> snapshots = book.snapshot_history
        >>> fig = plot_liquidity_heatmap(
        ...     snapshots,
        ...     (90, 110),
        ...     (pd.Timestamp('2015-08-24 09:30'),
        ...      pd.Timestamp('2015-08-24 10:00')),
        ...     'bid'
        ... )
        >>> plt.show()
    """
    fig, ax = plt.subplots(figsize=(14, 8))

    # Create grid for heatmap
    price_bins = np.linspace(price_range[0], price_range[1], 50)
    time_bins = pd.date_range(time_range[0], time_range[1], freq='1min')

    # Initialize grid
    heatmap_data = np.zeros((len(price_bins)-1, len(time_bins)-1))

    # Fill grid with liquidity data
    for snapshot in orderbook_snapshots:
        if snapshot.timestamp < time_range[0] or snapshot.timestamp > time_range[1]:
            continue

        # Find time bin
        time_idx = np.searchsorted(time_bins, snapshot.timestamp) - 1
        if time_idx < 0 or time_idx >= len(time_bins) - 1:
            continue

        # Get order book for appropriate side
        book = snapshot.bids if side == 'bid' else snapshot.asks

        # Aggregate liquidity into price bins
        for price, size in book.items():
            if price < price_range[0] or price > price_range[1]:
                continue
            price_idx = np.searchsorted(price_bins, price) - 1
            if price_idx >= 0 and price_idx < len(price_bins) - 1:
                heatmap_data[price_idx, time_idx] += size

    # Plot heatmap
    im = ax.imshow(heatmap_data,
                   aspect='auto',
                   origin='lower',
                   cmap='YlOrRd',
                   interpolation='bilinear',
                   extent=[mdates.date2num(time_bins[0]),
                          mdates.date2num(time_bins[-1]),
                          price_bins[0],
                          price_bins[-1]])

    # Format axes
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    ax.set_xlabel('Time (EST)')
    ax.set_ylabel('Price ($)')
    ax.set_title(f'Order Book Depth Evolution - {side.capitalize()} Side\n'
                f'Dark Red = High Liquidity, Light Yellow = Low Liquidity',
                fontsize=14, fontweight='bold')

    # Add colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax)
    cbar.set_label('Cumulative Size (shares)', rotation=270, labelpad=20)

    plt.tight_layout()
    return fig


def plot_multi_etf_comparison(
    etf_data: Dict[str, pd.DataFrame],
    fair_values: Dict[str, float]
) -> plt.Figure:
    """
    Compare multiple ETFs during flash crash.

    Shows which ETFs were hit hardest by comparing market prices
    to fair values across multiple securities.

    Args:
        etf_data: Dictionary mapping symbol to DataFrame with:
                 - timestamp: datetime (index or column)
                 - price: market price
        fair_values: Dictionary mapping symbol to fair value (NAV/iNAV)

    Returns:
        matplotlib Figure with subplots for each ETF

    Example:
        >>> etf_data = {
        ...     'RSP': rsp_df,
        ...     'SPY': spy_df,
        ...     'IVV': ivv_df
        ... }
        >>> fair_values = {'RSP': 71.5, 'SPY': 196.0, 'IVV': 196.0}
        >>> fig = plot_multi_etf_comparison(etf_data, fair_values)
    """
    fig, axes = plt.subplots(len(etf_data), 1,
                            figsize=(14, 4*len(etf_data)),
                            sharex=True)

    if len(etf_data) == 1:
        axes = [axes]

    for ax, (symbol, df) in zip(axes, etf_data.items()):
        # Ensure timestamp is in index
        if 'timestamp' in df.columns:
            df = df.set_index('timestamp')

        fair_value = fair_values[symbol]

        # Calculate discount
        df_copy = df.copy()
        df_copy['discount_pct'] = ((df_copy['price'] / fair_value) - 1) * 100

        # Plot price
        ax2 = ax.twinx()

        ax.plot(df_copy.index, df_copy['price'],
               label='Market Price', color='blue', linewidth=2)
        ax.axhline(y=fair_value, color='green', linestyle='--',
                  linewidth=2, label='Fair Value (NAV)')

        # Shade discount regions
        ax.fill_between(df_copy.index, df_copy['price'], fair_value,
                       where=(df_copy['price'] < fair_value),
                       alpha=0.3, color='red', label='Discount')

        # Plot discount on right axis
        ax2.plot(df_copy.index, df_copy['discount_pct'],
                color='red', alpha=0.5, linestyle='--')
        ax2.set_ylabel('Discount (%)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Highlight worst moment
        worst_idx = df_copy['discount_pct'].idxmin()
        worst_price = df_copy.loc[worst_idx, 'price']
        worst_discount = df_copy.loc[worst_idx, 'discount_pct']

        ax.scatter(worst_idx, worst_price,
                  s=200, c='red', marker='X',
                  zorder=5, edgecolors='black', linewidth=2,
                  label=f'Worst: ${worst_price:.2f} ({worst_discount:.1f}%)')

        ax.set_ylabel('Price ($)')
        ax.set_title(f'{symbol} - Flash Crash Price Action',
                    fontsize=13, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    axes[-1].set_xlabel('Time (EST)')
    plt.tight_layout()
    return fig


def plot_stop_loss_waterfall(
    stop_orders: pd.DataFrame,
    actual_executions: pd.DataFrame
) -> plt.Figure:
    """
    Waterfall chart showing stop-loss cascade.

    Visualizes how stop-loss orders triggered sequentially and
    how far below their trigger prices they actually filled.

    Args:
        stop_orders: DataFrame with columns:
                    - stop_price: trigger price
                    - size: order size
        actual_executions: DataFrame with columns:
                          - stop_price: trigger price
                          - execution_price: actual fill price
                          - size: shares executed

    Returns:
        matplotlib Figure with two panels

    Example:
        >>> stop_orders = pd.DataFrame({
        ...     'stop_price': [100, 99, 98, 97],
        ...     'size': [1000, 1500, 2000, 1200]
        ... })
        >>> executions = pd.DataFrame({
        ...     'stop_price': [100, 99, 98],
        ...     'execution_price': [98, 95, 90],
        ...     'size': [1000, 1500, 2000]
        ... })
        >>> fig = plot_stop_loss_waterfall(stop_orders, executions)
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Top panel: Stop orders waiting at each level
    ax1.bar(stop_orders['stop_price'], stop_orders['size'],
           width=0.5, color='orange', alpha=0.7,
           edgecolor='black', label='Stop Orders Waiting')

    ax1.set_xlabel('Stop Trigger Price ($)')
    ax1.set_ylabel('Total Size (shares)')
    ax1.set_title('Distribution of Stop-Loss Orders by Price Level',
                 fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')

    # Bottom panel: Execution vs trigger price (slippage)
    if not actual_executions.empty:
        x = np.arange(len(actual_executions))
        width = 0.35

        ax2.bar(x - width/2, actual_executions['stop_price'],
               width, label='Stop Trigger Price',
               color='orange', alpha=0.7)
        ax2.bar(x + width/2, actual_executions['execution_price'],
               width, label='Actual Execution Price',
               color='red', alpha=0.7)

        # Draw lines connecting trigger to execution
        for i in range(len(actual_executions)):
            ax2.plot([i - width/2, i + width/2],
                    [actual_executions.iloc[i]['stop_price'],
                     actual_executions.iloc[i]['execution_price']],
                    'k--', alpha=0.5, linewidth=1)

        ax2.set_xlabel('Stop Order Sequence')
        ax2.set_ylabel('Price ($)')
        ax2.set_title('Stop-Loss Execution Slippage\n'
                     'Orange = Intended Trigger | Red = Actual Fill',
                     fontsize=13, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels([f'Stop {i+1}' for i in range(len(actual_executions))])
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        # Annotate slippage
        for i, row in actual_executions.iterrows():
            slippage = ((row['execution_price'] / row['stop_price']) - 1) * 100
            ax2.text(i, row['execution_price'] - 1,
                    f'{slippage:.1f}%',
                    ha='center', va='top', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

    plt.tight_layout()
    return fig


def plot_market_maker_spread_evolution(mm_data: pd.DataFrame) -> plt.Figure:
    """
    Show how market maker spreads widened during crisis.

    Visualizes market maker withdrawal through spread widening
    and size reduction.

    Args:
        mm_data: DataFrame with columns:
                - timestamp: datetime (index or column)
                - spread_bps: bid-ask spread in basis points
                - bid_size: size at bid (optional)
                - ask_size: size at ask (optional)

    Returns:
        matplotlib Figure with 2-3 panels

    Example:
        >>> mm_data = pd.DataFrame({
        ...     'timestamp': timestamps,
        ...     'spread_bps': [10, 25, 100, 500, 50, 15],
        ...     'bid_size': [10000, 8000, 5000, 1000, 5000, 9000],
        ...     'ask_size': [10000, 8000, 5000, 1000, 5000, 9000]
        ... })
        >>> fig = plot_market_maker_spread_evolution(mm_data)
    """
    # Ensure timestamp is in index
    if 'timestamp' in mm_data.columns:
        mm_data = mm_data.set_index('timestamp')

    has_size_data = 'bid_size' in mm_data.columns and 'ask_size' in mm_data.columns

    if has_size_data:
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(14, 5))
        ax2 = ax3 = None

    # Panel 1: Spread width (log scale)
    ax1.plot(mm_data.index, mm_data['spread_bps'],
            color='red', linewidth=2)
    ax1.axhline(y=10, color='green', linestyle='--',
               label='Normal Spread (10 bps)')
    ax1.set_yscale('log')
    ax1.set_ylabel('Spread (bps, log scale)')
    ax1.set_title('Market Maker Spread Widening During Flash Crash',
                 fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3, which='both')

    if has_size_data:
        # Panel 2: Quoted size
        ax2.plot(mm_data.index, mm_data['bid_size'],
                label='Bid Size', color='green', linewidth=2)
        ax2.plot(mm_data.index, mm_data['ask_size'],
                label='Ask Size', color='red', linewidth=2)
        ax2.set_ylabel('Quoted Size (shares)')
        ax2.set_title('Market Maker Quote Size',
                     fontsize=13, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Panel 3: Effective cost to trade (liquidity index)
        mm_data_copy = mm_data.copy()
        mm_data_copy['liquidity_index'] = (
            (mm_data_copy['bid_size'] + mm_data_copy['ask_size']) /
            mm_data_copy['spread_bps']
        )
        ax3.plot(mm_data_copy.index, mm_data_copy['liquidity_index'],
                color='blue', linewidth=2)
        ax3.set_ylabel('Liquidity Index\n(size / spread)')
        ax3.set_xlabel('Time (EST)')
        ax3.set_title('Overall Liquidity Measure (Higher = More Liquid)',
                     fontsize=13, fontweight='bold')
        ax3.grid(True, alpha=0.3)

        # Format x-axis
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
    else:
        ax1.set_xlabel('Time (EST)')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)

    plt.tight_layout()
    return fig


def plot_halt_timeline_gantt(
    halt_data: pd.DataFrame,
    etf_symbols: Optional[List[str]] = None
) -> plt.Figure:
    """
    Gantt chart showing when each ETF was halted vs trading.

    Visualizes the temporal pattern of trading halts across
    multiple securities.

    Args:
        halt_data: DataFrame with columns:
                  - symbol: ticker symbol
                  - halt_start: halt start time
                  - halt_end: halt end time
                  - price_at_halt: price when halted (optional)
                  - discount_pct: discount percentage (optional)
        etf_symbols: Optional list of symbols to include.
                    If None, uses all symbols in halt_data.

    Returns:
        matplotlib Figure

    Example:
        >>> halt_data = pd.DataFrame({
        ...     'symbol': ['RSP', 'RSP', 'SPY'],
        ...     'halt_start': ['2015-08-24 09:35', '2015-08-24 09:42', ...],
        ...     'halt_end': ['2015-08-24 09:40', '2015-08-24 09:47', ...],
        ...     'discount_pct': [-15, -25, -8]
        ... })
        >>> fig = plot_halt_timeline_gantt(halt_data)
    """
    # Parse timestamps if needed
    if not pd.api.types.is_datetime64_any_dtype(halt_data['halt_start']):
        halt_data = halt_data.copy()
        halt_data['halt_start'] = pd.to_datetime(halt_data['halt_start'])
        halt_data['halt_end'] = pd.to_datetime(halt_data['halt_end'])

    # Determine symbols to include
    if etf_symbols is None:
        etf_symbols = sorted(halt_data['symbol'].unique())

    fig, ax = plt.subplots(figsize=(16, max(8, len(etf_symbols) * 0.4)))

    # Create mapping of symbols to y-positions
    symbol_to_y = {symbol: i for i, symbol in enumerate(etf_symbols)}

    # Plot each halt period
    for _, halt in halt_data.iterrows():
        symbol = halt['symbol']
        if symbol not in symbol_to_y:
            continue

        y_pos = symbol_to_y[symbol]
        start = mdates.date2num(halt['halt_start'])
        end = mdates.date2num(halt['halt_end'])
        duration = end - start

        # Color by severity (if discount_pct available)
        if 'discount_pct' in halt and not pd.isna(halt['discount_pct']):
            discount = halt['discount_pct']
            if discount < -20:
                color = 'darkred'
            elif discount < -10:
                color = 'red'
            else:
                color = 'orange'
        else:
            color = 'orange'

        # Draw rectangle
        rect = Rectangle((start, y_pos - 0.4), duration, 0.8,
                         facecolor=color, edgecolor='black', alpha=0.7)
        ax.add_patch(rect)

        # Annotate with price if available
        if 'price_at_halt' in halt and not pd.isna(halt['price_at_halt']):
            ax.text(start + duration/2, y_pos,
                   f"${halt['price_at_halt']:.1f}",
                   ha='center', va='center', fontsize=8,
                   color='white', fontweight='bold')

    # Format axes
    ax.set_yticks(range(len(etf_symbols)))
    ax.set_yticklabels(etf_symbols)
    ax.set_xlabel('Time (EST)')
    ax.set_title('ETF Trading Halts Timeline - August 24, 2015\n'
                'Dark Red = >20% discount | Red = 10-20% | Orange = <10%',
                fontsize=14, fontweight='bold')

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    ax.grid(True, alpha=0.3, axis='x')
    ax.set_xlim(mdates.date2num(halt_data['halt_start'].min()),
               mdates.date2num(halt_data['halt_end'].max()))

    plt.tight_layout()
    return fig


def plot_arbitrage_barrier_timeline(arbitrage_analysis: pd.DataFrame) -> plt.Figure:
    """
    Show when arbitrage was blocked and why.

    Visualizes the temporal evolution of arbitrage barriers
    alongside the ETF discount.

    Args:
        arbitrage_analysis: DataFrame with columns:
                           - timestamp: datetime (index or column)
                           - discount_pct: ETF discount percentage
                           - barriers: comma-separated barrier types

    Returns:
        matplotlib Figure with two panels

    Example:
        >>> arb_df = pd.DataFrame({
        ...     'timestamp': timestamps,
        ...     'discount_pct': [-5, -15, -25, -20, -10, -3],
        ...     'barriers': ['none', 'halted_components', 'stale_inav', ...]
        ... })
        >>> fig = plot_arbitrage_barrier_timeline(arb_df)
    """
    # Ensure timestamp is in index
    if 'timestamp' in arbitrage_analysis.columns:
        arbitrage_analysis = arbitrage_analysis.set_index('timestamp')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Top panel: Discount over time
    ax1.plot(arbitrage_analysis.index,
            arbitrage_analysis['discount_pct'],
            color='red', linewidth=2, label='ETF Discount')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax1.fill_between(arbitrage_analysis.index,
                    0, arbitrage_analysis['discount_pct'],
                    where=(arbitrage_analysis['discount_pct'] < 0),
                    alpha=0.3, color='red')
    ax1.set_ylabel('Discount (%)')
    ax1.set_title('ETF Discount and Arbitrage Barriers',
                 fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Bottom panel: Barrier timeline
    # Create binary indicators for each barrier type
    barrier_types = ['halted_components', 'stale_inav', 'liquidity_cost', 'settlement_risk']
    colors = {
        'halted_components': 'darkred',
        'stale_inav': 'orange',
        'liquidity_cost': 'yellow',
        'settlement_risk': 'red'
    }
    labels = {
        'halted_components': 'Halted Components',
        'stale_inav': 'Stale iNAV',
        'liquidity_cost': 'Liquidity Cost',
        'settlement_risk': 'Settlement Risk'
    }

    y_pos = 0
    for barrier in barrier_types:
        if barrier in ' '.join(arbitrage_analysis['barriers'].values):
            # Check if this barrier is present
            has_barrier = arbitrage_analysis['barriers'].str.contains(barrier, na=False)

            # Plot as filled region
            ax2.fill_between(arbitrage_analysis.index,
                            y_pos, y_pos + 0.8,
                            where=has_barrier,
                            alpha=0.7,
                            color=colors[barrier],
                            label=labels[barrier],
                            step='mid')
            y_pos += 1

    # If no barriers found, show "no barriers" zone
    no_barriers = ~arbitrage_analysis['barriers'].str.contains(
        '|'.join(barrier_types), na=False
    )
    if no_barriers.any():
        ax2.fill_between(arbitrage_analysis.index,
                        y_pos, y_pos + 0.8,
                        where=no_barriers,
                        alpha=0.7,
                        color='green',
                        label='No Barriers',
                        step='mid')

    ax2.set_ylim(0, y_pos + 1)
    ax2.set_yticks([])
    ax2.set_xlabel('Time (EST)')
    ax2.set_title('Arbitrage Barriers Over Time',
                 fontsize=13, fontweight='bold')
    ax2.legend(loc='upper right')

    # Format x-axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig
