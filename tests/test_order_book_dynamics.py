"""
Comprehensive tests for order_book_dynamics module.

Tests cover:
- OrderBookSnapshot functionality
- FlashCrashOrderBook simulation
- Market maker withdrawal scenarios
- Stop-loss cascades
- Kyle's lambda calculation
- Amihud illiquidity measure
- Liquidity gap identification
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime

from src.order_book_dynamics import (
    OrderBookSnapshot,
    FlashCrashOrderBook,
    calculate_kyle_lambda,
    calculate_amihud_illiquidity,
    identify_liquidity_gaps
)


class TestOrderBookSnapshot:
    """Tests for OrderBookSnapshot dataclass and its methods"""

    def setup_method(self):
        """Create sample order book snapshot for testing"""
        self.snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={99.5: 1000, 99.0: 2000, 98.5: 3000},
            asks={100.5: 1500, 101.0: 2500, 101.5: 3500},
            last_trade=100.0,
            fair_value=100.0,
            halt_status=False
        )

    def test_spread_bps_normal(self):
        """Test spread calculation in normal conditions"""
        spread = self.snapshot.spread_bps()
        # Best bid: 99.5, best ask: 100.5, mid: 100.0
        # Spread: (100.5 - 99.5) / 100.0 * 10000 = 100 bps
        assert abs(spread - 100.0) < 0.01

    def test_spread_bps_empty_bids(self):
        """Test spread with no bids"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={},
            asks={100.5: 1000},
            last_trade=None,
            fair_value=100.0,
            halt_status=False
        )
        assert snapshot.spread_bps() == np.inf

    def test_spread_bps_empty_asks(self):
        """Test spread with no asks"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={99.5: 1000},
            asks={},
            last_trade=None,
            fair_value=100.0,
            halt_status=False
        )
        assert snapshot.spread_bps() == np.inf

    def test_spread_bps_zero_mid_price(self):
        """Test spread calculation when mid price is zero (extreme crash)"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={0.0: 1000},
            asks={0.0: 1000},
            last_trade=None,
            fair_value=100.0,
            halt_status=False
        )
        assert snapshot.spread_bps() == np.inf

    def test_spread_bps_negative_prices(self):
        """Test spread calculation with negative prices (should return inf)"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={-1.0: 1000},
            asks={1.0: 1000},
            last_trade=None,
            fair_value=100.0,
            halt_status=False
        )
        # Mid is 0, should return inf
        assert snapshot.spread_bps() == np.inf

    def test_depth_at_distance_normal(self):
        """Test depth calculation within 1% of mid"""
        bid_depth, ask_depth = self.snapshot.depth_at_distance(0.01)
        # Mid = 100.0, threshold = 1.0
        # Bids within 99.0-100.0: 99.5 (1000) + 99.0 (2000) = 3000
        # Asks within 100.0-101.0: 100.5 (1500) + 101.0 (2500) = 4000
        assert bid_depth == 3000
        assert ask_depth == 4000

    def test_depth_at_distance_empty_book(self):
        """Test depth with empty order book"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={},
            asks={},
            last_trade=None,
            fair_value=100.0,
            halt_status=False
        )
        bid_depth, ask_depth = snapshot.depth_at_distance(0.01)
        assert bid_depth == 0
        assert ask_depth == 0

    def test_price_impact_buy_full_fill(self):
        """Test price impact for buy order that can be fully filled"""
        # Buy 1500 shares: 1500 @ 100.5 = 150,750 / 1500 = 100.5
        avg_price = self.snapshot.price_impact(1500, 'buy')
        assert abs(avg_price - 100.5) < 0.01

    def test_price_impact_buy_multiple_levels(self):
        """Test price impact for buy order hitting multiple levels"""
        # Buy 4000 shares: 1500 @ 100.5, 2500 @ 101.0
        # Total cost: 150,750 + 252,500 = 403,250 / 4000 = 100.8125
        avg_price = self.snapshot.price_impact(4000, 'buy')
        assert abs(avg_price - 100.8125) < 0.01

    def test_price_impact_sell_full_fill(self):
        """Test price impact for sell order"""
        # Sell 1000 shares @ 99.5
        avg_price = self.snapshot.price_impact(1000, 'sell')
        assert abs(avg_price - 99.5) < 0.01

    def test_price_impact_insufficient_liquidity(self):
        """Test price impact when order size exceeds available liquidity"""
        # Try to buy 10000 shares (only 7500 available)
        avg_price = self.snapshot.price_impact(10000, 'buy')
        assert np.isnan(avg_price)


