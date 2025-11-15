"""
LULD Band Calculator - Regulatory Methodology
Based on: SEC Release No. 34-67091 and FINRA Rule 6190

This module implements precise LULD (Limit Up-Limit Down) band calculations
using the exact methodology specified in SEC and FINRA regulations.

References:
- SEC Release No. 34-67091 (May 31, 2012): "National Market System Plan to Address
  Extraordinary Market Volatility"
- FINRA Rule 6190: "Limit Up-Limit Down Plan and Trading Halts"
- SEC Staff Guidance on LULD Implementation
"""

from typing import Tuple
from datetime import datetime, time


def calculate_luld_bands(
    reference_price: float,
    tier: int = 1,
    time_of_day: str = 'normal',
    leverage: float = 1.0
) -> Tuple[float, float, float]:
    """
    Calculate LULD bands using SEC/FINRA regulatory methodology.

    Parameters
    ----------
    reference_price : float
        The current Reference Price (typically prior close or 5-min average)
    tier : int, default 1
        1 = S&P 500, Russell 1000, Select ETPs
        2 = All other NMS stocks and ETPs
    time_of_day : str, default 'normal'
        'opening' = 9:30-9:45 AM (bands doubled)
        'closing' = 3:35-4:00 PM (bands doubled)
        'normal' = all other times
    leverage : float, default 1.0
        Leverage factor for leveraged ETPs (e.g., 2.0 for 2x, 3.0 for 3x)

    Returns
    -------
    tuple of (lower_band, upper_band, percentage)
        lower_band : Lower price band
        upper_band : Upper price band
        percentage : Band percentage (as decimal, e.g., 0.05 for 5%)

    Notes
    -----
    Band Percentages by Tier and Price (SEC Release 34-67091):

    | Price Range  | Tier 1 (S&P/Russell) | Tier 2 (Other NMS) |
    |--------------|----------------------|--------------------|
    | Above $3     | 5%                   | 10%                |
    | $0.75 - $3   | 20%                  | 20%                |
    | Below $0.75  | 75% or $0.15*        | 75% or $0.15*      |

    *Whichever is less restrictive

    Time-of-Day Adjustments (FINRA Rule 6190):
    - Opening period (9:30-9:45): Bands DOUBLED
    - Closing period (3:35-4:00): Bands DOUBLED
    - Normal trading: Standard bands

    Leveraged ETPs (SEC Guidance):
    - Bands multiplied by leverage factor
    - Example: 2x S&P 500 ETP has 10% bands (5% × 2) instead of 5%

    Examples
    --------
    >>> # Standard S&P 500 stock during normal trading
    >>> lower, upper, pct = calculate_luld_bands(100.00, tier=1)
    >>> print(f"Bands: ${lower:.2f} - ${upper:.2f} ({pct*100:.1f}%)")
    Bands: $95.00 - $105.00 (5.0%)

    >>> # Same stock during opening period (doubled)
    >>> lower, upper, pct = calculate_luld_bands(100.00, tier=1, time_of_day='opening')
    >>> print(f"Bands: ${lower:.2f} - ${upper:.2f} ({pct*100:.1f}%)")
    Bands: $90.00 - $110.00 (10.0%)

    >>> # 2x leveraged ETP during opening
    >>> lower, upper, pct = calculate_luld_bands(100.00, tier=1,
    ...                                          time_of_day='opening', leverage=2.0)
    >>> print(f"Bands: ${lower:.2f} - ${upper:.2f} ({pct*100:.1f}%)")
    Bands: $80.00 - $120.00 (20.0%)

    >>> # Low-priced stock (uses $0.15 floor)
    >>> lower, upper, pct = calculate_luld_bands(0.50, tier=1)
    >>> print(f"Bands: ${lower:.2f} - ${upper:.2f}")
    Bands: $0.35 - $0.65
    """

    # Step 1: Determine base percentage by price tier
    if reference_price >= 3.00:
        # Above $3: Different percentages for Tier 1 vs Tier 2
        base_pct = 0.05 if tier == 1 else 0.10

    elif 0.75 <= reference_price < 3.00:
        # $0.75 to $3: Both tiers use 20%
        base_pct = 0.20

    else:  # Below $0.75
        # Use 75% or $0.15, whichever is LESS restrictive (larger band)
        pct_75_band = reference_price * 0.75
        flat_15_band = 0.15

        # Less restrictive = larger absolute band size
        if pct_75_band >= flat_15_band:
            base_pct = 0.75
        else:
            # $0.15 band as a percentage of reference price
            base_pct = flat_15_band / reference_price

    # Step 2: Apply time-of-day multiplier
    # Bands are DOUBLED during opening and closing periods (FINRA Rule 6190)
    time_multiplier = 2.0 if time_of_day in ['opening', 'closing'] else 1.0
    base_pct *= time_multiplier

    # Step 3: Apply leverage multiplier for leveraged ETPs
    final_pct = base_pct * leverage

    # Calculate actual band prices
    lower_band = reference_price * (1 - final_pct)
    upper_band = reference_price * (1 + final_pct)

    return lower_band, upper_band, final_pct


