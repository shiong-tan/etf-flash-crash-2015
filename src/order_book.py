"""
Order Book Simulation

Simulates order book mechanics to demonstrate how market orders execute during
the August 24, 2015 flash crash, including "air pockets" and stop-loss cascades.
"""

from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class Order:
    """Represents a limit order in the order book."""
    price: float
    size: int

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must be non-negative")
        if self.size <= 0:
            raise ValueError("Size must be greater than zero")


class OrderBook:
    """
    Simulates an order book for educational purposes.

    Demonstrates how market orders execute and how "air pockets" (sparse liquidity)
    cause large price moves during the August 24, 2015 flash crash.

    Attributes:
        bids: List of buy orders (price, size), sorted high to low
        asks: List of sell orders (price, size), sorted low to high

    Example:
        >>> book = OrderBook()
        >>> book.add_bid(100.0, 1000)
        >>> book.add_ask(100.10, 1000)
        >>> book.get_spread()
        0.10
    """

    def __init__(self):
        """Initialize an empty order book."""
        self.bids: List[Order] = []  # Buy orders (highest price first)
        self.asks: List[Order] = []  # Sell orders (lowest price first)

    def add_bid(self, price: float, size: int) -> None:
        """
        Add a buy (bid) order to the book.

        Args:
            price: Bid price
            size: Number of shares
        """
        order = Order(price, size)
        self.bids.append(order)
        # Keep bids sorted by price (highest first)
        self.bids.sort(key=lambda x: x.price, reverse=True)

    def add_ask(self, price: float, size: int) -> None:
        """
        Add a sell (ask) order to the book.

        Args:
            price: Ask price
            size: Number of shares
        """
        order = Order(price, size)
        self.asks.append(order)
        # Keep asks sorted by price (lowest first)
        self.asks.sort(key=lambda x: x.price)

    def execute_market_buy(self, size: int) -> List[Tuple[float, int]]:
        """
        Execute a market buy order, taking liquidity from asks.

        Market orders execute at best available prices. During flash crashes,
        sparse order books cause executions far from expected prices.

        Args:
            size: Number of shares to buy

        Returns:
            List of (price, quantity) tuples showing each fill

        Raises:
            ValueError: If insufficient liquidity to fill order

        Example:
            >>> book = OrderBook()
            >>> book.add_ask(100.0, 500)
            >>> book.add_ask(101.0, 500)
            >>> book.execute_market_buy(800)
            [(100.0, 500), (101.0, 300)]
        """
        if size <= 0:
            raise ValueError("Order size must be positive")

        fills = []
        remaining = size

        while remaining > 0 and self.asks:
            best_ask = self.asks[0]

            if remaining >= best_ask.size:
                # Take entire level
                fills.append((best_ask.price, best_ask.size))
                remaining -= best_ask.size
                self.asks.pop(0)
            else:
                # Partial fill
                fills.append((best_ask.price, remaining))
                self.asks[0].size -= remaining
                remaining = 0

        if remaining > 0:
            raise ValueError(
                f"Insufficient liquidity: {remaining} shares unfilled. "
                f"This demonstrates an 'air pocket' - order book ran out of sellers."
            )

        return fills

    def execute_market_sell(self, size: int) -> List[Tuple[float, int]]:
        """
        Execute a market sell order, taking liquidity from bids.

        On August 24, 2015, market sells (including converted stop-losses)
        fell through sparse bid levels, causing catastrophic prices.

        Args:
            size: Number of shares to sell

        Returns:
            List of (price, quantity) tuples showing each fill

        Raises:
            ValueError: If insufficient liquidity

        Example:
            >>> book = OrderBook()
            >>> book.add_bid(100.0, 500)
            >>> book.add_bid(99.0, 500)
            >>> fills = book.execute_market_sell(800)
            >>> # Fills at 100.0 for 500 shares, then 99.0 for 300 shares
        """
        if size <= 0:
            raise ValueError("Order size must be positive")

        fills = []
        remaining = size

        while remaining > 0 and self.bids:
            best_bid = self.bids[0]

            if remaining >= best_bid.size:
                # Take entire level
                fills.append((best_bid.price, best_bid.size))
                remaining -= best_bid.size
                self.bids.pop(0)
            else:
                # Partial fill
                fills.append((best_bid.price, remaining))
                self.bids[0].size -= remaining
                remaining = 0

        if remaining > 0:
            raise ValueError(
                f"Insufficient liquidity: {remaining} shares unfilled. "
                f"This is an 'air pocket' where bids disappeared."
            )

        return fills

    def execute_limit_buy(self, size: int, price: float) -> List[Tuple[float, int]]:
        """
        Execute a limit buy order (only at or below limit price).

        Unlike market orders, limit orders provide price protection.
        May not fill entirely if price doesn't reach limit. Unfilled
        portion is added to the order book as a resting limit order.

        Args:
            size: Number of shares to buy
            price: Maximum acceptable price

        Returns:
            List of (price, quantity) tuples showing executed fills.
            May be empty if no fills. Unfilled portion is added to book.
        """
        if size <= 0 or price <= 0:
            raise ValueError("Size and price must be positive")

        fills = []
        remaining = size

        while remaining > 0 and self.asks and self.asks[0].price <= price:
            best_ask = self.asks[0]

            if remaining >= best_ask.size:
                fills.append((best_ask.price, best_ask.size))
                remaining -= best_ask.size
                self.asks.pop(0)
            else:
                fills.append((best_ask.price, remaining))
                self.asks[0].size -= remaining
                remaining = 0

        # Add unfilled portion to book as resting limit order
        if remaining > 0:
            self.add_bid(price, remaining)

        return fills

    def get_best_bid(self) -> Optional[float]:
        """Return highest bid price, or None if no bids."""
        return self.bids[0].price if self.bids else None

    def get_best_ask(self) -> Optional[float]:
        """Return lowest ask price, or None if no asks."""
        return self.asks[0].price if self.asks else None

    def get_midpoint(self) -> Optional[float]:
        """
        Return midpoint of best bid and ask.

        On August 24, wide spreads made midpoints unreliable for fair value.
        Example: Bid $50, Ask $70 → midpoint $60, but true value $72.
        """
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()

        if best_bid is not None and best_ask is not None:
            return (best_bid + best_ask) / 2
        return None

    def get_spread(self) -> Optional[float]:
        """Return bid-ask spread in dollars."""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()

        if best_bid is not None and best_ask is not None:
            return best_ask - best_bid
        return None

    def get_spread_bps(self, reference_price: Optional[float] = None) -> Optional[float]:
        """
        Return bid-ask spread in basis points.

        Args:
            reference_price: Price to use for percentage calculation
                            (default: midpoint)
        """
        spread = self.get_spread()
        if spread is None:
            return None

        if reference_price is None:
            reference_price = self.get_midpoint()

        if reference_price is None or reference_price == 0:
            return None

        return (spread / reference_price) * 10000  # Convert to basis points

    def display_book(self, levels: int = 5) -> str:
        """
        Return string representation of order book for display.

        Args:
            levels: Number of price levels to show on each side

        Returns:
            Formatted string showing bids and asks
        """
        lines = ["Order Book:"]
        lines.append("-" * 40)
        lines.append(f"{'Price':>10} {'Size':>10} | {'Price':>10} {'Size':>10}")
        lines.append(f"{'BIDS':>20} | {'ASKS':>20}")
        lines.append("-" * 40)

        for i in range(levels):
            bid_price = f"{self.bids[i].price:.2f}" if i < len(self.bids) else ""
            bid_size = f"{self.bids[i].size}" if i < len(self.bids) else ""
            ask_price = f"{self.asks[i].price:.2f}" if i < len(self.asks) else ""
            ask_size = f"{self.asks[i].size}" if i < len(self.asks) else ""

            lines.append(
                f"{bid_price:>10} {bid_size:>10} | {ask_price:>10} {ask_size:>10}"
            )

        spread = self.get_spread()
        if spread is not None:
            lines.append("-" * 40)
            lines.append(f"Spread: ${spread:.2f}")

        return "\n".join(lines)


