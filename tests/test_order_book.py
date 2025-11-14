"""
Tests for Order Book Module

Educational tests demonstrating order book mechanics and air pockets.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from order_book import OrderBook, Order, simulate_stop_loss_cascade


class TestOrderBookBasics:
    """Test basic order book operations"""

    def test_create_empty_order_book(self):
        """Create an empty order book"""
        book = OrderBook()
        assert len(book.bids) == 0
        assert len(book.asks) == 0

    def test_add_bid(self):
        """Add a bid to the order book"""
        book = OrderBook()
        book.add_bid(100.0, 500)

        assert len(book.bids) == 1
        assert book.bids[0].price == 100.0
        assert book.bids[0].size == 500

    def test_add_ask(self):
        """Add an ask to the order book"""
        book = OrderBook()
        book.add_ask(101.0, 500)

        assert len(book.asks) == 1
        assert book.asks[0].price == 101.0
        assert book.asks[0].size == 500

    def test_bids_sorted_descending(self):
        """Bids should be sorted highest first"""
        book = OrderBook()
        book.add_bid(100.0, 100)
        book.add_bid(101.0, 200)
        book.add_bid(99.0, 300)

        assert book.bids[0].price == 101.0
        assert book.bids[1].price == 100.0
        assert book.bids[2].price == 99.0

    def test_asks_sorted_ascending(self):
        """Asks should be sorted lowest first"""
        book = OrderBook()
        book.add_ask(102.0, 100)
        book.add_ask(101.0, 200)
        book.add_ask(103.0, 300)

        assert book.asks[0].price == 101.0
        assert book.asks[1].price == 102.0
        assert book.asks[2].price == 103.0


class TestSpreadCalculations:
    """Test bid-ask spread calculations"""

    def test_get_spread_normal(self):
        """Calculate spread in normal conditions"""
        book = OrderBook()
        book.add_bid(100.0, 500)
        book.add_ask(100.10, 500)

        spread = book.get_spread()
        assert spread == 0.10

    def test_get_spread_bps(self):
        """Calculate spread in basis points"""
        book = OrderBook()
        book.add_bid(100.0, 500)
        book.add_ask(101.0, 500)

        spread_bps = book.get_spread_bps()
        # 1 dollar spread / 100 mid = 1% = 100 bps
        assert abs(spread_bps - 100) < 1  # Allow floating point error

    def test_get_spread_empty_book(self):
        """Spread should be None for empty book"""
        book = OrderBook()
        assert book.get_spread() is None
        assert book.get_spread_bps() is None


class TestMarketOrders:
    """Test market order execution"""

    def test_execute_market_buy_single_level(self):
        """Market buy consuming single ask level"""
        book = OrderBook()
        book.add_ask(101.0, 500)
        book.add_ask(102.0, 300)

        fills = book.execute_market_buy(400)

        assert len(fills) == 2
        # First 500 shares at 101, then 0 at 102 (only took 400 total)
        # Wait, actually it should take all 500 from first level? No, only 400
        assert fills[0] == (101.0, 400)
        assert len(book.asks) == 1  # Second level remains
        assert book.asks[0].price == 102.0

    def test_execute_market_sell_single_level(self):
        """Market sell consuming single bid level"""
        book = OrderBook()
        book.add_bid(100.0, 500)
        book.add_bid(99.0, 300)

        fills = book.execute_market_sell(400)

        assert len(fills) == 1
        assert fills[0] == (100.0, 400)
        assert len(book.bids) == 2
        assert book.bids[0].size == 100  # 500 - 400 remaining

    def test_execute_market_buy_multiple_levels(self):
        """Market buy consuming multiple ask levels"""
        book = OrderBook()
        book.add_ask(101.0, 300)
        book.add_ask(102.0, 300)
        book.add_ask(103.0, 300)

        fills = book.execute_market_buy(700)

        assert len(fills) == 3
        assert fills[0] == (101.0, 300)
        assert fills[1] == (102.0, 300)
        assert fills[2] == (103.0, 100)

    def test_execute_market_sell_air_pocket(self):
        """Market sell falling through air pocket (August 24 scenario)"""
        book = OrderBook()
        book.add_bid(100.0, 500)
        book.add_bid(99.0, 300)
        # AIR POCKET: no bids between 99 and 90
        book.add_bid(90.0, 400)

        # Try to sell 1000 shares
        fills = book.execute_market_sell(1000)

        # Should fill at: 500@100, 300@99, 200@90
        assert len(fills) == 3
        assert fills[0] == (100.0, 500)
        assert fills[1] == (99.0, 300)
        assert fills[2] == (90.0, 200)

        # Average price calculation
        total_value = sum(price * size for price, size in fills)
        total_shares = sum(size for _, size in fills)
        avg_price = total_value / total_shares

        # Average should be well below $100
        assert avg_price < 97.0

    def test_execute_market_buy_insufficient_liquidity(self):
        """Market buy with insufficient liquidity should raise error"""
        book = OrderBook()
        book.add_ask(101.0, 100)

        with pytest.raises(ValueError, match="Insufficient liquidity"):
            book.execute_market_buy(500)


class TestLimitOrders:
    """Test limit order execution"""

    def test_execute_limit_buy_immediate_fill(self):
        """Limit buy that fills immediately"""
        book = OrderBook()
        book.add_ask(100.0, 500)

        fills = book.execute_limit_buy(300, 101.0)

        assert len(fills) == 1
        assert fills[0] == (100.0, 300)  # Filled at better price

    def test_execute_limit_buy_no_fill(self):
        """Limit buy that doesn't fill"""
        book = OrderBook()
        book.add_ask(102.0, 500)

        fills = book.execute_limit_buy(300, 101.0)

        assert len(fills) == 0  # No fill below limit
        # Order should be added to book
        assert len(book.bids) == 1
        assert book.bids[0].price == 101.0
        assert book.bids[0].size == 300

    def test_execute_limit_buy_partial_fill(self):
        """Limit buy with partial fill"""
        book = OrderBook()
        book.add_ask(100.0, 200)
        book.add_ask(102.0, 500)

        fills = book.execute_limit_buy(500, 101.0)

        # Should fill 200 at 100, rest becomes resting order
        assert len(fills) == 1
        assert fills[0] == (100.0, 200)
        assert len(book.bids) == 1
        assert book.bids[0].size == 300  # 500 - 200 resting