class TestFlashCrashOrderBook:
    """Tests for FlashCrashOrderBook simulation"""

    def setup_method(self):
        """Create order book for testing"""
        self.book = FlashCrashOrderBook(symbol='SPY', fair_value=200.0, normal_spread_bps=2.0)

    def test_initialization(self):
        """Test order book initializes correctly"""
        assert self.book.symbol == 'SPY'
        assert self.book.fair_value == 200.0
        assert self.book.normal_spread_bps == 2.0
        assert self.book.original_spread_bps == 2.0  # Check original is stored
        assert not self.book.halt_status
        assert self.book.market_maker_active
        assert len(self.book.bids) > 0
        assert len(self.book.asks) > 0

    def test_initial_order_book_structure(self):
        """Test that initial order book has realistic structure"""
        # Check that best bid is below fair value
        best_bid = max(self.book.bids.keys())
        assert best_bid < self.book.fair_value

        # Check that best ask is above fair value
        best_ask = min(self.book.asks.keys())
        assert best_ask > self.book.fair_value

        # Check that spread is reasonable
        spread = best_ask - best_bid
        expected_spread = self.book.fair_value * (self.book.normal_spread_bps / 10000)
        assert abs(spread - expected_spread) < 0.01

    def test_market_maker_withdrawal_moderate_stress(self):
        """Test market maker behavior under moderate stress"""
        original_spread = self.book.normal_spread_bps
        self.book.simulate_market_maker_withdrawal(0.2)

        # Spread should widen but not dramatically
        assert self.book.normal_spread_bps > original_spread
        assert self.book.market_maker_active

    def test_market_maker_withdrawal_high_stress(self):
        """Test market maker behavior under high stress"""
        self.book.simulate_market_maker_withdrawal(0.5)

        # Spreads should be very wide, liquidity reduced
        assert len(self.book.bids) < 50  # Many quotes removed
        assert len(self.book.asks) < 50
        assert self.book.market_maker_active  # Still active but scared

    def test_market_maker_withdrawal_panic(self):
        """Test market maker complete withdrawal during panic"""
        self.book.simulate_market_maker_withdrawal(0.9)

        # Market maker should withdraw completely
        assert not self.book.market_maker_active

        # Only stale quotes far from fair value should remain
        if self.book.bids:
            best_bid = max(self.book.bids.keys())
            assert best_bid < self.book.fair_value * 0.90
        if self.book.asks:
            best_ask = min(self.book.asks.keys())
            assert best_ask > self.book.fair_value * 1.10

    def test_spread_accumulation_bug_fixed(self):
        """Test that spread doesn't accumulate with multiple calls"""
        original_spread = self.book.original_spread_bps

        # Call withdrawal multiple times
        self.book.simulate_market_maker_withdrawal(0.1)
        spread_after_first = self.book.normal_spread_bps

        self.book.simulate_market_maker_withdrawal(0.1)
        spread_after_second = self.book.normal_spread_bps

        # Spreads should be the same (based on original, not accumulated)
        assert abs(spread_after_first - spread_after_second) < 0.01

    def test_execute_market_order_full_fill(self):
        """Test market order that fills completely"""
        initial_ask_size = sum(self.book.asks.values())
        executions = self.book.execute_market_order(1000, 'buy')

        # Should have at least one execution
        assert len(executions) > 0

        # Total filled should be 1000
        total_filled = sum(e['size'] for e in executions)
        assert total_filled == 1000

        # No unfilled status
        assert all(e.get('status') != 'UNFILLED' for e in executions)

    def test_execute_market_order_partial_fill(self):
        """Test market order that partially fills"""
        # Try to buy more than available
        total_available = sum(self.book.asks.values())
        executions = self.book.execute_market_order(total_available + 10000, 'buy')

        # Should have PARTIALLY_FILLED status
        partial_fill = [e for e in executions if e.get('status') == 'PARTIALLY_FILLED']
        assert len(partial_fill) == 1
        assert partial_fill[0]['filled_size'] == total_available

    def test_execute_market_order_updates_book(self):
        """Test that market order actually removes liquidity from book"""
        initial_ask_count = len(self.book.asks)
        initial_best_ask = min(self.book.asks.keys())

        # Buy all shares at best ask
        best_ask_size = self.book.asks[initial_best_ask]
        executions = self.book.execute_market_order(best_ask_size, 'buy')

        # Best ask should be removed
        assert len(self.book.asks) == initial_ask_count - 1
        assert initial_best_ask not in self.book.asks

    def test_luld_breach_detection(self):
        """Test that LULD breaches are detected and halt trading"""
        # Create order book with very thin liquidity
        thin_book = FlashCrashOrderBook(symbol='TEST', fair_value=100.0)
        thin_book.asks = {90.0: 1000}  # Price 10% below fair value

        executions = thin_book.execute_market_order(1000, 'buy')

        # Should trigger halt
        assert thin_book.halt_status

    def test_stop_loss_cascade_sequential(self):
        """Test sequential stop-loss cascade"""
        # First drive price down with initial sell to create stressed market
        self.book.execute_market_order(30000, 'sell')  # Price drops to ~199.54

        # Set stop orders ABOVE current market - they trigger because market is already below
        # Sequential cascade: each stop execution drives price lower, accelerating the crash
        stop_orders = {
            199.6: 3000,    # Triggers immediately (market at 199.54)
            199.5: 5000,    # Triggers from first stop execution
            199.4: 7000     # Triggers from second stop execution
        }

        results_df = self.book.simulate_stop_loss_cascade(stop_orders, 'sequential')

        # Should have results for orders that triggered
        assert len(results_df) > 0

        # Check slippage is calculated
        assert 'slippage_pct' in results_df.columns

        # Verify at least some slippages are calculated (not all NaN)
        assert not results_df['slippage_pct'].isna().all(), "All slippages are NaN"

        # Slippage should be negative (selling below trigger)
        valid_slippages = results_df['slippage_pct'].dropna()
        if len(valid_slippages) > 0:
            assert (valid_slippages <= 0).all(), "Some slippages are positive"

    def test_stop_loss_cascade_avalanche(self):
        """Test avalanche stop-loss cascade"""
        stop_orders = {
            199.0: 5000,
            198.0: 10000,
            197.0: 15000
        }

        results_df = self.book.simulate_stop_loss_cascade(stop_orders, 'avalanche')

        # Should have results
        assert len(results_df) > 0

        # All orders hit at once
        total_size = sum(results_df['size'])
        assert total_size == sum(stop_orders.values())

    def test_stop_loss_cascade_empty_book(self):
        """Test stop-loss cascade with empty order book"""
        empty_book = FlashCrashOrderBook(symbol='TEST', fair_value=100.0)
        empty_book.bids = {}  # Remove all bids

        stop_orders = {99.0: 1000}
        results_df = empty_book.simulate_stop_loss_cascade(stop_orders, 'sequential')

        # Should handle gracefully (no crash)
        assert isinstance(results_df, pd.DataFrame)

    def test_take_snapshot(self):
        """Test taking order book snapshot"""
        snapshot = self.book.take_snapshot()

        assert isinstance(snapshot, OrderBookSnapshot)
        assert snapshot.fair_value == self.book.fair_value
        assert snapshot.halt_status == self.book.halt_status
        assert len(snapshot.bids) > 0
        assert len(snapshot.asks) > 0

        # Snapshot should be in history
        assert len(self.book.snapshot_history) == 1


