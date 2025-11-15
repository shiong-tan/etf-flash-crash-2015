"""
Tests for Arbitrage Analysis Module

Educational tests demonstrating arbitrage analysis during flash crash.
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from src.arbitrage_analysis import (
    ArbitrageType,
    BarrierType,
    ArbitrageOpportunity,
    ETFArbitrageAnalyzer,
    calculate_no_arbitrage_bounds,
    identify_arbitrage_barriers
)


class TestEnums:
    """Test enum definitions"""

    def test_arbitrage_type_values(self):
        """Test ArbitrageType enum values"""
        assert ArbitrageType.CREATION.value == "creation"
        assert ArbitrageType.REDEMPTION.value == "redemption"
        assert ArbitrageType.NONE.value == "none"

    def test_arbitrage_type_members(self):
        """Test ArbitrageType has all expected members"""
        assert len(ArbitrageType) == 3
        assert hasattr(ArbitrageType, 'CREATION')
        assert hasattr(ArbitrageType, 'REDEMPTION')
        assert hasattr(ArbitrageType, 'NONE')

    def test_barrier_type_values(self):
        """Test BarrierType enum values"""
        assert BarrierType.HALTED_COMPONENTS.value == "halted_components"
        assert BarrierType.STALE_INAV.value == "stale_inav"
        assert BarrierType.LIQUIDITY_COST.value == "liquidity_cost"
        assert BarrierType.CAPITAL_CONSTRAINT.value == "capital_constraint"
        assert BarrierType.SETTLEMENT_RISK.value == "settlement_risk"

    def test_barrier_type_members(self):
        """Test BarrierType has all expected members"""
        assert len(BarrierType) == 5
        assert hasattr(BarrierType, 'HALTED_COMPONENTS')
        assert hasattr(BarrierType, 'STALE_INAV')
        assert hasattr(BarrierType, 'LIQUIDITY_COST')


class TestArbitrageOpportunity:
    """Test ArbitrageOpportunity dataclass"""

    def test_create_opportunity(self):
        """Test creating an arbitrage opportunity"""
        opp = ArbitrageOpportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=101.0,
            inav=100.0,
            spread_pct=1.0,
            arb_type=ArbitrageType.CREATION,
            gross_profit_per_unit=1.0,
            transaction_costs=0.25,
            net_profit_per_unit=0.75,
            is_profitable=True,
            barriers=[]
        )

        assert opp.etf_symbol == 'SPY'
        assert opp.etf_price == 101.0
        assert opp.inav == 100.0
        assert opp.spread_pct == 1.0
        assert opp.arb_type == ArbitrageType.CREATION
        assert opp.is_profitable is True
        assert len(opp.barriers) == 0

    def test_is_executable_no_barriers(self):
        """Test is_executable returns True when profitable with no barriers"""
        opp = ArbitrageOpportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=101.0,
            inav=100.0,
            spread_pct=1.0,
            arb_type=ArbitrageType.CREATION,
            gross_profit_per_unit=1.0,
            transaction_costs=0.25,
            net_profit_per_unit=0.75,
            is_profitable=True,
            barriers=[]
        )

        assert opp.is_executable() is True

    def test_is_executable_with_barriers(self):
        """Test is_executable returns False when barriers present"""
        opp = ArbitrageOpportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=101.0,
            inav=100.0,
            spread_pct=1.0,
            arb_type=ArbitrageType.CREATION,
            gross_profit_per_unit=1.0,
            transaction_costs=0.25,
            net_profit_per_unit=0.75,
            is_profitable=True,
            barriers=[BarrierType.HALTED_COMPONENTS]
        )

        assert opp.is_executable() is False

    def test_is_executable_not_profitable(self):
        """Test is_executable returns False when not profitable"""
        opp = ArbitrageOpportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=100.1,
            inav=100.0,
            spread_pct=0.1,
            arb_type=ArbitrageType.CREATION,
            gross_profit_per_unit=0.1,
            transaction_costs=0.25,
            net_profit_per_unit=-0.15,
            is_profitable=False,
            barriers=[]
        )

        assert opp.is_executable() is False


class TestETFArbitrageAnalyzer:
    """Test ETFArbitrageAnalyzer class"""

    def setup_method(self):
        """Create analyzer for testing"""
        self.analyzer = ETFArbitrageAnalyzer(
            transaction_costs_bps=25.0,
            creation_unit_size=50_000,
            min_profit_threshold=0.001
        )

    def test_initialization_default(self):
        """Test analyzer initializes with default parameters"""
        analyzer = ETFArbitrageAnalyzer()
        assert analyzer.transaction_costs_bps == 25.0
        assert analyzer.creation_unit_size == 50_000
        assert analyzer.min_profit_threshold == 0.001

    def test_initialization_custom(self):
        """Test analyzer initializes with custom parameters"""
        analyzer = ETFArbitrageAnalyzer(
            transaction_costs_bps=50.0,
            creation_unit_size=100_000,
            min_profit_threshold=0.002
        )
        assert analyzer.transaction_costs_bps == 50.0
        assert analyzer.creation_unit_size == 100_000
        assert analyzer.min_profit_threshold == 0.002

    def test_analyze_opportunity_creation(self):
        """Test analyzing creation arbitrage (ETF at premium)"""
        opp = self.analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=101.0,
            inav=100.0,
            halted_component_pct=0.0,
            inav_staleness_minutes=0.0
        )

        assert opp.etf_symbol == 'SPY'
        assert opp.etf_price == 101.0
        assert opp.inav == 100.0
        assert opp.spread_pct == 1.0
        assert opp.arb_type == ArbitrageType.CREATION
        assert opp.gross_profit_per_unit == 1.0
        assert opp.transaction_costs > 0
        assert opp.net_profit_per_unit > 0
        assert opp.is_profitable is True

    def test_analyze_opportunity_redemption(self):
        """Test analyzing redemption arbitrage (ETF at discount)"""
        opp = self.analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=99.0,
            inav=100.0,
            halted_component_pct=0.0,
            inav_staleness_minutes=0.0
        )

        assert opp.spread_pct == -1.0
        assert opp.arb_type == ArbitrageType.REDEMPTION
        assert opp.gross_profit_per_unit == 1.0
        assert opp.is_profitable is True

    def test_analyze_opportunity_no_arbitrage(self):
        """Test analyzing when ETF at fair value"""
        opp = self.analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=100.0,
            inav=100.0,
            halted_component_pct=0.0,
            inav_staleness_minutes=0.0
        )

        assert opp.spread_pct == 0.0
        assert opp.arb_type == ArbitrageType.NONE
        assert opp.gross_profit_per_unit == 0.0
        assert opp.is_profitable is False

    def test_analyze_opportunity_halted_components_barrier(self):
        """Test that halted components create barrier"""
        opp = self.analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='RSP',
            etf_price=110.0,
            inav=100.0,
            halted_component_pct=30.0,  # >20% halted
            inav_staleness_minutes=0.0
        )

        assert BarrierType.HALTED_COMPONENTS in opp.barriers
        assert opp.is_executable() is False

    def test_analyze_opportunity_stale_inav_barrier(self):
        """Test that stale iNAV creates barrier"""
        opp = self.analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='RSP',
            etf_price=110.0,
            inav=100.0,
            halted_component_pct=0.0,
            inav_staleness_minutes=10.0  # >5 minutes stale
        )

        assert BarrierType.STALE_INAV in opp.barriers
        assert opp.is_executable() is False

    def test_analyze_opportunity_liquidity_cost_barrier(self):
        """Test that high costs create liquidity barrier"""
        # Create analyzer with very high costs
        high_cost_analyzer = ETFArbitrageAnalyzer(
            transaction_costs_bps=500.0  # 5% transaction costs
        )

        opp = high_cost_analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=101.0,
            inav=100.0,
            halted_component_pct=0.0,
            inav_staleness_minutes=0.0
        )

        # 1% spread but 5% costs = negative net profit
        assert opp.net_profit_per_unit < 0
        assert BarrierType.LIQUIDITY_COST in opp.barriers

    def test_analyze_opportunity_extreme_spread_barrier(self):
        """Test that extreme spreads create settlement risk barrier"""
        opp = self.analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='RSP',
            etf_price=130.0,
            inav=100.0,
            halted_component_pct=0.0,
            inav_staleness_minutes=0.0
        )

        # 30% spread is extreme
        assert abs(opp.spread_pct) > 20
        assert BarrierType.SETTLEMENT_RISK in opp.barriers

    def test_analyze_opportunity_multiple_barriers(self):
        """Test that multiple barriers can exist simultaneously"""
        opp = self.analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='RSP',
            etf_price=130.0,
            inav=100.0,
            halted_component_pct=50.0,  # Halted components barrier
            inav_staleness_minutes=15.0  # Stale iNAV barrier
        )

        # Should have multiple barriers
        assert len(opp.barriers) >= 2
        assert BarrierType.HALTED_COMPONENTS in opp.barriers
        assert BarrierType.STALE_INAV in opp.barriers
        assert BarrierType.SETTLEMENT_RISK in opp.barriers

    def test_calculate_required_capital_single_unit(self):
        """Test capital calculation for single creation unit"""
        capital = self.analyzer.calculate_required_capital(
            etf_price=100.0,
            target_units=1
        )

        # 50,000 shares * $100 * 1.20 buffer = $6,000,000
        expected = 100.0 * 50_000 * 1.20
        assert capital == expected

    def test_calculate_required_capital_multiple_units(self):
        """Test capital calculation for multiple creation units"""
        capital = self.analyzer.calculate_required_capital(
            etf_price=100.0,
            target_units=5
        )

        # 5 * 50,000 shares * $100 * 1.20 buffer = $30,000,000
        expected = 100.0 * 50_000 * 5 * 1.20
        assert capital == expected

    def test_calculate_required_capital_high_price(self):
        """Test capital calculation with high ETF price"""
        capital = self.analyzer.calculate_required_capital(
            etf_price=500.0,
            target_units=1
        )

        expected = 500.0 * 50_000 * 1.20
        assert capital == expected


class TestNoArbitrageBounds:
    """Test calculate_no_arbitrage_bounds function"""

    def test_calculate_bounds_default_costs(self):
        """Test no-arbitrage bounds with default costs"""
        lower, upper = calculate_no_arbitrage_bounds(100.0)

        # 25 bps = 0.25% = 0.0025
        assert abs(lower - 99.75) < 0.01
        assert abs(upper - 100.25) < 0.01

    def test_calculate_bounds_custom_costs(self):
        """Test no-arbitrage bounds with custom costs"""
        lower, upper = calculate_no_arbitrage_bounds(100.0, 50.0)

        # 50 bps = 0.50% = 0.005
        assert abs(lower - 99.50) < 0.01
        assert abs(upper - 100.50) < 0.01

    def test_calculate_bounds_high_nav(self):
        """Test no-arbitrage bounds with high NAV"""
        lower, upper = calculate_no_arbitrage_bounds(500.0, 25.0)

        # 25 bps of 500 = 1.25
        assert abs(lower - 498.75) < 0.01
        assert abs(upper - 501.25) < 0.01

    def test_bounds_are_symmetric(self):
        """Test that bounds are symmetric around NAV"""
        nav = 100.0
        lower, upper = calculate_no_arbitrage_bounds(nav, 25.0)

        assert abs((nav - lower) - (upper - nav)) < 0.01


class TestIdentifyArbitrageBarriers:
    """Test identify_arbitrage_barriers function"""

    def test_identify_barriers_basic(self):
        """Test basic barrier identification across time series"""
        # Create time series data
        timestamps = pd.date_range('2015-08-24 09:30', periods=5, freq='1min')

        etf_prices = pd.Series([100.0, 110.0, 120.0, 105.0, 102.0], index=timestamps)
        inav_values = pd.Series([100.0, 100.0, 100.0, 100.0, 100.0], index=timestamps)
        halted_components = pd.Series([0.0, 10.0, 30.0, 20.0, 5.0], index=timestamps)
        inav_update_times = pd.Series(timestamps, index=timestamps)

        df = identify_arbitrage_barriers(
            etf_prices, inav_values, halted_components, inav_update_times
        )

        assert len(df) == 5
        assert 'timestamp' in df.columns
        assert 'etf_price' in df.columns
        assert 'inav' in df.columns
        assert 'spread_pct' in df.columns
        assert 'arb_type' in df.columns
        assert 'profitable' in df.columns
        assert 'executable' in df.columns
        assert 'barriers' in df.columns
        assert 'num_barriers' in df.columns

    def test_identify_barriers_no_barriers(self):
        """Test when no barriers exist"""
        timestamps = pd.date_range('2015-08-24 09:30', periods=3, freq='1min')

        etf_prices = pd.Series([100.5, 100.3, 100.4], index=timestamps)
        inav_values = pd.Series([100.0, 100.0, 100.0], index=timestamps)
        halted_components = pd.Series([0.0, 0.0, 0.0], index=timestamps)
        inav_update_times = pd.Series(timestamps, index=timestamps)

        df = identify_arbitrage_barriers(
            etf_prices, inav_values, halted_components, inav_update_times
        )

        # Small spreads, no halts, fresh iNAV
        # Some should be profitable and executable
        assert (df['num_barriers'] == 0).any()

    def test_identify_barriers_halted_components(self):
        """Test barrier identification with halted components"""
        timestamps = pd.date_range('2015-08-24 09:30', periods=2, freq='1min')

        etf_prices = pd.Series([110.0, 110.0], index=timestamps)
        inav_values = pd.Series([100.0, 100.0], index=timestamps)
        halted_components = pd.Series([50.0, 50.0], index=timestamps)  # 50% halted
        inav_update_times = pd.Series(timestamps, index=timestamps)

        df = identify_arbitrage_barriers(
            etf_prices, inav_values, halted_components, inav_update_times
        )

        # Should detect halted_components barrier
        assert 'halted_components' in df['barriers'].iloc[0]
        assert df['executable'].iloc[0] == False

    def test_identify_barriers_stale_inav(self):
        """Test barrier identification with stale iNAV"""
        timestamps = pd.date_range('2015-08-24 09:30', periods=2, freq='1min')

        etf_prices = pd.Series([110.0, 110.0], index=timestamps)
        inav_values = pd.Series([100.0, 100.0], index=timestamps)
        halted_components = pd.Series([0.0, 0.0], index=timestamps)
        # iNAV 10 minutes stale
        inav_update_times = pd.Series([timestamps[0] - timedelta(minutes=10),
                                        timestamps[1] - timedelta(minutes=10)],
                                       index=timestamps)

        df = identify_arbitrage_barriers(
            etf_prices, inav_values, halted_components, inav_update_times
        )

        # Should detect stale_inav barrier
        assert 'stale_inav' in df['barriers'].iloc[0]

    def test_identify_barriers_arbitrage_types(self):
        """Test that different arbitrage types are correctly identified"""
        timestamps = pd.date_range('2015-08-24 09:30', periods=3, freq='1min')

        # Premium, fair value, discount
        etf_prices = pd.Series([101.0, 100.0, 99.0], index=timestamps)
        inav_values = pd.Series([100.0, 100.0, 100.0], index=timestamps)
        halted_components = pd.Series([0.0, 0.0, 0.0], index=timestamps)
        inav_update_times = pd.Series(timestamps, index=timestamps)

        df = identify_arbitrage_barriers(
            etf_prices, inav_values, halted_components, inav_update_times
        )

        assert df['arb_type'].iloc[0] == 'creation'  # Premium
        assert df['arb_type'].iloc[1] == 'none'  # Fair value
        assert df['arb_type'].iloc[2] == 'redemption'  # Discount


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_zero_spread(self):
        """Test handling of zero spread (fair value)"""
        analyzer = ETFArbitrageAnalyzer()
        opp = analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=100.0,
            inav=100.0
        )

        assert opp.spread_pct == 0.0
        assert opp.arb_type == ArbitrageType.NONE
        assert opp.gross_profit_per_unit == 0.0

    def test_very_small_spread(self):
        """Test handling of very small spreads"""
        analyzer = ETFArbitrageAnalyzer()
        opp = analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=100.01,
            inav=100.0
        )

        # Small spread should not be profitable after costs
        assert opp.is_profitable is False

    def test_negative_price_difference(self):
        """Test redemption (discount) scenario"""
        analyzer = ETFArbitrageAnalyzer()
        opp = analyzer.analyze_opportunity(
            timestamp=pd.Timestamp.now(),
            etf_symbol='SPY',
            etf_price=95.0,
            inav=100.0
        )

        assert opp.spread_pct == -5.0
        assert opp.arb_type == ArbitrageType.REDEMPTION
        assert opp.gross_profit_per_unit == 5.0  # abs(spread)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