class TestStopLossCascade:
    """Test stop-loss cascade simulation"""

    def test_simulate_stop_loss_cascade(self):
        """Simulate cascading stop-loss orders"""
        initial_price = 100.0
        stop_levels = [99.0, 98.0, 97.0]
        order_sizes = [500, 300, 400]

        result = simulate_stop_loss_cascade(initial_price, stop_levels, order_sizes)

        assert 'triggers' in result
        assert 'executions' in result
        assert 'slippage' in result

        # Should have same number of triggers, executions, slippage
        assert len(result['triggers']) == len(stop_levels)
        assert len(result['executions']) == len(order_sizes)

        # Executions should be worse than triggers
        for trigger, execution in zip(result['triggers'], result['executions']):
            assert execution < trigger


class TestDisplayFunctions:
    """Test display and formatting"""

    def test_display_book_returns_string(self):
        """display_book should return formatted string"""
        book = OrderBook()
        book.add_bid(100.0, 500)
        book.add_ask(101.0, 500)

        output = book.display_book()

        assert isinstance(output, str)
        assert 'BIDS' in output
        assert 'ASKS' in output
        assert '100.00' in output
        assert '101.00' in output


class TestEdgeCases:
    """Test edge cases"""

    def test_zero_size_order(self):
        """Zero size orders should be rejected"""
        book = OrderBook()

        with pytest.raises(ValueError, match="greater than zero"):
            book.add_bid(100.0, 0)

    def test_negative_price(self):
        """Negative prices should be rejected"""
        book = OrderBook()

        with pytest.raises(ValueError, match="non-negative"):
            book.add_bid(-100.0, 500)

    def test_negative_size(self):
        """Negative sizes should be rejected"""
        book = OrderBook()

        with pytest.raises(ValueError, match="greater than zero"):
            book.add_bid(100.0, -500)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