class TestKyleLambda:
    """Tests for Kyle's lambda calculation"""

    def test_kyle_lambda_normal_conditions(self):
        """Test Kyle's lambda with normal market data"""
        trades = pd.DataFrame({
            'price': [100.0, 100.1, 100.2, 99.9, 100.0, 100.1, 100.3, 100.2, 100.1, 100.0, 100.2, 100.3],
            'size': [1000, 1500, 2000, 1200, 1100, 1300, 1800, 1400, 1600, 1700, 1900, 2100],
            'side': ['buy', 'buy', 'buy', 'sell', 'buy', 'buy', 'sell', 'buy', 'sell', 'buy', 'buy', 'sell']
        })

        lambda_val = calculate_kyle_lambda(trades, [])

        # Should return a numeric value
        assert isinstance(lambda_val, (int, float))
        assert not np.isnan(lambda_val)

    def test_kyle_lambda_insufficient_data(self):
        """Test Kyle's lambda with too few trades"""
        trades = pd.DataFrame({
            'price': [100.0, 100.1],
            'size': [1000, 1500],
            'side': ['buy', 'buy']
        })

        lambda_val = calculate_kyle_lambda(trades, [])

        # Should return NaN
        assert np.isnan(lambda_val)

    def test_kyle_lambda_missing_columns(self):
        """Test Kyle's lambda with missing required columns"""
        trades = pd.DataFrame({
            'price': [100.0, 100.1, 100.2],
            # Missing 'size' and 'side'
        })

        with pytest.raises(ValueError, match="must contain columns"):
            calculate_kyle_lambda(trades, [])

    def test_kyle_lambda_doesnt_mutate_input(self):
        """Test that Kyle's lambda doesn't mutate input DataFrame"""
        trades = pd.DataFrame({
            'price': [100.0, 100.1, 100.2, 99.9, 100.0, 100.1, 100.3, 100.2, 100.1, 100.0, 100.2, 100.3],
            'size': [1000, 1500, 2000, 1200, 1100, 1300, 1800, 1400, 1600, 1700, 1900, 2100],
            'side': ['buy', 'buy', 'buy', 'sell', 'buy', 'buy', 'sell', 'buy', 'sell', 'buy', 'buy', 'sell']
        })

        original_columns = set(trades.columns)
        calculate_kyle_lambda(trades, [])
        final_columns = set(trades.columns)

        # Columns should not change
        assert original_columns == final_columns


