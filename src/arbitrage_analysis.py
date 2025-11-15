"""
Arbitrage analysis for ETF flash crash scenarios.

This module analyzes arbitrage opportunities and barriers that prevented
arbitrage from functioning during the August 24, 2015 flash crash.

Classes:
    ArbitrageOpportunity: Dataclass representing an arbitrage opportunity
    ETFArbitrageAnalyzer: Analyzer for ETF arbitrage opportunities and barriers

Functions:
    calculate_no_arbitrage_bounds: Calculate price bounds preventing arbitrage
    identify_arbitrage_barriers: Identify barriers preventing arbitrage execution
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ArbitrageType(Enum):
    """Type of arbitrage opportunity."""
    CREATION = "creation"  # ETF trading at premium
    REDEMPTION = "redemption"  # ETF trading at discount
    NONE = "none"  # No opportunity


class BarrierType(Enum):
    """Types of barriers preventing arbitrage."""
    HALTED_COMPONENTS = "halted_components"  # Underlying stocks halted
    STALE_INAV = "stale_inav"  # iNAV calculation unreliable
    LIQUIDITY_COST = "liquidity_cost"  # Transaction costs too high
    CAPITAL_CONSTRAINT = "capital_constraint"  # Insufficient capital
    SETTLEMENT_RISK = "settlement_risk"  # T+settlement mismatch


@dataclass
class ArbitrageOpportunity:
    """
    Represents an arbitrage opportunity in an ETF.

    Attributes:
        timestamp: Time of opportunity
        etf_symbol: ETF ticker
        etf_price: Current ETF market price
        inav: Indicative NAV
        spread_pct: Percentage deviation (positive = premium, negative = discount)
        arb_type: Type of arbitrage (creation or redemption)
        gross_profit_per_unit: Profit before costs (per share)
        transaction_costs: Transaction costs (per share)
        net_profit_per_unit: Net profit after costs (per share)
        is_profitable: Whether opportunity is profitable after costs
        barriers: List of barriers preventing execution
    """
    timestamp: pd.Timestamp
    etf_symbol: str
    etf_price: float
    inav: float
    spread_pct: float
    arb_type: ArbitrageType
    gross_profit_per_unit: float
    transaction_costs: float
    net_profit_per_unit: float
    is_profitable: bool
    barriers: List[BarrierType]

    def is_executable(self) -> bool:
        """Check if arbitrage is executable despite barriers."""
        return self.is_profitable and len(self.barriers) == 0


class ETFArbitrageAnalyzer:
    """
    Analyze ETF arbitrage opportunities and execution barriers.

    This analyzer identifies arbitrage opportunities and the barriers that
    prevented arbitrageurs from exploiting them during the flash crash.

    Attributes:
        transaction_costs_bps: Transaction costs in basis points
        creation_unit_size: Standard creation unit size
        min_profit_threshold: Minimum profit threshold for execution
    """

    def __init__(self,
                 transaction_costs_bps: float = 25.0,
                 creation_unit_size: int = 50_000,
                 min_profit_threshold: float = 0.001):
        """
        Initialize arbitrage analyzer.

        Args:
            transaction_costs_bps: Transaction costs in basis points (default 25)
            creation_unit_size: Number of shares in creation unit (default 50,000)
            min_profit_threshold: Minimum profit as fraction (default 0.001 = 0.1%)
        """
        self.transaction_costs_bps = transaction_costs_bps
        self.creation_unit_size = creation_unit_size
        self.min_profit_threshold = min_profit_threshold

    def analyze_opportunity(self,
                          timestamp: pd.Timestamp,
                          etf_symbol: str,
                          etf_price: float,
                          inav: float,
                          halted_component_pct: float = 0.0,
                          inav_staleness_minutes: float = 0.0) -> ArbitrageOpportunity:
        """
        Analyze a potential arbitrage opportunity.

        Args:
            timestamp: Time of analysis
            etf_symbol: ETF ticker symbol
            etf_price: Current market price of ETF
            inav: Indicative NAV
            halted_component_pct: Percentage of components halted (0-100)
            inav_staleness_minutes: Minutes since last iNAV update

        Returns:
            ArbitrageOpportunity object
        """
        # Calculate spread
        spread = etf_price - inav
        spread_pct = (spread / inav) * 100

        # Determine arbitrage type
        if spread_pct > 0:
            arb_type = ArbitrageType.CREATION
        elif spread_pct < 0:
            arb_type = ArbitrageType.REDEMPTION
        else:
            arb_type = ArbitrageType.NONE

        # Calculate profits
        gross_profit_per_unit = abs(spread)
        transaction_costs = etf_price * (self.transaction_costs_bps / 10000)
        net_profit_per_unit = gross_profit_per_unit - transaction_costs
        is_profitable = net_profit_per_unit > (etf_price * self.min_profit_threshold)

        # Identify barriers
        barriers = self._identify_barriers(
            spread_pct=spread_pct,
            halted_component_pct=halted_component_pct,
            inav_staleness_minutes=inav_staleness_minutes,
            net_profit_per_unit=net_profit_per_unit,
            etf_price=etf_price
        )

        return ArbitrageOpportunity(
            timestamp=timestamp,
            etf_symbol=etf_symbol,
            etf_price=etf_price,
            inav=inav,
            spread_pct=spread_pct,
            arb_type=arb_type,
            gross_profit_per_unit=gross_profit_per_unit,
            transaction_costs=transaction_costs,
            net_profit_per_unit=net_profit_per_unit,
            is_profitable=is_profitable,
            barriers=barriers
        )

    def _identify_barriers(self,
                          spread_pct: float,
                          halted_component_pct: float,
                          inav_staleness_minutes: float,
                          net_profit_per_unit: float,
                          etf_price: float) -> List[BarrierType]:
        """
        Identify barriers preventing arbitrage execution.

        Args:
            spread_pct: Percentage spread
            halted_component_pct: Percentage of halted components
            inav_staleness_minutes: iNAV staleness in minutes
            net_profit_per_unit: Net profit per share
            etf_price: ETF price

        Returns:
            List of identified barriers
        """
        barriers = []

        # Barrier 1: Halted components prevent hedging
        if halted_component_pct > 20:  # >20% components halted
            barriers.append(BarrierType.HALTED_COMPONENTS)

        # Barrier 2: Stale iNAV makes fair value unknown
        if inav_staleness_minutes > 5:  # >5 minutes stale
            barriers.append(BarrierType.STALE_INAV)

        # Barrier 3: Liquidity costs exceed gross profit
        if net_profit_per_unit < 0:
            barriers.append(BarrierType.LIQUIDITY_COST)

        # Barrier 4: Extreme spreads suggest broken market
        if abs(spread_pct) > 20:  # >20% deviation
            # Such extreme spreads during flash crash indicated broken price discovery
            # not genuine arbitrage
            barriers.append(BarrierType.SETTLEMENT_RISK)

        return barriers

    def calculate_required_capital(self,
                                   etf_price: float,
                                   target_units: int = 1) -> float:
        """
        Calculate capital required for arbitrage trade.

        Args:
            etf_price: Current ETF price
            target_units: Number of creation units to trade (default 1)

        Returns:
            Required capital in dollars
        """
        shares_per_trade = self.creation_unit_size * target_units
        capital_required = etf_price * shares_per_trade

        # Add buffer for margin and costs (20%)
        return capital_required * 1.20


def calculate_no_arbitrage_bounds(
    nav: float,
    transaction_costs_bps: float = 25.0
) -> Tuple[float, float]:
    """
    Calculate no-arbitrage price bounds.

    Within these bounds, arbitrage is unprofitable after transaction costs.

    Args:
        nav: Net asset value (fair value)
        transaction_costs_bps: Transaction costs in basis points

    Returns:
        Tuple of (lower_bound, upper_bound)

    Example:
        >>> calculate_no_arbitrage_bounds(100.0, 25.0)
        (99.75, 100.25)
    """
    cost_fraction = transaction_costs_bps / 10000
    lower_bound = nav * (1 - cost_fraction)
    upper_bound = nav * (1 + cost_fraction)

    return (lower_bound, upper_bound)


def identify_arbitrage_barriers(
    etf_prices: pd.Series,
    inav_values: pd.Series,
    halted_components: pd.Series,
    inav_update_times: pd.Series,
    transaction_costs_bps: float = 25.0
) -> pd.DataFrame:
    """
    Identify arbitrage barriers across a time series.

    Analyzes each time point to determine what prevented arbitrage from
    functioning during the flash crash.

    Args:
        etf_prices: Time series of ETF prices
        inav_values: Time series of iNAV values
        halted_components: Time series of percentage of halted components
        inav_update_times: Time series of last iNAV update times
        transaction_costs_bps: Transaction costs in basis points

    Returns:
        DataFrame with columns:
            - timestamp
            - etf_price
            - inav
            - spread_pct
            - arb_type
            - profitable
            - executable
            - barriers (comma-separated list)

    Example:
        >>> barriers_df = identify_arbitrage_barriers(
        ...     etf_prices, inav_values, halted_pct, update_times
        ... )
        >>> print(barriers_df[barriers_df['spread_pct'].abs() > 10])
    """
    analyzer = ETFArbitrageAnalyzer(transaction_costs_bps=transaction_costs_bps)

    results = []
    for timestamp in etf_prices.index:
        etf_price = etf_prices[timestamp]
        inav = inav_values[timestamp]
        halted_pct = halted_components[timestamp]

        # Calculate staleness
        last_update = inav_update_times[timestamp]
        staleness_minutes = (timestamp - last_update).total_seconds() / 60

        # Analyze opportunity
        opp = analyzer.analyze_opportunity(
            timestamp=timestamp,
            etf_symbol="ETF",
            etf_price=etf_price,
            inav=inav,
            halted_component_pct=halted_pct,
            inav_staleness_minutes=staleness_minutes
        )

        results.append({
            'timestamp': timestamp,
            'etf_price': etf_price,
            'inav': inav,
            'spread_pct': opp.spread_pct,
            'arb_type': opp.arb_type.value,
            'profitable': opp.is_profitable,
            'executable': opp.is_executable(),
            'barriers': ','.join([b.value for b in opp.barriers]),
            'num_barriers': len(opp.barriers)
        })

    return pd.DataFrame(results)
