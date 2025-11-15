"""
Comprehensive test suite for market_maker_pnl.py module.

This test suite covers:
- MarketMakerPosition dataclass methods
- MarketMakerSimulator initialization and validation
- Quote generation under various market conditions
- Trade execution and position management
- P&L calculation and mark-to-market
- Risk metrics calculation
- Full crisis simulation

Test Coverage:
- Normal market conditions
- Crisis scenarios (hedge loss, high volatility)
- Edge cases (zero inventory, inventory limits, position crossing zero)
- Input validation
- Regression tests for fixed bugs
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from market_maker_pnl import (
    HedgeStatus,
    MarketMakerPosition,
    MarketMakerSimulator,
    simulate_market_maker_crisis
)


class TestHedgeStatus:
    """Tests for HedgeStatus enum"""

    def test_hedge_status_values(self):
        """Test that HedgeStatus enum has correct values"""
        assert HedgeStatus.FULL.value == "full_hedge_available"
        assert HedgeStatus.PARTIAL.value == "partial_hedge_available"
        assert HedgeStatus.NONE.value == "no_hedge_available"

    def test_hedge_status_enum_members(self):
        """Test that all expected enum members exist"""
        assert len(HedgeStatus) == 3
        assert HedgeStatus.FULL in HedgeStatus
        assert HedgeStatus.PARTIAL in HedgeStatus
        assert HedgeStatus.NONE in HedgeStatus


class TestMarketMakerPosition:
    """Tests for MarketMakerPosition dataclass and its methods"""

    def setup_method(self):
        """Create sample position for testing"""
        self.timestamp = pd.Timestamp.now()
        self.position = MarketMakerPosition(
            etf_inventory=10000,
            underlying_hedge=-10000,
            futures_hedge=0,
            etf_entry_price=100.0,
            hedge_entry_price=100.0,
            timestamp=self.timestamp,
            fair_value=100.0
        )

    def test_net_delta_zero_perfectly_hedged(self):
        """Test net delta calculation when perfectly hedged"""
        delta = self.position.net_delta()
        assert delta == 0  # 10000 + (-10000) + 0 = 0

    def test_net_delta_partial_hedge(self):
        """Test net delta with partial hedge"""
        self.position.underlying_hedge = -5000
        delta = self.position.net_delta()
        assert delta == 5000  # 10000 + (-5000) + 0 = 5000

    def test_net_delta_unhedged(self):
        """Test net delta with no hedge"""
        self.position.underlying_hedge = 0
        delta = self.position.net_delta()
        assert delta == 10000

    def test_net_delta_with_futures(self):
        """Test net delta including futures position"""
        self.position.futures_hedge = -2000
        self.position.underlying_hedge = -8000
        delta = self.position.net_delta()
        assert delta == 0  # 10000 + (-8000) + (-2000) = 0

    def test_net_delta_short_position(self):
        """Test net delta with short ETF position"""
        self.position.etf_inventory = -15000
        self.position.underlying_hedge = 15000
        delta = self.position.net_delta()
        assert delta == 0

    def test_inventory_risk_usd_long_position_profit(self):
        """Test P&L calculation for long position with profit"""
        current_price = 102.0
        pnl = self.position.inventory_risk_usd(current_price)

        # ETF P&L: 10000 * (102 - 100) = 20000
        # Hedge P&L: -10000 * (100 - 100) = 0
        # Total: 20000
        expected_pnl = 20000.0
        assert abs(pnl - expected_pnl) < 0.01

    def test_inventory_risk_usd_long_position_loss(self):
        """Test P&L calculation for long position with loss"""
        current_price = 98.0
        pnl = self.position.inventory_risk_usd(current_price)

        # ETF P&L: 10000 * (98 - 100) = -20000
        # Hedge P&L: -10000 * (100 - 100) = 0
        # Total: -20000
        expected_pnl = -20000.0
        assert abs(pnl - expected_pnl) < 0.01

    def test_inventory_risk_usd_with_hedge_profit(self):
        """Test P&L calculation with hedge position showing profit"""
        current_price = 105.0
        self.position.fair_value = 106.0  # Fair value moved up
        pnl = self.position.inventory_risk_usd(current_price)

        # ETF P&L: 10000 * (105 - 100) = 50000
        # Hedge P&L: -10000 * (106 - 100) = -60000
        # Total: -10000 (hedge offset most of ETF gain)
        expected_pnl = -10000.0
        assert abs(pnl - expected_pnl) < 0.01

    def test_inventory_risk_usd_short_position(self):
        """Test P&L calculation for short position"""
        self.position.etf_inventory = -5000
        self.position.etf_entry_price = 100.0
        self.position.underlying_hedge = 5000
        self.position.hedge_entry_price = 100.0

        current_price = 95.0
        self.position.fair_value = 95.0
        pnl = self.position.inventory_risk_usd(current_price)

        # ETF P&L: -5000 * (95 - 100) = 25000 (profit on short)
        # Hedge P&L: 5000 * (95 - 100) = -25000 (loss on long hedge)
        # Total: 0 (perfectly hedged)
        assert abs(pnl) < 0.01

    def test_inventory_risk_usd_zero_inventory(self):
        """Test P&L calculation with zero inventory"""
        self.position.etf_inventory = 0
        self.position.underlying_hedge = 0
        pnl = self.position.inventory_risk_usd(100.0)
        assert pnl == 0.0

    def test_inventory_risk_usd_no_hedge_entry_price(self):
        """Test P&L calculation when hedge_entry_price is None"""
        self.position.hedge_entry_price = None
        current_price = 105.0
        pnl = self.position.inventory_risk_usd(current_price)

        # Only ETF P&L
        expected_pnl = 10000 * (105 - 100)
        assert abs(pnl - expected_pnl) < 0.01

    def test_gamma_risk_calculation(self):
        """Test gamma risk estimation"""
        gamma = self.position.gamma_risk()

        # Net delta = 0, so gamma should be 0
        assert gamma == 0.0

    def test_gamma_risk_unhedged_position(self):
        """Test gamma risk with unhedged position"""
        self.position.underlying_hedge = 0
        gamma = self.position.gamma_risk()

        # abs(10000) * 0.40 = 4000
        expected_gamma = 10000 * 0.40
        assert abs(gamma - expected_gamma) < 0.01


class TestMarketMakerSimulatorInit:
    """Tests for MarketMakerSimulator initialization"""

    def test_initialization_default_params(self):
        """Test initialization with default parameters"""
        mm = MarketMakerSimulator(symbol='SPY')

        assert mm.symbol == 'SPY'
        assert mm.capital == 10_000_000
        assert mm.initial_capital == 10_000_000
        assert mm.max_inventory == 100_000
        assert mm.target_spread_bps == 2.0
        assert mm.position.etf_inventory == 0
        assert mm.position.underlying_hedge == 0
        assert mm.position.etf_entry_price == 0.0
        assert mm.position.hedge_entry_price is None
        assert mm.hedge_status == HedgeStatus.FULL
        assert mm.active is True
        assert len(mm.pnl_history) == 0
        assert len(mm.position_history) == 0

    def test_initialization_custom_params(self):
        """Test initialization with custom parameters"""
        mm = MarketMakerSimulator(
            symbol='QQQ',
            initial_capital=5_000_000,
            max_inventory=50_000,
            target_spread_bps=5.0
        )

        assert mm.symbol == 'QQQ'
        assert mm.capital == 5_000_000
        assert mm.max_inventory == 50_000
        assert mm.target_spread_bps == 5.0

    def test_initialization_invalid_capital(self):
        """Test that negative capital raises ValueError"""
        with pytest.raises(ValueError, match="initial_capital must be positive"):
            MarketMakerSimulator(symbol='SPY', initial_capital=-100)

    def test_initialization_zero_capital(self):
        """Test that zero capital raises ValueError"""
        with pytest.raises(ValueError, match="initial_capital must be positive"):
            MarketMakerSimulator(symbol='SPY', initial_capital=0)

    def test_initialization_invalid_inventory(self):
        """Test that negative max_inventory raises ValueError"""
        with pytest.raises(ValueError, match="max_inventory must be positive"):
            MarketMakerSimulator(symbol='SPY', max_inventory=-1000)

    def test_initialization_zero_inventory(self):
        """Test that zero max_inventory raises ValueError"""
        with pytest.raises(ValueError, match="max_inventory must be positive"):
            MarketMakerSimulator(symbol='SPY', max_inventory=0)

    def test_initialization_invalid_spread(self):
        """Test that negative target_spread_bps raises ValueError"""
        with pytest.raises(ValueError, match="target_spread_bps must be positive"):
            MarketMakerSimulator(symbol='SPY', target_spread_bps=-1.0)

    def test_initialization_zero_spread(self):
        """Test that zero target_spread_bps raises ValueError"""
        with pytest.raises(ValueError, match="target_spread_bps must be positive"):
            MarketMakerSimulator(symbol='SPY', target_spread_bps=0)


class TestQuoteMarket:
    """Tests for quote_market method"""

    def setup_method(self):
        """Create market maker for testing"""
        self.mm = MarketMakerSimulator(
            symbol='SPY',
            target_spread_bps=2.0,
            max_inventory=100_000
        )

    def test_quote_market_normal_conditions(self):
        """Test quote generation in normal market conditions"""
        quote = self.mm.quote_market(
            fair_value=200.0,
            hedge_status=HedgeStatus.FULL,
            volatility=0.20
        )

        assert quote is not None
        assert 'bid' in quote
        assert 'ask' in quote
        assert 'bid_size' in quote
        assert 'ask_size' in quote
        assert 'spread_bps' in quote

        # Spread should be around target (2 bps * (1 + 0.20/0.20) = 4 bps)
        expected_spread_bps = 2.0 * (1 + 0.20 / 0.20)
        assert abs(quote['spread_bps'] - expected_spread_bps) < 0.1

        # Quote should be centered around fair value
        mid = (quote['bid'] + quote['ask']) / 2
        assert abs(mid - 200.0) < 0.01

    def test_quote_market_full_hedge_low_volatility(self):
        """Test quote with full hedge and low volatility"""
        quote = self.mm.quote_market(
            fair_value=200.0,
            hedge_status=HedgeStatus.FULL,
            volatility=0.10
        )

        # Lower volatility should give tighter spread
        # 2.0 * (1 + 0.10/0.20) = 3.0 bps
        expected_spread_bps = 2.0 * (1 + 0.10 / 0.20)
        assert abs(quote['spread_bps'] - expected_spread_bps) < 0.1

    def test_quote_market_partial_hedge_widens_spread(self):
        """Test that partial hedge availability widens spreads significantly"""
        quote_full = self.mm.quote_market(200.0, HedgeStatus.FULL, 0.20)
        quote_partial = self.mm.quote_market(200.0, HedgeStatus.PARTIAL, 0.20)

        # Partial hedge should have much wider spread (10x multiplier)
        assert quote_partial['spread_bps'] > quote_full['spread_bps'] * 5

    def test_quote_market_no_hedge_low_volatility(self):
        """Test quote with no hedge but low volatility"""
        quote = self.mm.quote_market(
            fair_value=200.0,
            hedge_status=HedgeStatus.NONE,
            volatility=0.30
        )

        # Should still quote but with very wide spread (100x multiplier)
        assert quote is not None
        assert quote['spread_bps'] > 100  # Much wider than normal

    def test_quote_market_no_hedge_high_volatility_withdraws(self):
        """Test that MM withdraws quotes when no hedge + high volatility"""
        quote = self.mm.quote_market(
            fair_value=200.0,
            hedge_status=HedgeStatus.NONE,
            volatility=0.60  # Above 50% threshold
        )

        assert quote is None  # Market maker withdraws
        assert self.mm.active is False

    def test_quote_market_near_long_inventory_limit_offers_only(self):
        """Test that MM only offers when near long inventory limit"""
        # Set inventory to 95% of limit (long)
        self.mm.position.etf_inventory = int(self.mm.max_inventory * 0.95)

        quote = self.mm.quote_market(200.0, HedgeStatus.FULL, 0.20)

        assert quote is not None
        assert quote['bid'] is None  # No bid
        assert quote['ask'] is not None  # Only offer to sell
        assert quote['bid_size'] == 0
        assert quote['ask_size'] > 0
        assert quote['spread_bps'] == np.inf

    def test_quote_market_near_short_inventory_limit_bids_only(self):
        """Test that MM only bids when near short inventory limit"""
        # Set inventory to -95% of limit (short)
        self.mm.position.etf_inventory = -int(self.mm.max_inventory * 0.95)

        quote = self.mm.quote_market(200.0, HedgeStatus.FULL, 0.20)

        assert quote is not None
        assert quote['bid'] is not None  # Only bid to buy
        assert quote['ask'] is None  # No offer
        assert quote['bid_size'] > 0
        assert quote['ask_size'] == 0
        assert quote['spread_bps'] == np.inf

    def test_quote_market_at_inventory_limit_ask_size_limited(self):
        """Test that ask size is limited by inventory when at limit"""
        self.mm.position.etf_inventory = int(self.mm.max_inventory * 0.95)

        quote = self.mm.quote_market(200.0, HedgeStatus.FULL, 0.20)

        # Ask size should be <= current inventory
        assert quote['ask_size'] <= abs(self.mm.position.etf_inventory)
        assert quote['ask_size'] == min(10000, abs(self.mm.position.etf_inventory))


class TestExecuteTrade:
    """Tests for execute_trade method"""

    def setup_method(self):
        """Create market maker for testing"""
        self.mm = MarketMakerSimulator(
            symbol='SPY',
            max_inventory=100_000
        )

    def test_execute_trade_buy_order_mm_sells(self):
        """Test that MM sells when customer buys"""
        success = self.mm.execute_trade(
            size=1000,
            price=200.0,
            side='buy',
            fair_value=200.0,
            can_hedge=True
        )

        assert success is True
        # MM takes opposite side - customer buys, MM sells
        assert self.mm.position.etf_inventory == -1000
        assert self.mm.position.etf_entry_price == 200.0

    def test_execute_trade_sell_order_mm_buys(self):
        """Test that MM buys when customer sells"""
        success = self.mm.execute_trade(
            size=1000,
            price=200.0,
            side='sell',
            fair_value=200.0,
            can_hedge=True
        )

        assert success is True
        # MM takes opposite side - customer sells, MM buys
        assert self.mm.position.etf_inventory == 1000
        assert self.mm.position.etf_entry_price == 200.0

    def test_execute_trade_inventory_accumulation(self):
        """Test that multiple trades accumulate inventory correctly"""
        # First trade
        self.mm.execute_trade(1000, 200.0, 'sell', 200.0, True)
        assert self.mm.position.etf_inventory == 1000

        # Second trade - same direction
        self.mm.execute_trade(2000, 201.0, 'sell', 200.0, True)
        assert self.mm.position.etf_inventory == 3000

        # Entry price should be weighted average
        # (1000 * 200 + 2000 * 201) / 3000 = 200.666...
        expected_entry = (1000 * 200.0 + 2000 * 201.0) / 3000
        assert abs(self.mm.position.etf_entry_price - expected_entry) < 0.01

    def test_execute_trade_with_hedge(self):
        """Test that hedge is established when can_hedge=True"""
        self.mm.execute_trade(5000, 200.0, 'sell', 200.0, can_hedge=True)

        # Hedge should offset ETF inventory
        assert self.mm.position.etf_inventory == 5000
        assert self.mm.position.underlying_hedge == -5000
        assert self.mm.position.hedge_entry_price == 200.0

    def test_execute_trade_without_hedge(self):
        """Test that no hedge is created when can_hedge=False"""
        self.mm.execute_trade(5000, 200.0, 'sell', 200.0, can_hedge=False)

        # No hedge established
        assert self.mm.position.etf_inventory == 5000
        assert self.mm.position.underlying_hedge == 0
        assert self.mm.position.hedge_entry_price is None

    def test_execute_trade_reject_exceeds_inventory_limit(self):
        """Test that trades exceeding inventory limit are rejected"""
        success = self.mm.execute_trade(
            size=150_000,  # Exceeds 100k limit
            price=200.0,
            side='sell',
            fair_value=200.0,
            can_hedge=True
        )

        assert success is False
        assert self.mm.position.etf_inventory == 0  # No change

    def test_execute_trade_position_crosses_zero_long_to_short(self):
        """
        REGRESSION TEST for Critical Bug #1.
        Test that entry price is correct when position crosses zero from long to short.
        """
        # Start with long position
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, True)
        assert self.mm.position.etf_inventory == 10000
        assert self.mm.position.etf_entry_price == 100.0

        # Cross zero to short at higher price
        self.mm.execute_trade(15000, 102.0, 'buy', 102.0, True)
        assert self.mm.position.etf_inventory == -5000

        # Entry price should be 102.0 (new trade price), NOT weighted average
        assert abs(self.mm.position.etf_entry_price - 102.0) < 0.01

    def test_execute_trade_position_crosses_zero_short_to_long(self):
        """Test entry price when position crosses zero from short to long"""
        # Start with short position
        self.mm.execute_trade(10000, 100.0, 'buy', 100.0, True)
        assert self.mm.position.etf_inventory == -10000
        assert self.mm.position.etf_entry_price == 100.0

        # Cross zero to long at lower price
        self.mm.execute_trade(15000, 98.0, 'sell', 98.0, True)
        assert self.mm.position.etf_inventory == 5000

        # Entry price should be 98.0 (new trade price)
        assert abs(self.mm.position.etf_entry_price - 98.0) < 0.01

    def test_execute_trade_position_goes_to_zero(self):
        """Test that entry price and hedge reset when position goes to zero"""
        # Build position with hedge
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=True)
        assert self.mm.position.etf_inventory == 10000
        assert self.mm.position.underlying_hedge == -10000
        assert self.mm.position.hedge_entry_price == 100.0

        # Close position
        self.mm.execute_trade(10000, 105.0, 'buy', 105.0, can_hedge=True)

        # Verify complete cleanup
        assert self.mm.position.etf_inventory == 0
        assert self.mm.position.etf_entry_price == 0.0
        assert self.mm.position.underlying_hedge == 0
        assert self.mm.position.hedge_entry_price is None

    def test_execute_trade_weighted_average_entry_price(self):
        """Test weighted average entry price when adding to position"""
        # First trade: long 5000 @ 100
        self.mm.execute_trade(5000, 100.0, 'sell', 100.0, True)

        # Second trade: add 3000 @ 102
        self.mm.execute_trade(3000, 102.0, 'sell', 102.0, True)

        # Entry price: (5000 * 100 + 3000 * 102) / 8000 = 100.75
        expected_entry = (5000 * 100.0 + 3000 * 102.0) / 8000
        assert abs(self.mm.position.etf_entry_price - expected_entry) < 0.01

    def test_execute_trade_hedge_weighted_average(self):
        """
        REGRESSION TEST for Critical Bug #2.
        Test that hedge entry price uses weighted average, not replacement.
        """
        # First trade with hedge
        self.mm.execute_trade(5000, 200.0, 'sell', 200.0, can_hedge=True)
        assert self.mm.position.underlying_hedge == -5000
        assert abs(self.mm.position.hedge_entry_price - 200.0) < 0.01

        # Second trade with hedge at different fair value
        self.mm.execute_trade(3000, 202.0, 'sell', 204.0, can_hedge=True)
        assert self.mm.position.underlying_hedge == -8000

        # Hedge entry price should be weighted average
        # Hedge 1: 5000 @ 200, Hedge 2: 3000 @ 204
        # Weighted avg: (5000 * 200 + 3000 * 204) / 8000 = 201.5
        expected_hedge_entry = (5000 * 200.0 + 3000 * 204.0) / 8000
        assert abs(self.mm.position.hedge_entry_price - expected_hedge_entry) < 0.01

    def test_execute_trade_updates_position_history(self):
        """Test that position_history is updated after each trade"""
        assert len(self.mm.position_history) == 0

        self.mm.execute_trade(1000, 200.0, 'sell', 200.0, True)
        assert len(self.mm.position_history) == 1

        record = self.mm.position_history[0]
        assert record['etf_inventory'] == 1000
        assert record['hedge_position'] == -1000
        assert record['net_delta'] == 0
        assert record['fair_value'] == 200.0
        assert record['etf_price'] == 200.0

    def test_execute_trade_updates_timestamp(self):
        """Test that position timestamp is updated"""
        old_timestamp = self.mm.position.timestamp

        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.01)

        self.mm.execute_trade(1000, 200.0, 'sell', 200.0, True)
        assert self.mm.position.timestamp > old_timestamp


class TestMarkToMarket:
    """Tests for mark_to_market method"""

    def setup_method(self):
        """Create market maker for testing"""
        self.mm = MarketMakerSimulator(
            symbol='SPY',
            initial_capital=1_000_000
        )

    def test_mark_to_market_no_position(self):
        """Test P&L calculation with no position"""
        pnl = self.mm.mark_to_market(200.0)

        assert pnl['total_pnl'] == 0.0
        assert pnl['return_pct'] == 0.0
        assert pnl['capital'] == 1_000_000

    def test_mark_to_market_long_position_profit(self):
        """Test P&L calculation with long position in profit"""
        # Long 10000 @ 100
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=False)

        # Mark to market at 105
        pnl = self.mm.mark_to_market(105.0)

        # P&L: 10000 * (105 - 100) = 50000
        assert abs(pnl['total_pnl'] - 50000.0) < 0.01
        assert abs(pnl['return_pct'] - 5.0) < 0.01  # 50k / 1M = 5%
        assert abs(pnl['capital'] - 1_050_000) < 0.01

    def test_mark_to_market_long_position_loss(self):
        """Test P&L calculation with long position in loss"""
        # Long 10000 @ 100
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=False)

        # Mark to market at 95
        pnl = self.mm.mark_to_market(95.0)

        # P&L: 10000 * (95 - 100) = -50000
        assert abs(pnl['total_pnl'] - (-50000.0)) < 0.01
        assert abs(pnl['return_pct'] - (-5.0)) < 0.01
        assert abs(pnl['capital'] - 950_000) < 0.01

    def test_mark_to_market_hedged_position(self):
        """Test P&L calculation with hedged position"""
        # Long 10000 @ 100, hedged at 100
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=True)

        # Mark to market at 105, fair value also 105
        self.mm.position.fair_value = 105.0
        pnl = self.mm.mark_to_market(105.0)

        # ETF P&L: 10000 * (105 - 100) = 50000
        # Hedge P&L: -10000 * (105 - 100) = -50000
        # Net: 0 (perfectly hedged)
        assert abs(pnl['total_pnl']) < 0.01

    def test_mark_to_market_updates_pnl_history(self):
        """Test that pnl_history is updated"""
        assert len(self.mm.pnl_history) == 0

        self.mm.mark_to_market(200.0)
        assert len(self.mm.pnl_history) == 1

        self.mm.mark_to_market(201.0)
        assert len(self.mm.pnl_history) == 2

    def test_mark_to_market_pnl_history_structure(self):
        """Test structure of pnl_history entries"""
        self.mm.execute_trade(1000, 100.0, 'sell', 100.0, False)
        pnl = self.mm.mark_to_market(105.0)

        assert 'timestamp' in pnl
        assert 'etf_pnl' in pnl
        assert 'hedge_pnl' in pnl
        assert 'total_pnl' in pnl
        assert 'return_pct' in pnl
        assert 'capital' in pnl

        assert pnl == self.mm.pnl_history[-1]


class TestRiskMetrics:
    """Tests for calculate_risk_metrics method"""

    def setup_method(self):
        """Create market maker for testing"""
        self.mm = MarketMakerSimulator(
            symbol='SPY',
            initial_capital=1_000_000,
            max_inventory=100_000
        )

    def test_risk_metrics_empty_history(self):
        """Test that empty history returns empty dict"""
        metrics = self.mm.calculate_risk_metrics()
        assert metrics == {}

    def test_risk_metrics_with_history(self):
        """Test risk metrics calculation with P&L history"""
        # Execute some trades and mark to market
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=False)

        for price in [101, 102, 99, 98, 103, 97]:
            self.mm.mark_to_market(float(price))

        metrics = self.mm.calculate_risk_metrics()

        assert 'current_delta' in metrics
        assert 'gamma_risk' in metrics
        assert 'inventory_pct' in metrics
        assert 'var_95' in metrics
        assert 'expected_shortfall' in metrics
        assert 'max_drawdown' in metrics
        assert 'sharpe_ratio' in metrics

    def test_risk_metrics_current_delta(self):
        """Test current delta in risk metrics"""
        # Long 5000, hedged 5000
        self.mm.execute_trade(5000, 100.0, 'sell', 100.0, can_hedge=True)
        self.mm.mark_to_market(100.0)

        metrics = self.mm.calculate_risk_metrics()
        assert metrics['current_delta'] == 0  # Fully hedged

    def test_risk_metrics_inventory_pct(self):
        """Test inventory percentage calculation"""
        # 50k inventory out of 100k limit = 50%
        self.mm.execute_trade(50000, 100.0, 'sell', 100.0, can_hedge=False)
        self.mm.mark_to_market(100.0)

        metrics = self.mm.calculate_risk_metrics()
        assert abs(metrics['inventory_pct'] - 50.0) < 0.01

    def test_risk_metrics_var_calculation(self):
        """Test Value at Risk calculation"""
        # Create varying P&L
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=False)

        prices = [100, 102, 104, 98, 96, 103, 97, 101, 99, 105]
        for price in prices:
            self.mm.mark_to_market(float(price))

        metrics = self.mm.calculate_risk_metrics()

        # VaR should be negative (represents a loss)
        assert 'var_95' in metrics
        assert metrics['var_95'] < 0  # Should be a loss value

    def test_risk_metrics_expected_shortfall(self):
        """
        REGRESSION TEST for Critical Bug #3.
        Test Expected Shortfall calculation doesn't return NaN.
        """
        # Create small P&L history
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=False)

        for price in [100, 101, 102]:  # Small dataset
            self.mm.mark_to_market(float(price))

        metrics = self.mm.calculate_risk_metrics()

        # Should not be NaN
        assert not np.isnan(metrics['expected_shortfall'])

    def test_risk_metrics_max_drawdown(self):
        """Test maximum drawdown calculation"""
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=False)

        # Create pattern: profit, then big loss
        for price in [105, 110, 115, 95, 90]:  # Peak at 115, trough at 90
            self.mm.mark_to_market(float(price))

        metrics = self.mm.calculate_risk_metrics()

        # Max drawdown should be negative
        assert metrics['max_drawdown'] < 0

    def test_risk_metrics_sharpe_ratio(self):
        """Test Sharpe ratio calculation"""
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=False)

        for price in [101, 102, 103, 104, 105]:
            self.mm.mark_to_market(float(price))

        metrics = self.mm.calculate_risk_metrics()

        # Positive trend should have positive Sharpe
        assert 'sharpe_ratio' in metrics

    def test_risk_metrics_sharpe_zero_std(self):
        """Test Sharpe ratio when std is zero (constant P&L)"""
        self.mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=False)

        # Mark to same price multiple times
        for _ in range(5):
            self.mm.mark_to_market(100.0)

        metrics = self.mm.calculate_risk_metrics()

        # Should return 0, not inf or NaN
        assert metrics['sharpe_ratio'] == 0


class TestSimulateMarketMakerCrisis:
    """Tests for simulate_market_maker_crisis function"""

    def setup_method(self):
        """Create crisis scenario for testing"""
        self.timeline = pd.date_range('2015-08-24 09:30', periods=10, freq='1min')
        self.scenario = {
            'timeline': self.timeline,
            'etf_prices': [200, 199, 198, 195, 190, 185, 188, 192, 196, 198],
            'hedge_availability': [True, True, True, False, False, False, True, True, True, True],
            'volatility': [0.20, 0.25, 0.30, 0.50, 0.70, 0.80, 0.60, 0.40, 0.30, 0.25],
            'order_flow': [-1000, -2000, -3000, -5000, -8000, -5000, 2000, 3000, 2000, 1000]
        }

    def test_simulate_crisis_basic(self):
        """Test basic crisis simulation execution"""
        mm, results = simulate_market_maker_crisis(200.0, self.scenario)

        assert isinstance(mm, MarketMakerSimulator)
        assert isinstance(results, pd.DataFrame)
        assert len(results) == len(self.timeline)

    def test_simulate_crisis_results_structure(self):
        """Test structure of results DataFrame"""
        _, results = simulate_market_maker_crisis(200.0, self.scenario)

        expected_columns = [
            'timestamp', 'etf_price', 'fair_value', 'discount_pct',
            'spread_bps', 'mm_active', 'inventory', 'pnl', 'cumulative_return_pct'
        ]

        for col in expected_columns:
            assert col in results.columns

    def test_simulate_crisis_hedge_loss(self):
        """Test that crisis with hedge loss causes inventory buildup"""
        mm, results = simulate_market_maker_crisis(200.0, self.scenario)

        # During hedge loss period (idx 3-5), inventory should build up
        # due to incoming sell flow that can't be hedged
        inventory_at_peak = results['inventory'].iloc[5]

        # Should have accumulated inventory (negative from buying sell flow)
        assert inventory_at_peak != 0

    def test_simulate_crisis_mm_withdrawal(self):
        """Test that MM withdraws during extreme conditions"""
        # Create scenario with very high volatility and no hedge
        extreme_scenario = self.scenario.copy()
        extreme_scenario['volatility'] = [0.80] * 10
        extreme_scenario['hedge_availability'] = [False] * 10

        mm, results = simulate_market_maker_crisis(200.0, extreme_scenario)

        # MM should become inactive at some point
        assert not results['mm_active'].all()

    def test_simulate_crisis_with_custom_params(self):
        """Test simulation with custom market maker parameters"""
        mm_params = {
            'initial_capital': 5_000_000,
            'max_inventory': 50_000,
            'target_spread_bps': 5.0
        }

        mm, results = simulate_market_maker_crisis(
            200.0,
            self.scenario,
            mm_params=mm_params
        )

        assert mm.initial_capital == 5_000_000
        assert mm.max_inventory == 50_000
        assert mm.target_spread_bps == 5.0

    def test_simulate_crisis_spread_widening(self):
        """Test that spreads widen during crisis"""
        _, results = simulate_market_maker_crisis(200.0, self.scenario)

        # Spread at start (normal conditions)
        spread_start = results['spread_bps'].iloc[0]

        # Spread during crisis (high vol, no hedge)
        spread_crisis = results['spread_bps'].iloc[4]

        # Crisis spread should be wider
        assert spread_crisis > spread_start

    def test_simulate_crisis_discount_calculation(self):
        """Test that discount percentage is calculated correctly"""
        _, results = simulate_market_maker_crisis(200.0, self.scenario)

        # At idx 0: etf_price=200, fair_value=200
        # discount = (200/200 - 1) * 100 = 0%
        assert abs(results['discount_pct'].iloc[0] - 0.0) < 0.01

        # At idx 4: etf_price=190, fair_value=200
        # discount = (190/200 - 1) * 100 = -5%
        assert abs(results['discount_pct'].iloc[4] - (-5.0)) < 0.01

    def test_simulate_crisis_pnl_tracking(self):
        """Test that P&L is tracked throughout simulation"""
        _, results = simulate_market_maker_crisis(200.0, self.scenario)

        # P&L should vary throughout
        assert 'pnl' in results.columns
        assert 'cumulative_return_pct' in results.columns

        # Should have P&L history
        assert len(results) == len(self.timeline)

    def test_simulate_crisis_recovery_phase(self):
        """Test MM behavior during recovery phase"""
        mm, results = simulate_market_maker_crisis(200.0, self.scenario)

        # During recovery (idx 6-9), hedge becomes available and vol drops
        # Spreads should tighten
        spread_crisis = results['spread_bps'].iloc[5]
        spread_recovery = results['spread_bps'].iloc[8]

        # Recovery spread should be tighter (unless MM withdrew)
        if results['mm_active'].iloc[8]:
            assert spread_recovery < spread_crisis


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def test_large_position_partial_liquidation(self):
        """Test partial liquidation of large position"""
        mm = MarketMakerSimulator(symbol='SPY', max_inventory=100_000)

        # Build large position
        mm.execute_trade(80000, 100.0, 'sell', 100.0, can_hedge=False)
        assert mm.position.etf_inventory == 80000

        # Partial liquidation
        mm.execute_trade(50000, 105.0, 'buy', 105.0, can_hedge=False)
        assert mm.position.etf_inventory == 30000

        # Entry price should still be original
        assert abs(mm.position.etf_entry_price - 100.0) < 0.01

    def test_alternating_buy_sell_flow(self):
        """Test handling of alternating buy/sell flow"""
        mm = MarketMakerSimulator(symbol='SPY')

        for i in range(10):
            side = 'sell' if i % 2 == 0 else 'buy'
            mm.execute_trade(1000, 200.0, side, 200.0, can_hedge=True)

        # Should end near zero inventory (alternating)
        assert abs(mm.position.etf_inventory) < 2000

    def test_extreme_price_movement(self):
        """Test P&L calculation with extreme price movements"""
        mm = MarketMakerSimulator(symbol='SPY', initial_capital=10_000_000)

        # Long 10000 @ 100
        mm.execute_trade(10000, 100.0, 'sell', 100.0, can_hedge=False)

        # Price crashes 50%
        pnl = mm.mark_to_market(50.0)

        # P&L: 10000 * (50 - 100) = -500000
        assert abs(pnl['total_pnl'] - (-500_000)) < 0.01

    def test_zero_volatility_quote(self):
        """Test quote generation with zero volatility"""
        mm = MarketMakerSimulator(symbol='SPY', target_spread_bps=2.0)

        quote = mm.quote_market(
            fair_value=200.0,
            hedge_status=HedgeStatus.FULL,
            volatility=0.0
        )

        # Should still generate valid quote
        assert quote is not None
        assert quote['spread_bps'] > 0

    def test_fractional_shares_rounding(self):
        """Test that inventory handles integer shares correctly"""
        mm = MarketMakerSimulator(symbol='SPY')

        # All trades should maintain integer inventory
        mm.execute_trade(1500, 100.0, 'sell', 100.0, True)
        assert isinstance(mm.position.etf_inventory, int)
        assert mm.position.etf_inventory == 1500