class TestAmihudIlliquidity:
    """Tests for Amihud illiquidity measure"""

    def test_amihud_normal_conditions(self):
        """Test Amihud measure with normal data"""
        prices = pd.Series([100.0, 100.5, 99.8, 100.2, 100.7])
        volumes = pd.Series([10000, 12000, 11000, 10500, 13000])

        illiq = calculate_amihud_illiquidity(prices, volumes)

        # Should be positive and small for liquid market
        assert illiq > 0
        assert illiq < 0.001  # Liquid market

    def test_amihud_zero_volume(self):
        """Test Amihud with zero volumes"""
        prices = pd.Series([100.0, 100.5, 99.8])
        volumes = pd.Series([0, 0, 0])

        illiq = calculate_amihud_illiquidity(prices, volumes)

        # Should return NaN when no volume
        assert np.isnan(illiq)

    def test_amihud_some_zero_volumes(self):
        """Test Amihud with some zero volumes mixed in"""
        prices = pd.Series([100.0, 100.5, 99.8, 100.2, 100.7])
        volumes = pd.Series([10000, 0, 11000, 0, 13000])

        illiq = calculate_amihud_illiquidity(prices, volumes)

        # Should handle and return value based on non-zero volumes
        assert not np.isnan(illiq)
        assert illiq > 0

    def test_amihud_high_volatility_low_volume(self):
        """Test Amihud with high price volatility and low volume (illiquid)"""
        # Use truly low volume to create illiquid market
        prices = pd.Series([100.0, 95.0, 105.0, 90.0, 110.0])
        volumes = pd.Series([1, 2, 1, 2, 1])  # Very low volume

        illiq = calculate_amihud_illiquidity(prices, volumes)

        # Should be high for illiquid market (adjusted realistic threshold)
        assert illiq > 0.001  # Illiquid market


class TestLiquidityGaps:
    """Tests for liquidity gap identification"""

    def test_identify_gaps_normal_book(self):
        """Test gap identification in normal order book"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={100.0: 1000, 98.0: 2000, 96.0: 3000},  # 2% gaps
            asks={101.0: 1000, 103.0: 2000, 105.0: 3000},
            last_trade=100.0,
            fair_value=100.0,
            halt_status=False
        )

        gaps = identify_liquidity_gaps(snapshot, threshold_pct=1.5)

        # Should find two gaps: 100->98 and 98->96
        assert len(gaps) == 2

    def test_identify_gaps_tight_book(self):
        """Test gap identification in tight order book (no gaps)"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={100.0: 1000, 99.95: 2000, 99.90: 3000},  # < 1% gaps
            asks={100.05: 1000, 100.10: 2000, 100.15: 3000},
            last_trade=100.0,
            fair_value=100.0,
            halt_status=False
        )

        gaps = identify_liquidity_gaps(snapshot, threshold_pct=1.0)

        # Should find no gaps
        assert len(gaps) == 0

    def test_identify_gaps_empty_book(self):
        """Test gap identification with empty order book"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={},
            asks={},
            last_trade=None,
            fair_value=100.0,
            halt_status=False
        )

        gaps = identify_liquidity_gaps(snapshot, threshold_pct=2.0)

        # Should return empty list
        assert len(gaps) == 0

    def test_identify_gaps_large_threshold(self):
        """Test gap identification with very large threshold"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={100.0: 1000, 50.0: 2000},  # 50% gap!
            asks={101.0: 1000},
            last_trade=100.0,
            fair_value=100.0,
            halt_status=False
        )

        gaps = identify_liquidity_gaps(snapshot, threshold_pct=10.0)

        # Should find the large gap
        assert len(gaps) >= 1
        # Gap should be from 50.0 to 100.0
        assert (50.0, 100.0) in gaps