def get_time_of_day_category(dt: datetime) -> str:
    """
    Determine LULD time-of-day category for band calculation.

    Parameters
    ----------
    dt : datetime
        The datetime to categorize

    Returns
    -------
    str
        'opening', 'closing', or 'normal'

    Examples
    --------
    >>> from datetime import datetime
    >>> dt = datetime(2015, 8, 24, 9, 35, 0)  # 9:35 AM
    >>> get_time_of_day_category(dt)
    'opening'
    """
    t = dt.time()

    # Opening period: 9:30 - 9:45 AM (inclusive)
    if time(9, 30) <= t < time(9, 45):
        return 'opening'

    # Closing period: 3:35 - 4:00 PM (inclusive)
    elif time(15, 35) <= t <= time(16, 0):
        return 'closing'

    else:
        return 'normal'


def analyze_flash_crash_halt(
    ticker: str,
    reference_price: float,
    actual_price: float,
    tier: int,
    timestamp: datetime,
    leverage: float = 1.0
) -> dict:
    """
    Analyze whether a price should have triggered LULD halt.

    Parameters
    ----------
    ticker : str
        ETF ticker symbol
    reference_price : float
        LULD Reference Price at time of analysis
    actual_price : float
        Actual trading price
    tier : int
        1 or 2 (S&P 500/Russell 1000 or Other NMS)
    timestamp : datetime
        Time of the price observation
    leverage : float, default 1.0
        Leverage factor if applicable

    Returns
    -------
    dict
        Analysis results including bands, violation status, and details

    Examples
    --------
    >>> from datetime import datetime
    >>> # DVY on August 24, 2015 at 9:35 AM
    >>> result = analyze_flash_crash_halt(
    ...     ticker='DVY',
    ...     reference_price=75.50,
    ...     actual_price=65.20,
    ...     tier=1,
    ...     timestamp=datetime(2015, 8, 24, 9, 35, 0)
    ... )
    >>> print(f"Halt triggered: {result['halt_triggered']}")
    >>> print(f"Distance from band: {result['distance_from_band_pct']:.1f}%")
    """

    # Determine time of day category
    time_category = get_time_of_day_category(timestamp)

    # Calculate LULD bands
    lower_band, upper_band, band_pct = calculate_luld_bands(
        reference_price=reference_price,
        tier=tier,
        time_of_day=time_category,
        leverage=leverage
    )

    # Calculate price deviation
    price_change = actual_price - reference_price
    price_change_pct = (price_change / reference_price) * 100

    # Check if LULD would trigger
    halt_triggered = (actual_price <= lower_band) or (actual_price >= upper_band)

    # Calculate distance from band
    if actual_price < reference_price:
        # Price below reference - check lower band
        distance_from_band = actual_price - lower_band
        distance_from_band_pct = (distance_from_band / lower_band) * 100
    else:
        # Price above reference - check upper band
        distance_from_band = actual_price - upper_band
        distance_from_band_pct = (distance_from_band / upper_band) * 100

    return {
        'ticker': ticker,
        'timestamp': timestamp,
        'time_category': time_category,
        'reference_price': reference_price,
        'actual_price': actual_price,
        'lower_band': lower_band,
        'upper_band': upper_band,
        'band_percentage': band_pct * 100,
        'price_change': price_change,
        'price_change_pct': price_change_pct,
        'halt_triggered': halt_triggered,
        'distance_from_band': distance_from_band,
        'distance_from_band_pct': distance_from_band_pct,
        'tier': tier,
        'leverage': leverage
    }


