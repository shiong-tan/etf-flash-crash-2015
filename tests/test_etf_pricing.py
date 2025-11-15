"""
Tests for ETF Pricing Module

Educational tests demonstrating correct usage of pricing functions.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from etf_pricing import (
    calculate_nav, calculate_inav, arbitrage_spread,
    creation_profit, redemption_profit, simulate_stale_inav
)


class TestBasicPricing:
    """Test NAV and iNAV calculations"""

    def test_calculate_nav_simple(self):
        """Test NAV calculation with simple holdings"""
        holdings = {'AAPL': 100, 'MSFT': 200}
        prices = {'AAPL': 150.0, 'MSFT': 300.0}
        shares_outstanding = 1000

        nav = calculate_nav(holdings, prices, shares_outstanding)

        # (100*150 + 200*300) / 1000 = 75
        assert nav == 75.0

    def test_calculate_inav_same_as_nav_with_same_prices(self):
        """iNAV should equal NAV when prices are the same"""
        holdings = {'AAPL': 100, 'MSFT': 200}
        prices = {'AAPL': 150.0, 'MSFT': 300.0}
        shares_outstanding = 1000

        nav = calculate_nav(holdings, prices, shares_outstanding)
        inav = calculate_inav(holdings, prices, shares_outstanding)

        assert nav == inav

    def test_calculate_nav_validates_missing_prices(self):
        """NAV calculation should fail if prices are missing"""
        holdings = {'AAPL': 100, 'MSFT': 200}
        prices = {'AAPL': 150.0}  # Missing MSFT
        shares_outstanding = 1000

        with pytest.raises(ValueError, match="Missing prices"):
            calculate_nav(holdings, prices, shares_outstanding)

    def test_calculate_nav_validates_negative_prices(self):
        """NAV calculation should reject negative prices"""
        holdings = {'AAPL': 100}
        prices = {'AAPL': -150.0}
        shares_outstanding = 1000

        with pytest.raises(ValueError, match="non-negative"):
            calculate_nav(holdings, prices, shares_outstanding)


class TestArbitrage:
    """Test arbitrage spread calculations"""

    def test_arbitrage_spread_premium(self):
        """Test spread calculation when ETF trades at premium"""
        etf_price = 101.0
        fair_value = 100.0

        result = arbitrage_spread(etf_price, fair_value)

        assert result['spread_pct'] == 1.0
        assert result['spread_bps'] == 100
        assert result['profitable_creation'] is True
        assert result['profitable_redemption'] is False
        assert result['action'] == 'create'

    def test_arbitrage_spread_discount(self):
        """Test spread calculation when ETF trades at discount"""
        etf_price = 99.0
        fair_value = 100.0

        result = arbitrage_spread(etf_price, fair_value)

        assert result['spread_pct'] == -1.0
        assert result['spread_bps'] == -100
        assert result['profitable_creation'] is False
        assert result['profitable_redemption'] is True
        assert result['action'] == 'redeem'

    def test_arbitrage_spread_fair_value(self):
        """Test spread calculation when ETF trades at fair value"""
        etf_price = 100.0
        fair_value = 100.0

        result = arbitrage_spread(etf_price, fair_value)

        assert result['spread_pct'] == 0.0
        assert result['action'] == 'none'


class TestCreationRedemption:
    """Test creation and redemption profit calculations"""

    def test_creation_profit_profitable(self):
        """Test profitable creation scenario"""
        etf_price = 101.0
        basket_value = 5_000_000  # 50,000 shares * $100
        creation_unit_size = 50_000
        transaction_costs_bps = 25.0

        result = creation_profit(
            etf_price, basket_value, creation_unit_size, transaction_costs_bps
        )

        assert result['etf_value'] == etf_price * creation_unit_size
        assert result['basket_cost'] == basket_value
        assert result['gross_profit'] > 0
        assert 'net_profit' in result
        assert 'transaction_costs' in result

    def test_redemption_profit_profitable(self):
        """Test profitable redemption scenario"""
        etf_price = 99.0
        basket_value = 5_000_000
        creation_unit_size = 50_000
        transaction_costs_bps = 25.0

        result = redemption_profit(
            etf_price, basket_value, creation_unit_size, transaction_costs_bps
        )

        assert result['etf_cost'] == etf_price * creation_unit_size
        assert result['basket_value_received'] == basket_value
        assert result['gross_profit'] > 0


class TestStaleINAV:
    """Test stale iNAV simulation (August 24, 2015 scenario)"""

    def test_simulate_stale_inav_basic(self):
        """Test stale iNAV calculation with halted stocks"""
        holdings = {f'STOCK_{i}': 1 for i in range(100)}
        stale_prices = {f'STOCK_{i}': 100.0 for i in range(100)}

        # 20 stocks halted, 80 down 5%
        # If halted stocks were trading, they would also be down 5%
        halted_tickers = [f'STOCK_{i}' for i in range(20)]
        current_prices = {
            ticker: stale_prices[ticker] * 0.95  # All stocks down 5% in reality
            for ticker in holdings.keys()
        }

        result = simulate_stale_inav(
            holdings, current_prices, stale_prices, halted_tickers, 100
        )

        assert result['pct_halted'] == 20.0
        assert result['num_halted'] == 20
        # iNAV with stale uses $100 for halted, $95 for trading
        # True iNAV uses $95 for all
        # So inav_with_stale should be > inav_true
        assert result['inav_with_stale'] > result['inav_true']
        assert result['error_pct'] > 0

    def test_simulate_stale_inav_no_halts(self):
        """Test stale iNAV when no stocks are halted"""
        holdings = {f'STOCK_{i}': 1 for i in range(100)}
        prices = {f'STOCK_{i}': 100.0 for i in range(100)}

        result = simulate_stale_inav(
            holdings, prices, prices, [], 100
        )

        assert result['pct_halted'] == 0.0
        assert result['inav_with_stale'] == result['inav_true']
        assert result['error_pct'] == 0.0


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_holdings(self):
        """Empty holdings should raise error"""
        with pytest.raises(ValueError, match="cannot be empty"):
            calculate_nav({}, {}, 1000)

    def test_zero_shares_outstanding(self):
        """Zero shares outstanding should raise error"""
        holdings = {'AAPL': 100}
        prices = {'AAPL': 150.0}

        with pytest.raises(ValueError, match="greater than zero"):
            calculate_nav(holdings, prices, 0)

    def test_negative_holdings(self):
        """Negative holdings should raise error"""
        holdings = {'AAPL': -100}
        prices = {'AAPL': 150.0}

        with pytest.raises(ValueError, match="non-negative"):
            calculate_nav(holdings, prices, 1000)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