class TestEdgeCases:
    """Tests for edge cases and error conditions"""

    def test_order_book_with_single_price_level(self):
        """Test order book with only one price level"""
        book = FlashCrashOrderBook(symbol='TEST', fair_value=100.0)
        book.bids = {99.0: 1000}
        book.asks = {101.0: 1000}

        snapshot = book.take_snapshot()
        spread = snapshot.spread_bps()

        # Should calculate spread correctly
        assert spread > 0

    def test_execute_order_with_zero_size(self):
        """Test executing order with zero size"""
        book = FlashCrashOrderBook(symbol='TEST', fair_value=100.0)
        executions = book.execute_market_order(0, 'buy')

        # Should return empty list or handle gracefully
        total_filled = sum(e.get('size', 0) for e in executions)
        assert total_filled == 0

    def test_snapshot_after_halt(self):
        """Test taking snapshot after trading is halted"""
        book = FlashCrashOrderBook(symbol='TEST', fair_value=100.0)
        book.halt_status = True

        snapshot = book.take_snapshot()

        # Snapshot should reflect halt status
        assert snapshot.halt_status

    def test_multiple_withdrawals_same_level(self):
        """Test multiple market maker withdrawals at same stress level"""
        book = FlashCrashOrderBook(symbol='TEST', fair_value=100.0)

        # Withdraw twice at same level
        book.simulate_market_maker_withdrawal(0.5)
        spread_after_first = book.normal_spread_bps

        book.simulate_market_maker_withdrawal(0.5)
        spread_after_second = book.normal_spread_bps

        # Should produce same spread (not accumulate)
        assert abs(spread_after_first - spread_after_second) < 0.01


class TestInputValidation:
    """Tests for input validation and error handling"""

    def test_kyle_lambda_missing_price_column(self):
        """Test Kyle's lambda with missing 'price' column"""
        trades = pd.DataFrame({
            'size': [1000, 1500],
            'side': ['buy', 'sell']
        })

        with pytest.raises(ValueError, match="must contain columns"):
            calculate_kyle_lambda(trades, [])

    def test_kyle_lambda_missing_size_column(self):
        """Test Kyle's lambda with missing 'size' column"""
        trades = pd.DataFrame({
            'price': [100.0, 100.1],
            'side': ['buy', 'sell']
        })

        with pytest.raises(ValueError, match="must contain columns"):
            calculate_kyle_lambda(trades, [])

    def test_kyle_lambda_missing_side_column(self):
        """Test Kyle's lambda with missing 'side' column"""
        trades = pd.DataFrame({
            'price': [100.0, 100.1],
            'size': [1000, 1500]
        })

        with pytest.raises(ValueError, match="must contain columns"):
            calculate_kyle_lambda(trades, [])

    def test_depth_at_distance_negative_percentage(self):
        """Test depth_at_distance with negative percentage"""
        snapshot = OrderBookSnapshot(
            timestamp=pd.Timestamp.now(),
            bids={99.5: 1000},
            asks={100.5: 1000},
            last_trade=None,
            fair_value=100.0,
            halt_status=False
        )

        # Should handle gracefully (negative distance might be edge case)
        bid_depth, ask_depth = snapshot.depth_at_distance(-0.01)
        # Negative distance could return 0 or handle specially
        assert bid_depth >= 0
        assert ask_depth >= 0

    def test_snapshot_history_accumulates_correctly(self):
        """Test that snapshots accumulate in history without duplication"""
        book = FlashCrashOrderBook(symbol='TEST', fair_value=100.0)
        assert len(book.snapshot_history) == 0

        snapshot1 = book.take_snapshot()
        assert len(book.snapshot_history) == 1
        assert book.snapshot_history[0] is snapshot1

        snapshot2 = book.take_snapshot()
        assert len(book.snapshot_history) == 2
        assert book.snapshot_history[1] is snapshot2

    def test_trade_history_accumulates_correctly(self):
        """Test that trades accumulate in history"""
        book = FlashCrashOrderBook(symbol='TEST', fair_value=100.0)
        assert len(book.trade_history) == 0

        book.execute_market_order(1000, 'buy')
        trade_count_1 = len(book.trade_history)
        assert trade_count_1 > 0

        book.execute_market_order(2000, 'sell')
        trade_count_2 = len(book.trade_history)
        assert trade_count_2 > trade_count_1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
