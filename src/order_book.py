"""
Order Book Simulation

Simulates order book mechanics to demonstrate how market orders execute during
the August 24, 2015 flash crash, including "air pockets" and stop-loss cascades.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Order:
    """Represents a limit order in the order book."""
    price: float
    size: int

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must be positive")
        if self.size <= 0:
            raise ValueError("Size must be positive")


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

    def execute_limit_buy(self, price: float, size: int) -> List[Tuple[float, int]]:
        """
        Execute a limit buy order (only at or below limit price).

        Unlike market orders, limit orders provide price protection.
        May not fill entirely if price doesn't reach limit.

        Args:
            price: Maximum acceptable price
            size: Number of shares to buy

        Returns:
            List of (price, quantity) tuples. May be empty if no fills.
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

        # Unlike market orders, limit orders don't error on partial fills
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
    initial_book: OrderBook,
    stop_triggers: List[Tuple[float, int]],
    initial_price: float
) -> List[Tuple[float, float, int]]:
    """
    Simulate a stop-loss cascade like August 24, 2015.

    Demonstrates how stop-loss orders convert to market orders, execute at
    progressively worse prices, and trigger more stops in a vicious cycle.

    Args:
        initial_book: Starting order book state
        stop_triggers: List of (trigger_price, size) for pending stop-losses
        initial_price: Starting market price

    Returns:
        List of (trigger_price, execution_price, size) tuples showing
        how each stop-loss executed below its trigger

    Example:
        Shows IUSV stop at $108.69 executing at $87.32 (20% worse than trigger)
    """
    # Sort stops by trigger price (highest first, will trigger first)
    stops = sorted(stop_triggers, key=lambda x: x[0], reverse=True)

    executions = []
    current_price = initial_price

    for trigger_price, size in stops:
        if current_price <= trigger_price:
            # Stop triggered, becomes market order
            try:
                fills = initial_book.execute_market_sell(size)
                # Calculate average execution price
                total_value = sum(price * qty for price, qty in fills)
                total_qty = sum(qty for _, qty in fills)
                avg_price = total_value / total_qty

                executions.append((trigger_price, avg_price, size))
                current_price = avg_price  # Update market price
            except ValueError:
                # Ran out of liquidity (air pocket reached)
                break

    return executions
