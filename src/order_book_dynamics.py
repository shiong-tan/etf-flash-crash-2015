"""
Advanced order book analysis for flash crash conditions.
Implements realistic market microstructure models.

This module provides tools for analyzing order book behavior during extreme
market conditions, particularly the August 24, 2015 ETF flash crash.

Classes:
    OrderBookSnapshot: Represents order book state at a point in time
    FlashCrashOrderBook: Simulates order book behavior during flash crash

Functions:
    calculate_kyle_lambda: Calculate price impact coefficient
    calculate_amihud_illiquidity: Calculate Amihud illiquidity measure
    identify_liquidity_gaps: Identify "air pockets" in order book
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class OrderBookSnapshot:
    """
    Represents order book state at a point in time.

    Attributes:
        timestamp: Time of snapshot
        bids: Dictionary mapping price to size
        asks: Dictionary mapping price to size
        last_trade: Price of last trade (None if no trades yet)
        fair_value: Fair value (NAV/iNAV) at this time
        halt_status: Whether trading is halted
    """
    timestamp: pd.Timestamp
    bids: Dict[float, int]  # price -> size
    asks: Dict[float, int]
    last_trade: Optional[float]
    fair_value: float
    halt_status: bool

    def spread_bps(self) -> float:
        """
        Calculate bid-ask spread in basis points.

        Returns:
            Spread in basis points, or np.inf if no quotes

        Examples:
            >>> snapshot = OrderBookSnapshot(...)
            >>> snapshot.spread_bps()
            5.2  # 5.2 basis points
        """
        if not self.bids or not self.asks:
            return np.inf
        best_bid = max(self.bids.keys())
        best_ask = min(self.asks.keys())
        mid = (best_bid + best_ask) / 2

        # Handle zero or negative mid price (extreme flash crash scenarios)
        if mid <= 0:
            return np.inf

        return ((best_ask - best_bid) / mid) * 10000

    def depth_at_distance(self, distance_pct: float) -> Tuple[int, int]:
        """
        Calculate cumulative depth within distance_pct from mid.

        Args:
            distance_pct: Distance from mid as decimal (e.g., 0.01 = 1%)

        Returns:
            Tuple of (bid_depth, ask_depth) in shares

        Examples:
            >>> snapshot.depth_at_distance(0.01)  # Within 1% of mid
            (50000, 45000)  # 50k shares bid, 45k shares ask
        """
        if not self.bids or not self.asks:
            return (0, 0)

        best_bid = max(self.bids.keys())
        best_ask = min(self.asks.keys())
        mid = (best_bid + best_ask) / 2

        threshold = mid * distance_pct
        bid_depth = sum(size for price, size in self.bids.items()
                       if price >= mid - threshold)
        ask_depth = sum(size for price, size in self.asks.items()
                       if price <= mid + threshold)

        return (bid_depth, ask_depth)

    def price_impact(self, quantity: int, side: str) -> float:
        """
        Calculate price impact for market order of given size.

        Args:
            quantity: Number of shares
            side: 'buy' or 'sell'

        Returns:
            Average execution price, or np.nan if insufficient liquidity

        Examples:
            >>> snapshot.price_impact(10000, 'buy')
            76.52  # Would execute at average price of $76.52
        """
        book = self.bids if side == 'sell' else self.asks
        reverse = side == 'sell'

        sorted_prices = sorted(book.keys(), reverse=reverse)
        remaining = quantity
        total_cost = 0.0

        for price in sorted_prices:
            available = book[price]
            traded = min(remaining, available)
            total_cost += traded * price
            remaining -= traded
            if remaining == 0:
                break

        if remaining > 0:
            # Not enough liquidity - return NaN
            return np.nan

        return total_cost / quantity


class FlashCrashOrderBook:
    """
    Simulates order book behavior during flash crash conditions.
    Models realistic liquidity provision/withdrawal dynamics.

    This class simulates how order books behave during extreme market stress,
    particularly focusing on market maker behavior and the cascade effects
    of stop-loss orders.

    Attributes:
        symbol: ETF ticker symbol
        fair_value: Current fair value (NAV/iNAV)
        normal_spread_bps: Normal market spread in basis points
        luld_band_pct: LULD circuit breaker band percentage (5.0 or 10.0 typically)
        bids: Current bid orders {price: size}
        asks: Current ask orders {price: size}
        trade_history: List of executed trades
        snapshot_history: List of order book snapshots
        halt_status: Whether trading is currently halted
        volatility: Current volatility estimate
        market_maker_active: Whether market makers are actively quoting
    """

    def __init__(self, symbol: str, fair_value: float, normal_spread_bps: float = 2.0,
                 luld_band_pct: float = 5.0):
        """
        Initialize order book with normal market conditions.

        Args:
            symbol: ETF ticker
            fair_value: Initial fair value
            normal_spread_bps: Normal spread in basis points (default 2.0)
            luld_band_pct: LULD circuit breaker band percentage (default 5.0)
                - 5% for regular trading hours
                - 10% for market opening/closing
                - Custom values for simulation scenarios

        Examples:
            >>> # Regular trading with 5% bands
            >>> book = FlashCrashOrderBook('SPY', 200.0)
            >>>
            >>> # Market opening with 10% bands
            >>> book = FlashCrashOrderBook('SPY', 200.0, luld_band_pct=10.0)
        """
        self.symbol = symbol
        self.fair_value = fair_value
        self.normal_spread_bps = normal_spread_bps
        self.original_spread_bps = normal_spread_bps  # Store original to prevent accumulation
        self.luld_band_pct = luld_band_pct

        self.bids = {}  # price -> size
        self.asks = {}
        self.trade_history = []
        self.snapshot_history = []

        self.halt_status = False
        self.volatility = 0.20  # 20% annualized
        self.market_maker_active = True

        # Initialize normal order book
        self._initialize_normal_book()

    def _initialize_normal_book(self):
        """
        Create realistic initial order book with power-law depth decay.

        Uses power-law distribution to model realistic order book depth,
        with more liquidity near the mid and less far away.
        """
        spread = self.fair_value * (self.normal_spread_bps / 10000)

        # Market maker quotes at best bid/ask
        self.bids[self.fair_value - spread/2] = 10000
        self.asks[self.fair_value + spread/2] = 10000

        # Power-law distribution of limit orders
        # More orders near the mid, fewer far away
        for i in range(1, 50):
            distance = spread * i
            # Size decays as ~1/distance^2
            size = int(10000 / (i ** 1.5))

            self.bids[self.fair_value - spread/2 - distance] = size
            self.asks[self.fair_value + spread/2 + distance] = size

    def simulate_market_maker_withdrawal(self, stress_level: float):
        """
        Model market maker response to stress.

        Market makers respond to stress by widening spreads, reducing size,
        and ultimately withdrawing quotes entirely under extreme stress.

        Args:
            stress_level: 0.0 (calm) to 1.0 (panic)

        Effects:
            - stress < 0.3: Wider spreads
            - 0.3 <= stress < 0.7: Dramatically wider spreads, reduced size
            - stress >= 0.7: Complete withdrawal

        Examples:
            >>> book = FlashCrashOrderBook('SPY', 200.0)
            >>> book.simulate_market_maker_withdrawal(0.8)  # Panic
            >>> book.market_maker_active
            False
        """
        if stress_level < 0.3:
            # Moderate stress - widen spreads
            spread_multiplier = 1 + stress_level * 10  # up to 4x wider
            self.normal_spread_bps = self.original_spread_bps * spread_multiplier

        elif stress_level < 0.7:
            # High stress - widen spreads dramatically, reduce size
            spread_multiplier = 10 + stress_level * 50  # 10x to 45x wider
            size_reduction = 0.9  # reduce to 10% of normal

            # Remove tight quotes, widen significantly
            best_bid = max(self.bids.keys()) if self.bids else self.fair_value * 0.95
            best_ask = min(self.asks.keys()) if self.asks else self.fair_value * 1.05

            # Clear close-in quotes
            self.bids = {p: int(s * size_reduction)
                        for p, s in self.bids.items()
                        if p < self.fair_value * 0.98}
            self.asks = {p: int(s * size_reduction)
                        for p, s in self.asks.items()
                        if p > self.fair_value * 1.02}

        else:
            # Panic - complete withdrawal
            self.market_maker_active = False
            # Only stale limit orders remain
            self.bids = {p: s for p, s in self.bids.items()
                        if p < self.fair_value * 0.90}
            self.asks = {p: s for p, s in self.asks.items()
                        if p > self.fair_value * 1.10}

    def execute_market_order(self, size: int, side: str) -> List[Dict]:
        """
        Execute market order and return fill details.

        Market orders walk the book, executing against available liquidity
        at each price level until filled or liquidity is exhausted.

        Args:
            size: Number of shares
            side: 'buy' or 'sell'

        Returns:
            List of execution dictionaries with keys:
                - price: Execution price
                - size: Size filled at this price
                - timestamp: Execution timestamp
                - side: Order side
                - status: 'UNFILLED' if partial fill

        Examples:
            >>> book.execute_market_order(5000, 'buy')
            [{'price': 200.01, 'size': 3000, 'timestamp': ..., 'side': 'buy'},
             {'price': 200.02, 'size': 2000, 'timestamp': ..., 'side': 'buy'}]
        """
        book = self.bids if side == 'sell' else self.asks
        reverse = side == 'sell'

        executions = []
        remaining = size
        timestamp = pd.Timestamp.now()

        sorted_prices = sorted(book.keys(), reverse=reverse)

        for price in sorted_prices:
            if remaining == 0:
                break

            available = book[price]
            traded = min(remaining, available)

            executions.append({
                'price': price,
                'size': traded,
                'timestamp': timestamp,
                'side': side
            })

            # Update book
            book[price] -= traded
            if book[price] == 0:
                del book[price]

            remaining -= traded

            # Check for LULD breach
            if self._check_luld_breach(price):
                self.halt_status = True
                self.trade_history.extend(executions)
                return executions

        # If we couldn't fill entire order
        if remaining > 0:
            status = 'PARTIALLY_FILLED' if remaining < size else 'UNFILLED'
            executions.append({
                'price': np.nan,
                'size': remaining,
                'timestamp': timestamp,
                'side': side,
                'status': status,
                'filled_size': size - remaining
            })

        self.trade_history.extend(executions)
        return executions

    def _check_luld_breach(self, price: float) -> bool:
        """
        Check if price breaches LULD bands.

        The Limit Up-Limit Down (LULD) mechanism halts trading when prices move
        beyond specified percentage bands. This uses the configured band percentage
        which can vary by time of day and market conditions:

        - Regular trading: typically 5%
        - Market open/close: typically 10%
        - Custom scenarios: user-configurable

        Args:
            price: Execution price to check

        Returns:
            True if price breaches configured LULD band

        Examples:
            >>> book = FlashCrashOrderBook('SPY', 200.0, luld_band_pct=5.0)
            >>> book._check_luld_breach(189.0)  # 5.5% below fair value
            True
            >>> book._check_luld_breach(195.0)  # 2.5% below fair value
            False
        """
        band_multiplier = self.luld_band_pct / 100
        lower_band = self.fair_value * (1 - band_multiplier)
        upper_band = self.fair_value * (1 + band_multiplier)
        return price < lower_band or price > upper_band

    def simulate_stop_loss_cascade(self,
                                   stop_orders: Dict[float, int],
                                   trigger_scenario: str = 'sequential') -> pd.DataFrame:
        """
        Simulate cascade of stop-loss orders triggering.

        Demonstrates how stop-loss orders can cascade, with each execution
        driving prices lower and triggering additional stops.

        Args:
            stop_orders: Dictionary {stop_price: total_size}
            trigger_scenario:
                'sequential' - stops trigger one level at a time
                'avalanche' - all stops hit at once

        Returns:
            DataFrame with execution details including slippage

        Examples:
            >>> stops = {75.0: 10000, 74.0: 15000, 73.0: 20000}
            >>> results = book.simulate_stop_loss_cascade(stops, 'sequential')
            >>> results['slippage_pct'].mean()
            -8.5  # Average 8.5% slippage
        """
        results = []

        # Sort stop prices from high to low
        sorted_stops = sorted(stop_orders.items(), reverse=True)

        if trigger_scenario == 'avalanche':
            # All stops trigger simultaneously
            total_sell_pressure = sum(stop_orders.values())
            executions = self.execute_market_order(total_sell_pressure, 'sell')

            for exec_detail in executions:
                results.append({
                    'trigger_price': None,
                    'execution_price': exec_detail['price'],
                    'size': exec_detail['size'],
                    'slippage_pct': ((exec_detail['price'] / self.fair_value) - 1) * 100
                                   if not np.isnan(exec_detail['price']) else np.nan,
                    'timestamp': exec_detail['timestamp']
                })

        else:  # sequential
            for stop_price, size in sorted_stops:
                # Check if current market price has hit stop
                # Stop triggers if: no bids (air pocket) OR best bid <= stop price
                best_bid = max(self.bids.keys()) if self.bids else None
                stop_triggered = (best_bid is None) or (best_bid <= stop_price)

                if stop_triggered:
                    # Stop triggered - becomes market order
                    try:
                        executions = self.execute_market_order(size, 'sell')

                        if executions:
                            avg_exec_price = np.mean([e['price'] for e in executions
                                                     if not np.isnan(e['price'])])

                            results.append({
                                'trigger_price': stop_price,
                                'execution_price': avg_exec_price,
                                'size': size,
                                'slippage_pct': ((avg_exec_price / stop_price) - 1) * 100
                                               if not np.isnan(avg_exec_price) else np.nan,
                                'timestamp': executions[0]['timestamp'] if (executions and len(executions) > 0) else pd.Timestamp.now()
                            })
                    except Exception:
                        # Air pocket - no liquidity to fill stop order
                        # Record the triggered stop even though it couldn't execute
                        results.append({
                            'trigger_price': stop_price,
                            'execution_price': np.nan,
                            'size': size,
                            'slippage_pct': np.nan,
                            'timestamp': pd.Timestamp.now()
                        })
                        break  # No point continuing if we hit an air pocket

                    if self.halt_status:
                        break

        return pd.DataFrame(results)

    def take_snapshot(self) -> OrderBookSnapshot:
        """
        Capture current order book state.

        Returns:
            OrderBookSnapshot with current book state
        """
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids=self.bids.copy(),
            asks=self.asks.copy(),
            last_trade=self.trade_history[-1]['price'] if self.trade_history else None,
            fair_value=self.fair_value,
            halt_status=self.halt_status
        )
        self.snapshot_history.append(snapshot)
        return snapshot


# Utility functions for analysis

def calculate_kyle_lambda(trades_df: pd.DataFrame,
                          orderbook_snapshots: List[OrderBookSnapshot]) -> float:
    """
    Calculate Kyle's lambda (price impact coefficient).

    Kyle's lambda measures how much prices move per unit of order flow.
    Higher lambda indicates lower liquidity and greater price impact.

    Lambda = dP / dQ (change in price per unit of order flow)

    Args:
        trades_df: DataFrame with 'price', 'size', 'side' columns
        orderbook_snapshots: List of order book snapshots (reserved for future use)

    Returns:
        Kyle's lambda coefficient (higher = less liquid)

    References:
        Kyle, A. S. (1985). Continuous Auctions and Insider Trading.
        Econometrica, 53(6), 1315-1335.

    Examples:
        >>> lambda_coef = calculate_kyle_lambda(trades, snapshots)
        >>> print(f"Kyle's lambda: {lambda_coef:.6f}")
        Kyle's lambda: 0.000245  # Low impact = high liquidity
    """
    # Validate required columns
    required_cols = {'price', 'size', 'side'}
    if not required_cols.issubset(trades_df.columns):
        raise ValueError(f"trades_df must contain columns: {required_cols}")

    if len(trades_df) < 10:
        return np.nan

    # Work on a copy to avoid mutating caller's DataFrame
    df = trades_df.copy()

    # Calculate signed order flow
    df['signed_volume'] = np.where(
        df['side'] == 'buy',
        df['size'],
        -df['size']
    )

    # Calculate price changes
    df['price_change'] = df['price'].diff()

    # Regression: price_change ~ signed_volume
    from scipy.stats import linregress
    valid_data = df[['signed_volume', 'price_change']].dropna()

    if len(valid_data) < 5:
        return np.nan

    slope, intercept, r_value, p_value, std_err = linregress(
        valid_data['signed_volume'],
        valid_data['price_change']
    )

    return slope


def calculate_amihud_illiquidity(price_series: pd.Series,
                                 volume_series: pd.Series) -> float:
    """
    Calculate Amihud illiquidity measure.

    The Amihud measure captures how much prices move per dollar traded.
    Higher values indicate lower liquidity.

    Amihud = mean(|return| / dollar_volume)

    Args:
        price_series: Time series of prices
        volume_series: Time series of volumes

    Returns:
        Amihud illiquidity ratio (higher = more illiquid)

    References:
        Amihud, Y. (2002). Illiquidity and stock returns: cross-section and
        time-series effects. Journal of Financial Markets, 5(1), 31-56.

    Examples:
        >>> illiq = calculate_amihud_illiquidity(prices, volumes)
        >>> print(f"Amihud ratio: {illiq:.8f}")
        Amihud ratio: 0.00000123  # Low = liquid, High = illiquid
    """
    returns = price_series.pct_change().abs()
    dollar_volume = price_series * volume_series

    # Filter out zero volume periods before division to avoid inf values
    valid_mask = dollar_volume > 0
    if not valid_mask.any():
        return np.nan

    illiquidity = returns[valid_mask] / dollar_volume[valid_mask]

    return illiquidity.mean()


def identify_liquidity_gaps(orderbook: OrderBookSnapshot,
                           threshold_pct: float = 2.0) -> List[Tuple[float, float]]:
    """
    Identify "air pockets" in order book.

    Air pockets are price levels with no liquidity, creating gaps where
    market orders can experience extreme slippage.

    Args:
        orderbook: Order book snapshot to analyze
        threshold_pct: Minimum gap size as percentage (default 2.0%)

    Returns:
        List of (lower_price, upper_price) tuples for gaps > threshold

    Examples:
        >>> gaps = identify_liquidity_gaps(snapshot, threshold_pct=2.0)
        >>> for lower, upper in gaps:
        ...     print(f"Gap from ${lower:.2f} to ${upper:.2f}")
        Gap from $72.50 to $74.00
        Gap from $68.00 to $70.25
    """
    gaps = []

    if not orderbook.bids:
        return gaps

    sorted_bids = sorted(orderbook.bids.keys(), reverse=True)

    for i in range(len(sorted_bids) - 1):
        upper_price = sorted_bids[i]
        lower_price = sorted_bids[i + 1]

        gap_pct = ((upper_price - lower_price) / upper_price) * 100

        if gap_pct > threshold_pct:
            gaps.append((lower_price, upper_price))

    return gaps
