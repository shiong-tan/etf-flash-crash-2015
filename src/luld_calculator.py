"""
LULD Band Calculator - Regulatory Methodology
Based on: SEC Release No. 34-67091 and FINRA Rule 6190

This module implements precise LULD (Limit Up-Limit Down) band calculations
using the exact methodology specified in SEC and FINRA regulations.

SCOPE AND LIMITATIONS:
This calculator provides STATIC band calculation for a given Reference Price.
It does NOT implement:
- Reference Price calculation and updates (1% trigger, 5-min average, 30-sec hold)
- Limit State mechanism (15-second timer before halt)
- Reopening auction logic
- Exchange-specific reopening collars

For complete LULD simulation including dynamic behavior, additional components
are required. See guide/03-deep-dive/luld-failure-modes.md for details.

References:
- SEC Release No. 34-67091 (May 31, 2012): "National Market System Plan to Address
  Extraordinary Market Volatility"
- FINRA Rule 6190: "Limit Up-Limit Down Plan and Trading Halts"
- SEC Staff Guidance on LULD Implementation
"""

from typing import Tuple, Literal
from datetime import datetime, time

# Band Configuration Constants (SEC Release 34-67091)
PRICE_THRESHOLD_HIGH = 3.00  # Above this: tier-specific bands
PRICE_THRESHOLD_LOW = 0.75   # Below this: special penny stock rules
FLAT_BAND_FLOOR = 0.15       # Flat band for very low prices

# Band Percentages by Tier and Price Range
TIER1_HIGH_BAND_PCT = 0.05   # Tier 1 above $3: 5%
TIER2_HIGH_BAND_PCT = 0.10   # Tier 2 above $3: 10%
MID_PRICE_BAND_PCT = 0.20    # Both tiers $0.75-$3: 20%
LOW_PRICE_BAND_PCT = 0.75    # Both tiers below $0.75: 75% (or $0.15)

# Time-of-Day Multipliers (FINRA Rule 6190)
TIME_MULTIPLIER_OPENING = 2.0  # 9:30-9:45 AM: bands doubled
TIME_MULTIPLIER_CLOSING = 2.0  # 3:35-4:00 PM: bands doubled
TIME_MULTIPLIER_NORMAL = 1.0   # All other times: standard bands

# Trading Hours
MARKET_OPEN = time(9, 30)      # 9:30 AM
OPENING_END = time(9, 45)      # 9:45 AM
CLOSING_START = time(15, 35)   # 3:35 PM
MARKET_CLOSE = time(16, 0)     # 4:00 PM


def calculate_luld_bands(
    reference_price: float,
    tier: Literal[1, 2] = 1,
    time_of_day: Literal['opening', 'closing', 'normal'] = 'normal',
    leverage: float = 1.0
) -> Tuple[float, float, float]:
    """
    Calculate LULD bands using SEC/FINRA regulatory methodology.

    Parameters
    ----------
    reference_price : float
        The current Reference Price (typically prior close or 5-min average)
        Must be positive.
    tier : Literal[1, 2], default 1
        1 = S&P 500, Russell 1000, Select ETPs
        2 = All other NMS stocks and ETPs
    time_of_day : Literal['opening', 'closing', 'normal'], default 'normal'
        'opening' = 9:30-9:45 AM (bands doubled)
        'closing' = 3:35-4:00 PM (bands doubled)
        'normal' = all other times
    leverage : float, default 1.0
        Leverage factor for leveraged ETPs (e.g., 2.0 for 2x, 3.0 for 3x)
        Must be positive and typically <= 3.0

    Returns
    -------
    tuple of (lower_band, upper_band, percentage)
        lower_band : Lower price band (always >= 0.00)
        upper_band : Upper price band
        percentage : Band percentage (as decimal, e.g., 0.05 for 5%)

    Raises
    ------
    ValueError
        If any input parameter is invalid

    Notes
    -----
    Band Percentages by Tier and Price (SEC Release 34-67091):

    | Price Range  | Tier 1 (S&P/Russell) | Tier 2 (Other NMS) |
    |--------------|----------------------|--------------------|
    | Above $3     | 5%                   | 10%                |
    | $0.75 - $3   | 20%                  | 20%                |
    | Below $0.75  | 75% or $0.15*        | 75% or $0.15*      |

    *Whichever is less restrictive

    INTERPRETATION NOTE: "Less restrictive" for prices below $0.75 is ambiguous
    in the specification. This implementation uses "larger absolute band width"
    as the interpretation, but applies a non-negativity constraint to prevent
    mathematically impossible negative prices.

    At very low prices (< $0.20), the $0.15 flat band can exceed the reference
    price itself. In these cases, we floor the lower band at $0.00 to maintain
    physical constraints (price >= 0).

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

    >>> # Low-priced stock (uses 75% band)
    >>> lower, upper, pct = calculate_luld_bands(0.50, tier=1)
    >>> print(f"Bands: ${lower:.2f} - ${upper:.2f}")
    Bands: $0.12 - $0.88

    >>> # Very low-priced stock (uses $0.15 flat band, floored at $0.00)
    >>> lower, upper, pct = calculate_luld_bands(0.10, tier=1)
    >>> print(f"Bands: ${lower:.2f} - ${upper:.2f}")
    Bands: $0.00 - $0.25
    """
    # Input validation
    if reference_price <= 0:
        raise ValueError(f"reference_price must be positive, got {reference_price}")

    if tier not in [1, 2]:
        raise ValueError(f"tier must be 1 or 2, got {tier}")

    if time_of_day not in ['opening', 'closing', 'normal']:
        raise ValueError(f"time_of_day must be 'opening', 'closing', or 'normal', got '{time_of_day}'")

    if leverage <= 0 or leverage > 3:
        raise ValueError(f"leverage must be in (0, 3], got {leverage}")

    # Step 1: Determine base percentage by price tier
    if reference_price >= PRICE_THRESHOLD_HIGH:
        # Above $3: Different percentages for Tier 1 vs Tier 2
        base_pct = TIER1_HIGH_BAND_PCT if tier == 1 else TIER2_HIGH_BAND_PCT

    elif PRICE_THRESHOLD_LOW <= reference_price < PRICE_THRESHOLD_HIGH:
        # $0.75 to $3: Both tiers use 20%
        base_pct = MID_PRICE_BAND_PCT

    else:  # Below $0.75
        # Use 75% or $0.15, whichever is LESS restrictive (larger band)
        #
        # INTERPRETATION NOTE: "Less restrictive" is ambiguous in specification.
        # Current implementation uses "larger absolute band width" interpretation,
        # with non-negativity constraint to prevent negative lower bands.
        #
        # See: SEC Release No. 34-67091 Section IV.B.3 for clarification.
        pct_75_band = reference_price * LOW_PRICE_BAND_PCT
        flat_15_band = FLAT_BAND_FLOOR

        # Less restrictive = larger absolute band size
        if pct_75_band >= flat_15_band:
            base_pct = LOW_PRICE_BAND_PCT
        else:
            # $0.15 band as a percentage of reference price
            base_pct = flat_15_band / reference_price

    # Step 2: Apply time-of-day multiplier
    # Bands are DOUBLED during opening and closing periods (FINRA Rule 6190)
    if time_of_day == 'opening':
        time_multiplier = TIME_MULTIPLIER_OPENING
    elif time_of_day == 'closing':
        time_multiplier = TIME_MULTIPLIER_CLOSING
    else:
        time_multiplier = TIME_MULTIPLIER_NORMAL

    base_pct *= time_multiplier

    # Step 3: Apply leverage multiplier for leveraged ETPs
    final_pct = base_pct * leverage

    # Calculate actual band prices
    lower_band = reference_price * (1 - final_pct)
    upper_band = reference_price * (1 + final_pct)

    # CRITICAL FIX: Apply non-negativity constraint
    # Prices cannot be negative in financial markets
    lower_band = max(0.00, lower_band)

    return lower_band, upper_band, final_pct