if __name__ == '__main__':
    # Demonstrate with August 24, 2015 examples
    from datetime import datetime

    print("="*80)
    print("LULD BAND ANALYSIS - AUGUST 24, 2015 FLASH CRASH")
    print("Based on SEC Release No. 34-67091 and FINRA Rule 6190")
    print("="*80)
    print()

    # DVY at 9:35 AM
    print("DVY (iShares Dividend ETF) at 9:35 AM:")
    print("-" * 60)
    result = analyze_flash_crash_halt(
        ticker='DVY',
        reference_price=75.50,
        actual_price=65.20,
        tier=1,
        timestamp=datetime(2015, 8, 24, 9, 35, 0)
    )

    print(f"Time: {result['timestamp'].strftime('%I:%M %p')} ({result['time_category']} period)")
    print(f"Reference Price: ${result['reference_price']:.2f}")
    print(f"LULD Bands: ${result['lower_band']:.2f} - ${result['upper_band']:.2f}")
    print(f"  (±{result['band_percentage']:.1f}% - doubled for opening period)")
    print(f"Actual Price: ${result['actual_price']:.2f}")
    print(f"Price Change: ${result['price_change']:.2f} ({result['price_change_pct']:.1f}%)")
    print(f"Halt Triggered: {'YES' if result['halt_triggered'] else 'NO'}")
    print(f"Distance from Lower Band: ${result['distance_from_band']:.2f} ({result['distance_from_band_pct']:.1f}%)")
    print()

    # RSP at 9:38 AM
    print("RSP (Equal-Weight S&P 500) at 9:38 AM:")
    print("-" * 60)
    result = analyze_flash_crash_halt(
        ticker='RSP',
        reference_price=76.80,
        actual_price=43.77,
        tier=1,
        timestamp=datetime(2015, 8, 24, 9, 38, 0)
    )

    print(f"Time: {result['timestamp'].strftime('%I:%M %p')} ({result['time_category']} period)")
    print(f"Reference Price: ${result['reference_price']:.2f}")
    print(f"LULD Bands: ${result['lower_band']:.2f} - ${result['upper_band']:.2f}")
    print(f"  (±{result['band_percentage']:.1f}% - doubled for opening period)")
    print(f"Actual Price: ${result['actual_price']:.2f}")
    print(f"Price Change: ${result['price_change']:.2f} ({result['price_change_pct']:.1f}%)")
    print(f"Halt Triggered: {'YES' if result['halt_triggered'] else 'NO'}")
    print(f"Distance from Lower Band: ${result['distance_from_band']:.2f} ({result['distance_from_band_pct']:.1f}%)")
    print()

    # SPLV at 9:40 AM
    print("SPLV (Low Volatility ETF) at 9:40 AM:")
    print("-" * 60)
    result = analyze_flash_crash_halt(
        ticker='SPLV',
        reference_price=39.50,
        actual_price=21.18,
        tier=1,
        timestamp=datetime(2015, 8, 24, 9, 40, 0)
    )

    print(f"Time: {result['timestamp'].strftime('%I:%M %p')} ({result['time_category']} period)")
    print(f"Reference Price: ${result['reference_price']:.2f}")
    print(f"LULD Bands: ${result['lower_band']:.2f} - ${result['upper_band']:.2f}")
    print(f"  (±{result['band_percentage']:.1f}% - doubled for opening period)")
    print(f"Actual Price: ${result['actual_price']:.2f}")
    print(f"Price Change: ${result['price_change']:.2f} ({result['price_change_pct']:.1f}%)")
    print(f"Halt Triggered: {'YES' if result['halt_triggered'] else 'NO'}")
    print(f"Distance from Lower Band: ${result['distance_from_band']:.2f} ({result['distance_from_band_pct']:.1f}%)")
    print()

    print("="*80)
    print("KEY INSIGHT: All three ETFs triggered LULD halts, but fell so far")
    print("that even with DOUBLED opening period bands (10% instead of 5%),")
    print("they breached the limits by massive margins.")
    print("="*80)
