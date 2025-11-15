"""
Tests for LULD Band Calculator

Tests the luld_calculator module against SEC/FINRA specifications
and validates calculations against August 24, 2015 historical data.
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from luld_calculator import (
    calculate_luld_bands,
    get_time_of_day_category,
    analyze_flash_crash_halt
)


class TestCalculateLULDBands:
    """Test LULD band calculations for various scenarios."""

    def test_tier1_above_3_normal(self):
        """Test Tier 1 stock above $3 during normal hours (5% bands)."""
        lower, upper, pct = calculate_luld_bands(100.00, tier=1, time_of_day='normal')
        assert lower == 95.00
        assert upper == 105.00
        assert pct == 0.05

    def test_tier2_above_3_normal(self):
        """Test Tier 2 stock above $3 during normal hours (10% bands)."""
        lower, upper, pct = calculate_luld_bands(100.00, tier=2, time_of_day='normal')
        assert lower == pytest.approx(90.00)
        assert upper == pytest.approx(110.00)
        assert pct == pytest.approx(0.10)

    def test_tier1_above_3_opening(self):
        """Test Tier 1 stock above $3 during opening period (10% bands - doubled)."""
        lower, upper, pct = calculate_luld_bands(100.00, tier=1, time_of_day='opening')
        assert lower == pytest.approx(90.00)
        assert upper == pytest.approx(110.00)
        assert pct == pytest.approx(0.10)

    def test_tier2_above_3_opening(self):
        """Test Tier 2 stock above $3 during opening period (20% bands - doubled)."""
        lower, upper, pct = calculate_luld_bands(100.00, tier=2, time_of_day='opening')
        assert lower == 80.00
        assert upper == 120.00
        assert pct == 0.20

    def test_tier1_above_3_closing(self):
        """Test Tier 1 stock above $3 during closing period (10% bands - doubled)."""
        lower, upper, pct = calculate_luld_bands(100.00, tier=1, time_of_day='closing')
        assert lower == pytest.approx(90.00)
        assert upper == pytest.approx(110.00)
        assert pct == pytest.approx(0.10)

    def test_price_range_075_to_3(self):
        """Test stock in $0.75-$3 range (20% bands for both tiers)."""
        # Tier 1
        lower, upper, pct = calculate_luld_bands(2.00, tier=1, time_of_day='normal')
        assert lower == 1.60
        assert upper == 2.40
        assert pct == 0.20

        # Tier 2 (should be same)
        lower, upper, pct = calculate_luld_bands(2.00, tier=2, time_of_day='normal')
        assert lower == 1.60
        assert upper == 2.40
        assert pct == 0.20

    def test_price_below_075_percentage_band(self):
        """Test stock below $0.75 using 75% band (when larger than $0.15)."""
        # At $0.50, 75% band = $0.375, which is > $0.15, so use 75%
        lower, upper, pct = calculate_luld_bands(0.50, tier=1, time_of_day='normal')
        assert lower == 0.125  # 0.50 * 0.25
        assert upper == 0.875  # 0.50 * 1.75
        assert pct == 0.75

    def test_price_below_075_flat_band(self):
        """Test stock below $0.75 using $0.15 flat band (when larger than 75%)."""
        # At $0.10, 75% band = $0.075, which is < $0.15, so use $0.15
        # $0.15 as percentage of $0.10 = 150%
        # CRITICAL FIX: Lower band now floored at $0.00 (cannot be negative)
        lower, upper, pct = calculate_luld_bands(0.10, tier=1, time_of_day='normal')
        assert lower == pytest.approx(0.00)   # Floored at zero (0.10 - 0.15 = -0.05 → 0.00)
        assert upper == pytest.approx(0.25)   # 0.10 + 0.15
        assert pct == pytest.approx(1.5)      # 150%

    def test_leveraged_etp_2x(self):
        """Test 2x leveraged ETP (bands doubled)."""
        lower, upper, pct = calculate_luld_bands(
            100.00, tier=1, time_of_day='normal', leverage=2.0
        )
        assert lower == pytest.approx(90.00)  # 5% * 2 = 10%
        assert upper == pytest.approx(110.00)
        assert pct == pytest.approx(0.10)

    def test_leveraged_etp_3x_opening(self):
        """Test 3x leveraged ETP during opening (bands tripled, then doubled for opening)."""
        lower, upper, pct = calculate_luld_bands(
            100.00, tier=1, time_of_day='opening', leverage=3.0
        )
        assert lower == pytest.approx(70.00)  # 5% * 2 (opening) * 3 (leverage) = 30%
        assert upper == pytest.approx(130.00)
        assert pct == pytest.approx(0.30)

    def test_edge_case_exact_3_dollars(self):
        """Test stock exactly at $3.00 (should use above $3 bands)."""
        lower, upper, pct = calculate_luld_bands(3.00, tier=1, time_of_day='normal')
        assert lower == pytest.approx(2.85)  # 5% band
        assert upper == pytest.approx(3.15)
        assert pct == pytest.approx(0.05)

    def test_edge_case_exact_075_dollars(self):
        """Test stock exactly at $0.75 (should use $0.75-$3 bands)."""
        lower, upper, pct = calculate_luld_bands(0.75, tier=1, time_of_day='normal')
        assert lower == pytest.approx(0.60)  # 20% band
        assert upper == pytest.approx(0.90)
        assert pct == pytest.approx(0.20)


class TestGetTimeOfDayCategory:
    """Test time-of-day categorization for LULD bands."""

    def test_opening_period_start(self):
        """Test 9:30 AM (start of opening period)."""
        dt = datetime(2015, 8, 24, 9, 30, 0)
        assert get_time_of_day_category(dt) == 'opening'

    def test_opening_period_middle(self):
        """Test 9:35 AM (middle of opening period)."""
        dt = datetime(2015, 8, 24, 9, 35, 0)
        assert get_time_of_day_category(dt) == 'opening'

    def test_opening_period_end(self):
        """Test 9:44 AM (end of opening period)."""
        dt = datetime(2015, 8, 24, 9, 44, 59)
        assert get_time_of_day_category(dt) == 'opening'

    def test_normal_period_just_after_opening(self):
        """Test 9:45 AM (just after opening period)."""
        dt = datetime(2015, 8, 24, 9, 45, 0)
        assert get_time_of_day_category(dt) == 'normal'

    def test_normal_period_midday(self):
        """Test 12:00 PM (normal trading)."""
        dt = datetime(2015, 8, 24, 12, 0, 0)
        assert get_time_of_day_category(dt) == 'normal'

    def test_closing_period_start(self):
        """Test 3:35 PM (start of closing period)."""
        dt = datetime(2015, 8, 24, 15, 35, 0)
        assert get_time_of_day_category(dt) == 'closing'

    def test_closing_period_middle(self):
        """Test 3:45 PM (middle of closing period)."""
        dt = datetime(2015, 8, 24, 15, 45, 0)
        assert get_time_of_day_category(dt) == 'closing'

    def test_closing_period_end(self):
        """Test 4:00 PM (market close - exclusive end of closing period)."""
        dt = datetime(2015, 8, 24, 16, 0, 0)
        # FIX: 4:00 PM exact is when market CLOSES, not in closing period
        # Closing period is 3:35-4:00 PM (exclusive end)
        assert get_time_of_day_category(dt) == 'normal'


class TestAnalyzeFlashCrashHalt:
    """Test flash crash halt analysis against historical data."""

    def test_dvy_at_935am(self):
        """Test DVY at 9:35 AM on August 24, 2015."""
        result = analyze_flash_crash_halt(
            ticker='DVY',
            reference_price=75.50,
            actual_price=65.20,
            tier=1,
            timestamp=datetime(2015, 8, 24, 9, 35, 0)
        )

        # Should be in opening period
        assert result['time_category'] == 'opening'

        # Opening period bands should be 10% (doubled from 5%)
        assert result['band_percentage'] == 10.0

        # Lower band: 75.50 * 0.90 = 67.95
        assert result['lower_band'] == pytest.approx(67.95, abs=0.01)

        # Upper band: 75.50 * 1.10 = 83.05
        assert result['upper_band'] == pytest.approx(83.05, abs=0.01)

        # Actual price 65.20 is below 67.95, so halt should trigger
        assert result['halt_triggered'] is True

        # Price change: 65.20 - 75.50 = -10.30
        assert result['price_change'] == pytest.approx(-10.30, abs=0.01)

        # Price change %: -10.30 / 75.50 = -13.6%
        assert result['price_change_pct'] == pytest.approx(-13.6, abs=0.1)

        # Distance from lower band: 65.20 - 67.95 = -2.75
        assert result['distance_from_band'] == pytest.approx(-2.75, abs=0.01)

    def test_rsp_at_938am(self):
        """Test RSP at 9:38 AM on August 24, 2015."""
        result = analyze_flash_crash_halt(
            ticker='RSP',
            reference_price=76.80,
            actual_price=43.77,
            tier=1,
            timestamp=datetime(2015, 8, 24, 9, 38, 0)
        )

        # Should be in opening period
        assert result['time_category'] == 'opening'

        # Opening period bands should be 10%
        assert result['band_percentage'] == 10.0

        # Lower band: 76.80 * 0.90 = 69.12
        assert result['lower_band'] == pytest.approx(69.12, abs=0.01)

        # Actual price 43.77 is well below 69.12, so halt should trigger
        assert result['halt_triggered'] is True

        # Price change %: (43.77 - 76.80) / 76.80 = -43.0%
        assert result['price_change_pct'] == pytest.approx(-43.0, abs=0.1)

    def test_splv_at_940am(self):
        """Test SPLV at 9:40 AM on August 24, 2015."""
        result = analyze_flash_crash_halt(
            ticker='SPLV',
            reference_price=39.50,
            actual_price=21.18,
            tier=1,
            timestamp=datetime(2015, 8, 24, 9, 40, 0)
        )

        # Should be in opening period
        assert result['time_category'] == 'opening'

        # Opening period bands should be 10%
        assert result['band_percentage'] == 10.0

        # Lower band: 39.50 * 0.90 = 35.55
        assert result['lower_band'] == pytest.approx(35.55, abs=0.01)

        # Actual price 21.18 is well below 35.55, so halt should trigger
        assert result['halt_triggered'] is True

        # Price change %: (21.18 - 39.50) / 39.50 = -46.4%
        assert result['price_change_pct'] == pytest.approx(-46.4, abs=0.1)

    def test_no_halt_within_bands(self):
        """Test stock trading within bands (no halt)."""
        result = analyze_flash_crash_halt(
            ticker='SPY',
            reference_price=200.00,
            actual_price=199.00,  # -0.5%, well within 5% band
            tier=1,
            timestamp=datetime(2015, 8, 24, 10, 0, 0)
        )

        # Should be in normal period (after 9:45)
        assert result['time_category'] == 'normal'

        # Normal period bands should be 5%
        assert result['band_percentage'] == 5.0

        # No halt should trigger
        assert result['halt_triggered'] is False

    def test_halt_at_upper_band(self):
        """Test stock hitting upper band (upward halt)."""
        result = analyze_flash_crash_halt(
            ticker='TEST',
            reference_price=100.00,
            actual_price=105.50,  # Above 5% upper band
            tier=1,
            timestamp=datetime(2015, 8, 24, 10, 0, 0)
        )

        # Should trigger halt
        assert result['halt_triggered'] is True

        # Distance should be positive (above upper band)
        assert result['distance_from_band'] > 0


class TestHistoricalAccuracy:
    """Validate calculator against known historical data."""

    def test_all_three_etfs_halted_opening_period(self):
        """Verify all three major ETFs triggered halts during opening period."""
        # DVY
        dvy = analyze_flash_crash_halt('DVY', 75.50, 65.20, 1, datetime(2015, 8, 24, 9, 35, 0))
        assert dvy['halt_triggered'] is True
        assert dvy['time_category'] == 'opening'

        # RSP
        rsp = analyze_flash_crash_halt('RSP', 76.80, 43.77, 1, datetime(2015, 8, 24, 9, 38, 0))
        assert rsp['halt_triggered'] is True
        assert rsp['time_category'] == 'opening'

        # SPLV
        splv = analyze_flash_crash_halt('SPLV', 39.50, 21.18, 1, datetime(2015, 8, 24, 9, 40, 0))
        assert splv['halt_triggered'] is True
        assert splv['time_category'] == 'opening'

    def test_opening_period_doubled_bands(self):
        """Verify that opening period bands are correctly doubled."""
        # Normal period: 5% for Tier 1
        normal = calculate_luld_bands(100.00, tier=1, time_of_day='normal')
        assert normal[2] == 0.05

        # Opening period: 10% for Tier 1 (doubled)
        opening = calculate_luld_bands(100.00, tier=1, time_of_day='opening')
        assert opening[2] == 0.10

        # Verify bands are exactly double
        assert opening[2] == normal[2] * 2


class TestPennyStockNonNegativity:
    """Test non-negativity constraint for very low-priced stocks."""

    def test_penny_stock_no_negative_bands(self):
        """Ensure no negative bands for any price (CRITICAL FIX validation)."""
        test_prices = [0.01, 0.05, 0.10, 0.15, 0.20, 0.50, 0.74]
        for price in test_prices:
            lower, upper, pct = calculate_luld_bands(price, tier=1)
            assert lower >= 0.00, f"Negative lower band at price ${price}"
            assert upper > lower, f"Upper band not greater than lower at ${price}"

    def test_very_low_price_01_cents(self):
        """Test extremely low price (1 cent)."""
        lower, upper, pct = calculate_luld_bands(0.01, tier=1, time_of_day='normal')
        assert lower == pytest.approx(0.00)  # Floored at zero
        assert upper > 0.01  # Upper band should be positive
        assert pct > 0  # Band percentage should be positive

    def test_very_low_price_05_cents(self):
        """Test very low price (5 cents)."""
        lower, upper, pct = calculate_luld_bands(0.05, tier=1, time_of_day='normal')
        assert lower == pytest.approx(0.00)  # Floored at zero
        assert upper == pytest.approx(0.20)  # 0.05 + 0.15
        assert pct == pytest.approx(3.0)  # $0.15/$0.05 = 300%

    def test_low_price_20_cents(self):
        """Test transition point (20 cents) where bands start being positive."""
        lower, upper, pct = calculate_luld_bands(0.20, tier=1, time_of_day='normal')
        assert lower == pytest.approx(0.05)  # 0.20 - 0.15 = 0.05 (barely positive)
        assert upper == pytest.approx(0.35)  # 0.20 + 0.15
        assert pct == pytest.approx(0.75)  # $0.15/$0.20 = 75%


class TestBoundaryConditions:
    """Test boundary conditions and edge cases."""

    def test_boundary_945_discontinuity(self):
        """Test band discontinuity at 9:45 AM boundary."""
        ref_price = 100.00

        # 9:44:59 - still opening period
        dt_opening = datetime(2015, 8, 24, 9, 44, 59)
        lower_open, upper_open, pct_open = calculate_luld_bands(
            ref_price, tier=1, time_of_day=get_time_of_day_category(dt_opening)
        )
        assert pct_open == 0.10  # Doubled

        # 9:45:00 - normal period starts
        dt_normal = datetime(2015, 8, 24, 9, 45, 0)
        lower_norm, upper_norm, pct_norm = calculate_luld_bands(
            ref_price, tier=1, time_of_day=get_time_of_day_category(dt_normal)
        )
        assert pct_norm == 0.05  # Standard

        # Verify discontinuity
        assert pct_open == 2 * pct_norm

    def test_boundary_closing_period_exclusive_end(self):
        """Test closing period exclusive end at 4:00 PM."""
        # 3:59:59 - still closing period
        dt_closing = datetime(2015, 8, 24, 15, 59, 59)
        category_closing = get_time_of_day_category(dt_closing)
        assert category_closing == 'closing'

        # 4:00:00 - market closed, but if categorized should be normal
        # (though no trades occur at exactly 4:00 PM)
        dt_market_close = datetime(2015, 8, 24, 16, 0, 0)
        category_close = get_time_of_day_category(dt_market_close)
        assert category_close == 'normal'  # Not 'closing' (fixed bug)

    def test_price_exactly_at_band(self):
        """Test price exactly at band edge."""
        result = analyze_flash_crash_halt(
            ticker='TEST',
            reference_price=100.00,
            actual_price=95.00,  # Exactly at 5% lower band
            tier=1,
            timestamp=datetime(2015, 8, 24, 10, 0, 0)
        )
        # Current behavior uses <= which triggers halt at exact band
        assert result['halt_triggered'] is True
        assert result['distance_from_band'] == pytest.approx(0.00)

    def test_price_just_inside_band(self):
        """Test price just inside band (no halt)."""
        result = analyze_flash_crash_halt(
            ticker='TEST',
            reference_price=100.00,
            actual_price=95.01,  # Just inside 5% lower band
            tier=1,
            timestamp=datetime(2015, 8, 24, 10, 0, 0)
        )
        assert result['halt_triggered'] is False
        assert result['distance_from_band'] > 0


class TestInputValidation:
    """Test input validation and error handling."""

    def test_negative_reference_price_raises_error(self):
        """Test that negative reference price raises ValueError."""
        with pytest.raises(ValueError, match="reference_price must be positive"):
            calculate_luld_bands(-10.00, tier=1)

    def test_zero_reference_price_raises_error(self):
        """Test that zero reference price raises ValueError."""
        with pytest.raises(ValueError, match="reference_price must be positive"):
            calculate_luld_bands(0.00, tier=1)

    def test_invalid_tier_raises_error(self):
        """Test that invalid tier raises ValueError."""
        with pytest.raises(ValueError, match="tier must be 1 or 2"):
            calculate_luld_bands(100.00, tier=5)

    def test_invalid_time_of_day_raises_error(self):
        """Test that invalid time_of_day raises ValueError."""
        with pytest.raises(ValueError, match="time_of_day must be"):
            calculate_luld_bands(100.00, tier=1, time_of_day='morning')

    def test_negative_leverage_raises_error(self):
        """Test that negative leverage raises ValueError."""
        with pytest.raises(ValueError, match="leverage must be in"):
            calculate_luld_bands(100.00, tier=1, leverage=-1.0)

    def test_zero_leverage_raises_error(self):
        """Test that zero leverage raises ValueError."""
        with pytest.raises(ValueError, match="leverage must be in"):
            calculate_luld_bands(100.00, tier=1, leverage=0.0)

    def test_excessive_leverage_raises_error(self):
        """Test that excessive leverage (>3x) raises ValueError."""
        with pytest.raises(ValueError, match="leverage must be in"):
            calculate_luld_bands(100.00, tier=1, leverage=5.0)


class TestLeveragedETPs:
    """Additional tests for leveraged ETPs."""

    def test_leveraged_etp_3x_closing(self):
        """Test 3x leveraged ETP during closing (bands tripled, then doubled for closing)."""
        lower, upper, pct = calculate_luld_bands(
            100.00, tier=1, time_of_day='closing', leverage=3.0
        )
        assert lower == pytest.approx(70.00)  # 5% * 2 (closing) * 3 (leverage) = 30%
        assert upper == pytest.approx(130.00)
        assert pct == pytest.approx(0.30)

    def test_leveraged_etp_maximum_3x(self):
        """Test 3x leveraged ETP (maximum allowed leverage)."""
        lower, upper, pct = calculate_luld_bands(
            100.00, tier=1, time_of_day='normal', leverage=3.0
        )
        assert lower == pytest.approx(85.00)  # 5% * 3 = 15%
        assert upper == pytest.approx(115.00)
        assert pct == pytest.approx(0.15)