def get_time_of_day_category(dt: datetime) -> Literal['opening', 'closing', 'normal']:
    """
    Determine LULD time-of-day category for band calculation.

    Parameters
    ----------
    dt : datetime
        The datetime to categorize

    Returns
    -------
    Literal['opening', 'closing', 'normal']
        'opening' : 9:30-9:45 AM (exclusive end)
        'closing' : 3:35-4:00 PM (exclusive end)
        'normal'  : All other times during trading hours

    Notes
    -----
    - Opening period: 9:30:00 - 9:44:59.999...
    - Normal period: 9:45:00 - 15:34:59.999...
    - Closing period: 15:35:00 - 15:59:59.999...
    - Market closes at 16:00:00 (4:00 PM exact) - no trades occur at this time

    Examples
    --------
    >>> from datetime import datetime
    >>> dt = datetime(2015, 8, 24, 9, 35, 0)  # 9:35 AM
    >>> get_time_of_day_category(dt)
    'opening'

    >>> dt = datetime(2015, 8, 24, 9, 45, 0)  # 9:45 AM
    >>> get_time_of_day_category(dt)
    'normal'

    >>> dt = datetime(2015, 8, 24, 15, 35, 0)  # 3:35 PM
    >>> get_time_of_day_category(dt)
    'closing'
    """
    t = dt.time()

    # Opening period: 9:30 - 9:45 AM (exclusive end)
    if MARKET_OPEN <= t < OPENING_END:
        return 'opening'

    # Closing period: 3:35 - 4:00 PM (exclusive end)
    # FIX: Changed from <= to < to exclude exactly 4:00 PM (market closed)
    elif CLOSING_START <= t < MARKET_CLOSE:
        return 'closing'

    else:
        return 'normal'


def analyze_flash_crash_halt(
    ticker: str,
    reference_price: float,
    actual_price: float,
    tier: Literal[1, 2],
    timestamp: datetime,
    leverage: float = 1.0
) -> dict:
    """
    Analyze whether a price should have triggered LULD halt.

    NOTE: This function performs STATIC analysis assuming the Reference Price
    is given. It does NOT implement the dynamic Reference Price calculation
    or the 15-second Limit State timer required for complete LULD simulation.

    For complete understanding of LULD dynamics, see:
    - guide/03-deep-dive/luld-failure-modes.md
    - guide/04-market-maker-perspective/luld-from-mm-view.md

    Parameters
    ----------
    ticker : str
        ETF ticker symbol
    reference_price : float
        LULD Reference Price at time of analysis
    actual_price : float
        Actual trading price
    tier : Literal[1, 2]
        1 = S&P 500/Russell 1000, 2 = Other NMS
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
    # NOTE: This is simplified - actual LULD requires 15-second Limit State
    halt_triggered = (actual_price <= lower_band) or (actual_price >= upper_band)

    # Calculate distance from band
    if actual_price < reference_price:
        # Price below reference - check lower band
        distance_from_band = actual_price - lower_band
        if lower_band > 0:
            distance_from_band_pct = (distance_from_band / lower_band) * 100
        else:
            # Handle edge case where lower_band = 0
            distance_from_band_pct = -100.0 if distance_from_band < 0 else 0.0
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