def simulate_stop_loss_cascade(
    initial_price: float,
    stop_levels: List[float],
    order_sizes: List[int],
    initial_book: Optional[OrderBook] = None
) -> Dict:
    """
    Simulate a stop-loss cascade like August 24, 2015.

    Demonstrates how stop-loss orders convert to market orders, execute at
    progressively worse prices, and trigger more stops in a vicious cycle.

    Args:
        initial_price: Starting market price
        stop_levels: List of stop-loss trigger prices
        order_sizes: List of order sizes for each stop level
        initial_book: Optional order book. If None, creates realistic sparse book.

    Returns:
        Dict with keys:
            - triggers: List of trigger prices
            - executions: List of actual execution prices
            - slippage: List of slippage amounts (trigger - execution)
            - slippage_pct: List of slippage percentages

    Example:
        >>> result = simulate_stop_loss_cascade(100.0, [99.0, 98.0], [500, 300])
        >>> result['triggers']
        [99.0, 98.0]
    """
    if len(stop_levels) != len(order_sizes):
        raise ValueError("stop_levels and order_sizes must have same length")

    # Create order book if not provided (sparse book with gaps)
    if initial_book is None:
        initial_book = OrderBook()
        # Create sparse order book with limited depth and gaps
        # This simulates the "air pockets" of August 24, 2015
        # Limited liquidity at each level ensures price impact/slippage
        initial_book.add_bid(initial_price - 1, 200)  # Limited depth
        initial_book.add_bid(initial_price - 2, 150)
        # Gap at initial_price - 3 (no bids)
        initial_book.add_bid(initial_price - 4, 200)
        initial_book.add_bid(initial_price - 5, 150)
        # Gap at initial_price - 6
        initial_book.add_bid(initial_price - 7, 200)
        initial_book.add_bid(initial_price - 8, 150)
        # Deeper levels with more gaps
        initial_book.add_bid(initial_price - 10, 200)
        initial_book.add_bid(initial_price - 12, 200)
        initial_book.add_bid(initial_price - 15, 200)

    # Combine and sort stops by trigger price (highest first)
    stops = sorted(zip(stop_levels, order_sizes), key=lambda x: x[0], reverse=True)

    triggers = []
    executions = []
    slippage = []
    slippage_pct = []
    current_price = initial_price

    # Simulate initial sell pressure that starts the cascade
    # If price is above highest stop, execute a small sell to trigger first stop
    if stops and current_price > stops[0][0]:
        # Execute small sell to drop price below first stop
        try:
            initial_sell_size = 100  # Small sell to start cascade
            fills = initial_book.execute_market_sell(initial_sell_size)
            if fills:
                total_value = sum(price * qty for price, qty in fills)
                total_qty = sum(qty for _, qty in fills)
                current_price = total_value / total_qty
        except ValueError:
            pass  # Not enough liquidity for initial sell

    cascade_started = False

    for trigger_price, size in stops:
        # Stop triggers if price is at or below trigger, OR if cascade has started
        # (simulating panic/momentum selling where all stops fire once cascade begins)
        should_trigger = current_price <= trigger_price or cascade_started

        if should_trigger:
            cascade_started = True  # Once started, all remaining stops trigger
            # Stop triggered, becomes market order
            try:
                fills = initial_book.execute_market_sell(size)
                if not fills:
                    # No fills but no exception - shouldn't happen but check anyway
                    break

                # Calculate average execution price
                total_value = sum(price * qty for price, qty in fills)
                total_qty = sum(qty for _, qty in fills)
                avg_price = total_value / total_qty

                triggers.append(trigger_price)
                executions.append(avg_price)
                slip = trigger_price - avg_price
                slippage.append(slip)
                slippage_pct.append((slip / trigger_price) * 100)

                current_price = avg_price  # Update market price
            except ValueError as e:
                # Ran out of liquidity (air pocket reached)
                break

    return {
        'triggers': triggers,
        'executions': executions,
        'slippage': slippage,
        'slippage_pct': slippage_pct
    }
