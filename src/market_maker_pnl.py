"""
Market maker P&L simulation and risk analysis for flash crash scenarios.
Models realistic hedging constraints and inventory risk.

This module simulates market maker behavior during extreme market conditions,
particularly the August 24, 2015 ETF flash crash. It models how market makers
manage inventory, hedge risk, and calculate P&L under stress.

Classes:
    HedgeStatus: Enum for market maker hedging capability
    MarketMakerPosition: Dataclass representing position and risk
    MarketMakerSimulator: Simulates market maker behavior and P&L

Functions:
    simulate_market_maker_crisis: Run complete crisis simulation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class HedgeStatus(Enum):
    """
    Market maker hedging capability status.

    During normal markets, market makers can fully hedge their inventory.
    During flash crashes, hedging becomes difficult or impossible due to
    trading halts in underlying securities.
    """
    FULL = "full_hedge_available"
    PARTIAL = "partial_hedge_available"
    NONE = "no_hedge_available"


@dataclass
class MarketMakerPosition:
    """
    Represents market maker's position and risk at a point in time.

    Market makers maintain inventory in ETFs and hedge that inventory
    by taking offsetting positions in the underlying securities or futures.

    Attributes:
        etf_inventory: Shares of ETF (positive = long, negative = short)
        underlying_hedge: Offsetting position in basket of stocks
        futures_hedge: Position in S&P 500 futures
        etf_entry_price: Average entry price for ETF position
        hedge_entry_price: Average entry price for hedge
        timestamp: Time of position snapshot
        fair_value: Current fair value (NAV/iNAV)
    """
    etf_inventory: int  # positive = long, negative = short
    underlying_hedge: int  # offsetting position in basket
    futures_hedge: int  # S&P futures position

    etf_entry_price: float
    hedge_entry_price: Optional[float]

    timestamp: pd.Timestamp
    fair_value: float

    def net_delta(self) -> int:
        """
        Calculate net directional exposure.

        Net delta represents the market maker's net exposure to market moves.
        In normal conditions, this should be close to zero (market neutral).

        Returns:
            Net directional exposure in shares

        Examples:
            >>> pos = MarketMakerPosition(etf_inventory=10000, underlying_hedge=-10000, ...)
            >>> pos.net_delta()
            0  # Perfectly hedged
        """
        # ETF gives 1:1 delta exposure
        # Underlying hedge and futures should offset
        return self.etf_inventory + self.underlying_hedge + self.futures_hedge

    def inventory_risk_usd(self, current_etf_price: float) -> float:
        """
        Calculate mark-to-market P&L on current position.

        Note: This simplified calculation does not include futures P&L.
        The futures_hedge position is tracked but not included in P&L.
        For production use, futures P&L should be added.

        Args:
            current_etf_price: Current market price of ETF

        Returns:
            Unrealized P&L in dollars (excluding futures)

        Examples:
            >>> pos = MarketMakerPosition(etf_inventory=10000, etf_entry_price=100.0, ...)
            >>> pos.inventory_risk_usd(102.0)
            20000.0  # $2 profit per share * 10000 shares
        """
        # P&L on ETF position
        etf_pnl = self.etf_inventory * (current_etf_price - self.etf_entry_price)

        # P&L on hedge
        hedge_pnl = 0.0
        if self.hedge_entry_price:
            hedge_pnl = self.underlying_hedge * (self.fair_value - self.hedge_entry_price)

        # TODO: Add futures P&L calculation
        # Would require tracking futures_entry_price and current_futures_price

        return etf_pnl + hedge_pnl

    def gamma_risk(self) -> float:
        """
        Estimate gamma risk (convexity of P&L).

        Gamma measures how delta changes with price moves. Higher gamma
        means P&L is more sensitive to large price swings.

        Returns:
            Gamma risk estimate

        Note:
            This is a simplified estimate. Real gamma calculation would
            require option positions and volatility surface.
        """
        # Simplified: gamma ~ abs(net_delta) * volatility
        # Higher during crisis (assume 40% vol)
        return abs(self.net_delta()) * 0.40


class MarketMakerSimulator:
    """
    Simulate market maker behavior during flash crash.

    This class models how market makers:
    - Provide liquidity by taking the other side of trades
    - Manage inventory limits
    - Hedge positions to remain market neutral
    - Adjust spreads based on risk and hedging capability
    - Withdraw from market when hedging becomes impossible

    Key insights:
    - Market makers provide liquidity but need to hedge inventory
    - During crisis, hedging becomes impossible (halts in underlying)
    - Without hedging capability, they must withdraw or face catastrophic losses
    - This withdrawal amplifies the crisis by removing liquidity

    Attributes:
        symbol: ETF ticker
        capital: Total capital available
        initial_capital: Starting capital (for return calculation)
        max_inventory: Maximum inventory limit (shares)
        target_spread_bps: Target spread in basis points
        position: Current position and risk
        pnl_history: History of P&L snapshots
        position_history: History of positions
        hedge_status: Current hedging capability
        active: Whether still quoting markets
    """

    def __init__(self,
                 symbol: str,
                 initial_capital: float = 10_000_000,
                 max_inventory: int = 100_000,
                 target_spread_bps: float = 2.0):
        """
        Initialize market maker simulator.

        Args:
            symbol: ETF ticker
            initial_capital: Starting capital in dollars
            max_inventory: Maximum inventory in shares
            target_spread_bps: Target spread in normal conditions

        Raises:
            ValueError: If parameters are invalid
        """
        # Input validation
        if initial_capital <= 0:
            raise ValueError(f"initial_capital must be positive, got {initial_capital}")
        if max_inventory <= 0:
            raise ValueError(f"max_inventory must be positive, got {max_inventory}")
        if target_spread_bps <= 0:
            raise ValueError(f"target_spread_bps must be positive, got {target_spread_bps}")

        self.symbol = symbol
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.max_inventory = max_inventory
        self.target_spread_bps = target_spread_bps

        self.position = MarketMakerPosition(
            etf_inventory=0,
            underlying_hedge=0,
            futures_hedge=0,
            etf_entry_price=0.0,
            hedge_entry_price=None,
            timestamp=pd.Timestamp.now(),
            fair_value=0.0
        )

        self.pnl_history = []
        self.position_history = []
        self.hedge_status = HedgeStatus.FULL

        self.active = True  # Still quoting markets

    def quote_market(self,
                    fair_value: float,
                    hedge_status: HedgeStatus,
                    volatility: float) -> Optional[Dict[str, float]]:
        """
        Decide whether and how to quote the market.

        Market makers adjust their quotes based on:
        - Current inventory (skew quotes to reduce inventory)
        - Hedging capability (widen spreads if can't hedge)
        - Market volatility (widen spreads in volatile conditions)
        - Inventory limits (stop quoting if at limit)

        Args:
            fair_value: Current fair value (NAV/iNAV)
            hedge_status: Current hedging capability
            volatility: Current market volatility (annualized)

        Returns:
            Quote dictionary with bid, ask, sizes and spread_bps,
            or None if withdrawing quotes

        Examples:
            >>> mm = MarketMakerSimulator('SPY')
            >>> quote = mm.quote_market(200.0, HedgeStatus.FULL, 0.20)
            >>> quote['spread_bps']
            2.0  # Normal spread
        """
        # Check if inventory limit reached
        if abs(self.position.etf_inventory) > self.max_inventory * 0.9:
            # Near limit - quote only to reduce inventory
            if self.position.etf_inventory > 0:
                # Long - only offer (sell)
                spread = fair_value * (volatility * 5)  # Very wide
                return {
                    'bid': None,
                    'ask': fair_value + spread/2,
                    'bid_size': 0,
                    'ask_size': min(10000, abs(self.position.etf_inventory)),
                    'spread_bps': np.inf
                }
            else:
                # Short - only bid (buy)
                spread = fair_value * (volatility * 5)
                return {
                    'bid': fair_value - spread/2,
                    'ask': None,
                    'bid_size': min(10000, abs(self.position.etf_inventory)),
                    'ask_size': 0,
                    'spread_bps': np.inf
                }

        # Adjust spread based on hedge availability and volatility
        if hedge_status == HedgeStatus.FULL:
            # Normal conditions - tight spreads
            spread_bps = self.target_spread_bps * (1 + volatility / 0.20)

        elif hedge_status == HedgeStatus.PARTIAL:
            # Some components halted - widen spreads significantly
            spread_bps = self.target_spread_bps * 10 * (1 + volatility / 0.20)

        else:  # HedgeStatus.NONE
            # Cannot hedge - consider withdrawing
            if volatility > 0.50:  # 50% volatility = panic
                self.active = False
                return None  # Withdraw quotes
            else:
                # Quote with massive spreads
                spread_bps = self.target_spread_bps * 100

        spread = fair_value * (spread_bps / 10000)

        # INVENTORY-BASED SKEWING
        # Skew quotes to encourage mean reversion
        # If long (+inventory): skew quotes DOWN to encourage selling
        # If short (-inventory): skew quotes UP to encourage buying
        inventory_ratio = self.position.etf_inventory / self.max_inventory

        # Skew factor: 0.5 bps per 1% of max inventory
        # At max inventory (100%), skew = 50 bps = 0.5% of price
        skew_bps = inventory_ratio * 50  # basis points
        skew = fair_value * (skew_bps / 10000)

        # Apply skew to both bid and ask (shifts entire quote, not spread)
        bid = fair_value - spread/2 - skew
        ask = fair_value + spread/2 - skew

        return {
            'bid': bid,
            'ask': ask,
            'bid_size': 10000,
            'ask_size': 10000,
            'spread_bps': spread_bps
        }

    def execute_trade(self,
                     size: int,
                     price: float,
                     side: str,
                     fair_value: float,
                     can_hedge: bool) -> bool:
        """
        Execute trade as market maker.

        Market maker takes the opposite side of the incoming order.
        Buy order → Market maker sells
        Sell order → Market maker buys

        Args:
            size: Number of shares in incoming order
            price: Execution price
            side: Incoming order side ('buy' or 'sell')
            fair_value: Current fair value
            can_hedge: Whether hedging is possible

        Returns:
            True if trade accepted, False if rejected

        Examples:
            >>> mm = MarketMakerSimulator('SPY')
            >>> mm.execute_trade(1000, 200.0, 'buy', 200.0, True)
            True  # Trade accepted
        """
        # Market maker takes opposite side
        mm_side = 'sell' if side == 'buy' else 'buy'
        mm_size = size if mm_side == 'buy' else -size

        # Check inventory limits
        new_inventory = self.position.etf_inventory + mm_size
        if abs(new_inventory) > self.max_inventory:
            return False  # Reject trade

        # Update position with correct entry price calculation
        if new_inventory == 0:
            # Flat position - reset entry price
            self.position.etf_entry_price = 0.0
        elif (self.position.etf_inventory > 0 and new_inventory < 0) or \
             (self.position.etf_inventory < 0 and new_inventory > 0):
            # Position crossed zero - new entry price is current trade price
            self.position.etf_entry_price = price
        elif abs(new_inventory) > abs(self.position.etf_inventory):
            # Adding to existing position - weighted average
            old_value = self.position.etf_inventory * self.position.etf_entry_price
            new_value = mm_size * price
            self.position.etf_entry_price = (old_value + new_value) / new_inventory
        # else: Reducing position - keep original entry price

        self.position.etf_inventory = new_inventory
        self.position.fair_value = fair_value
        self.position.timestamp = pd.Timestamp.now()

        # Attempt to hedge
        if can_hedge:
            # Calculate new hedge size
            new_hedge_size = -self.position.etf_inventory
            hedge_delta = new_hedge_size - self.position.underlying_hedge

            if new_hedge_size == 0:
                # Position is flat - reset hedge
                self.position.underlying_hedge = 0
                self.position.hedge_entry_price = None
            elif hedge_delta != 0:
                # Adding to hedge - calculate weighted average entry price
                if self.position.hedge_entry_price is not None and self.position.underlying_hedge != 0:
                    old_value = self.position.underlying_hedge * self.position.hedge_entry_price
                    new_value = hedge_delta * fair_value
                    self.position.hedge_entry_price = (old_value + new_value) / new_hedge_size
                else:
                    self.position.hedge_entry_price = fair_value

                self.position.underlying_hedge = new_hedge_size

        # Record position
        self.position_history.append({
            'timestamp': self.position.timestamp,
            'etf_inventory': self.position.etf_inventory,
            'hedge_position': self.position.underlying_hedge,
            'net_delta': self.position.net_delta(),
            'fair_value': fair_value,
            'etf_price': price
        })

        return True

    def mark_to_market(self, etf_price: float) -> Dict[str, float]:
        """
        Calculate current P&L.

        Mark-to-market calculates the unrealized P&L if all positions
        were closed at current market prices.

        Args:
            etf_price: Current ETF market price

        Returns:
            Dictionary with P&L breakdown:
                - etf_pnl: P&L on ETF position
                - hedge_pnl: P&L on hedge positions
                - total_pnl: Net P&L
                - return_pct: Return on initial capital
                - capital: Current capital

        Examples:
            >>> mm = MarketMakerSimulator('SPY', initial_capital=1_000_000)
            >>> mm.execute_trade(10000, 200.0, 'sell', 200.0, True)
            >>> pnl = mm.mark_to_market(202.0)
            >>> pnl['total_pnl']
            0.0  # Hedged position, no P&L
        """
        inventory_pnl = self.position.inventory_risk_usd(etf_price)

        pnl_dict = {
            'timestamp': pd.Timestamp.now(),
            'etf_pnl': inventory_pnl,
            'hedge_pnl': 0.0,  # Simplified - hedge P&L included in inventory_pnl
            'total_pnl': inventory_pnl,
            'return_pct': (inventory_pnl / self.initial_capital) * 100,
            'capital': self.initial_capital + inventory_pnl
        }

        self.pnl_history.append(pnl_dict)
        return pnl_dict

    def calculate_risk_metrics(self) -> Dict[str, float]:
        """
        Calculate risk metrics.

        Risk metrics help assess the market maker's exposure and
        potential for losses under various scenarios.

        Returns:
            Dictionary with risk metrics:
                - current_delta: Net directional exposure
                - gamma_risk: Convexity risk
                - inventory_pct: Inventory as % of limit
                - var_95: Value at Risk (95% confidence)
                - expected_shortfall: Expected loss beyond VaR
                - max_drawdown: Maximum peak-to-trough loss
                - sharpe_ratio: Risk-adjusted return

        Examples:
            >>> mm = MarketMakerSimulator('SPY')
            >>> # ... execute some trades ...
            >>> metrics = mm.calculate_risk_metrics()
            >>> metrics['current_delta']
            0  # Market neutral
        """
        if not self.pnl_history:
            return {}

        pnl_series = pd.Series([p['total_pnl'] for p in self.pnl_history])

        # Calculate VaR and Expected Shortfall
        var_95 = pnl_series.quantile(0.05)
        tail_losses = pnl_series[pnl_series < var_95]
        expected_shortfall = tail_losses.mean() if len(tail_losses) > 0 else var_95

        return {
            'current_delta': self.position.net_delta(),
            'gamma_risk': self.position.gamma_risk(),
            'inventory_pct': (abs(self.position.etf_inventory) / self.max_inventory) * 100,
            'var_95': var_95,  # 5th percentile loss
            'expected_shortfall': expected_shortfall,
            'max_drawdown': (pnl_series - pnl_series.cummax()).min(),
            'sharpe_ratio': pnl_series.mean() / pnl_series.std() if pnl_series.std() > 0 else 0
        }


def simulate_market_maker_crisis(
    fair_value: float,
    crisis_scenario: Dict,
    mm_params: Optional[Dict] = None
) -> Tuple[MarketMakerSimulator, pd.DataFrame]:
    """
    Simulate market maker behavior through crisis.

    This function runs a complete simulation of market maker behavior
    during a flash crash scenario, tracking P&L, inventory, and risk metrics.

    Args:
        fair_value: Starting fair value (NAV/iNAV)
        crisis_scenario: Dictionary with timeline and market conditions:
            - 'timeline': List of timestamps
            - 'etf_prices': ETF market prices at each time
            - 'hedge_availability': Boolean array (can hedge at time t?)
            - 'volatility': Volatility at each time
            - 'order_flow': Net buying/selling pressure at each time
        mm_params: Optional market maker parameters

    Returns:
        Tuple of (MarketMakerSimulator instance, DataFrame with results)

    Examples:
        >>> scenario = {
        ...     'timeline': pd.date_range('2015-08-24 09:30', periods=10, freq='1min'),
        ...     'etf_prices': [200, 199, 195, 190, 185, 180, 185, 190, 195, 198],
        ...     'hedge_availability': [True] * 5 + [False] * 5,
        ...     'volatility': [0.2] * 5 + [0.6] * 5,
        ...     'order_flow': [-1000, -2000, -5000, -10000, -15000, -5000, 2000, 3000, 2000, 1000]
        ... }
        >>> mm, results = simulate_market_maker_crisis(200.0, scenario)
        >>> results['pnl'].iloc[-1]
        -50000.0  # Example P&L at end
    """
    mm_params = mm_params or {}
    mm = MarketMakerSimulator(
        symbol='ETF',
        **mm_params
    )

    results = []

    for i, timestamp in enumerate(crisis_scenario['timeline']):
        etf_price = crisis_scenario['etf_prices'][i]
        can_hedge = crisis_scenario['hedge_availability'][i]
        vol = crisis_scenario['volatility'][i]
        flow = crisis_scenario['order_flow'][i]

        # Determine hedge status
        if can_hedge:
            hedge_status = HedgeStatus.FULL
        else:
            hedge_status = HedgeStatus.NONE

        # Get quote
        quote = mm.quote_market(fair_value, hedge_status, vol)

        # Process order flow
        if quote and flow != 0:
            side = 'buy' if flow > 0 else 'sell'
            size = abs(flow)

            if quote['bid'] and side == 'sell':
                mm.execute_trade(size, quote['bid'], side, fair_value, can_hedge)
            elif quote['ask'] and side == 'buy':
                mm.execute_trade(size, quote['ask'], side, fair_value, can_hedge)

        # Mark to market
        pnl = mm.mark_to_market(etf_price)

        results.append({
            'timestamp': timestamp,
            'etf_price': etf_price,
            'fair_value': fair_value,
            'discount_pct': ((etf_price / fair_value) - 1) * 100,
            'spread_bps': quote['spread_bps'] if quote else np.inf,
            'mm_active': mm.active,
            'inventory': mm.position.etf_inventory,
            'pnl': pnl['total_pnl'],
            'cumulative_return_pct': pnl['return_pct']
        })

    return mm, pd.DataFrame(results)
