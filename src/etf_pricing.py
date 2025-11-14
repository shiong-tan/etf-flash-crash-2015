"""
ETF Pricing Functions

Functions for calculating NAV, iNAV, and arbitrage spreads for ETFs.
Demonstrates the pricing mechanics that failed during the August 24, 2015 flash crash.
"""

from typing import Dict, Union


def calculate_nav(
    holdings: Dict[str, float],
    prices: Dict[str, float],
    shares_outstanding: float,
    cash: float = 0.0,
    liabilities: float = 0.0,
) -> float:
    """
    Calculate Net Asset Value (NAV) for an ETF.

    NAV is calculated once daily at 4:00 PM ET market close using official closing prices.

    Formula:
        NAV = (Sum of holdings value + cash - liabilities) / shares outstanding

    Args:
        holdings: Dict mapping ticker to number of shares held
                  Example: {"AAPL": 1000, "MSFT": 2000}
        prices: Dict mapping ticker to current market price
                Example: {"AAPL": 150.0, "MSFT": 300.0}
        shares_outstanding: Total ETF shares outstanding
        cash: Cash holdings in fund
        liabilities: Fund liabilities

    Returns:
        NAV per share

    Example:
        >>> holdings = {"AAPL": 100, "MSFT": 200}
        >>> prices = {"AAPL": 150.0, "MSFT": 300.0}
        >>> calculate_nav(holdings, prices, 10000)
        7.5
    """
    if shares_outstanding <= 0:
        raise ValueError("shares_outstanding must be positive")

    if not holdings:
        raise ValueError("holdings dictionary cannot be empty")

    # Validate that all required prices are available
    missing_prices = set(holdings.keys()) - set(prices.keys())
    if missing_prices:
        raise ValueError(f"Missing prices for tickers: {missing_prices}")

    # Validate non-negative values
    if any(price < 0 for price in prices.values()):
        raise ValueError("All prices must be non-negative")
    if any(shares < 0 for shares in holdings.values()):
        raise ValueError("All holdings must be non-negative")

    # Calculate total value of holdings
    total_value = sum(
        holdings[ticker] * prices[ticker]
        for ticker in holdings.keys()
    )

    # Add cash and subtract liabilities
    net_assets = total_value + cash - liabilities

    # Divide by shares outstanding
    nav = net_assets / shares_outstanding

    return nav


def calculate_inav(
    holdings: Dict[str, float],
    current_prices: Dict[str, float],
    creation_unit_size: int = 50000,
    cash_per_unit: float = 0.0,
) -> float:
    """
    Calculate Intraday Indicative Value (iNAV) for an ETF.

    iNAV is updated every 15 seconds during trading hours using last available prices.
    On August 24, 2015, iNAV became unreliable when underlying stocks were halted
    and "last available" prices were stale.

    Formula:
        iNAV = (Sum of basket value + cash) / creation unit size

    Args:
        holdings: Dict mapping ticker to shares in one creation unit
                  Example: {"AAPL": 10, "MSFT": 20} for one creation unit
        current_prices: Dict mapping ticker to current/last available price
        creation_unit_size: Number of ETF shares in one creation unit (typically 25k-100k)
        cash_per_unit: Cash component per creation unit

    Returns:
        iNAV per ETF share

    Example:
        >>> holdings = {"AAPL": 10, "MSFT": 20}
        >>> current_prices = {"AAPL": 150.0, "MSFT": 300.0}
        >>> calculate_inav(holdings, current_prices, 50000)
        0.15

    Note:
        On Aug 24, 2015, "current_prices" contained stale values for halted stocks,
        making iNAV unreliable for fair value assessment.
    """
    if creation_unit_size <= 0:
        raise ValueError("creation_unit_size must be positive")

    if not holdings:
        raise ValueError("holdings dictionary cannot be empty")

    # Validate that all required prices are available
    missing_prices = set(holdings.keys()) - set(current_prices.keys())
    if missing_prices:
        raise ValueError(f"Missing prices for tickers: {missing_prices}")

    # Calculate total basket value
    basket_value = sum(
        holdings[ticker] * current_prices[ticker]
        for ticker in holdings.keys()
    )

    # Add cash component
    total_value = basket_value + cash_per_unit

    # Divide by creation unit size to get per-share value
    inav = total_value / creation_unit_size

    return inav


def arbitrage_spread(
    etf_price: float,
    inav: float,
    transaction_costs: float = 0.001,
) -> Dict[str, Union[float, bool]]:
    """
    Calculate arbitrage spread between ETF price and iNAV.

    Determines whether creation or redemption arbitrage is profitable after
    transaction costs. On August 24, apparent arbitrage opportunities were
    actually unhedgeable speculation due to stale iNAV values.

    Args:
        etf_price: Current market price of ETF
        inav: Intraday indicative value
        transaction_costs: Transaction costs as fraction (e.g., 0.001 = 10 bps)

    Returns:
        Dict containing:
            - spread_pct: Percentage spread (positive = premium, negative = discount)
            - spread_bps: Spread in basis points
            - profitable_creation: Whether creation arbitrage is profitable
            - profitable_redemption: Whether redemption arbitrage is profitable
            - action: Recommended action ("create", "redeem", or "none")

    Example:
        >>> arbitrage_spread(100.0, 101.0, 0.001)
        {'spread_pct': 1.0, 'spread_bps': 100.0, 'profitable_creation': False,
         'profitable_redemption': True, 'action': 'redeem'}
    """
    if inav <= 0 or etf_price <= 0:
        raise ValueError("Prices must be positive")

    # Calculate spread
    spread = etf_price - inav
    spread_pct = (spread / inav) * 100
    spread_bps = spread_pct * 100

    # Determine if arbitrage is profitable after costs
    # Creation: profitable if ETF trades at premium > transaction costs
    profitable_creation = spread_pct > (transaction_costs * 100)

    # Redemption: profitable if ETF trades at discount > transaction costs
    profitable_redemption = spread_pct < -(transaction_costs * 100)

    # Determine recommended action
    if profitable_creation:
        action = "create"
    elif profitable_redemption:
        action = "redeem"
    else:
        action = "none"

    return {
        "spread_pct": spread_pct,
        "spread_bps": spread_bps,
        "profitable_creation": profitable_creation,
        "profitable_redemption": profitable_redemption,
        "action": action,
    }


def creation_profit(
    etf_price: float,
    basket_value: float,
    creation_unit_size: int,
    transaction_costs_bps: float = 25.0,
) -> Dict[str, float]:
    """
    Calculate profit from ETF creation arbitrage.

    Creation process:
    1. Buy underlying basket of securities
    2. Short ETF shares as hedge
    3. Deliver basket to issuer, receive ETF shares
    4. Cover short with received shares
    5. Profit = premium spread - transaction costs

    Args:
        etf_price: Current market price of ETF per share
        basket_value: Total value of underlying basket (for one creation unit)
        creation_unit_size: Number of ETF shares in creation unit
        transaction_costs_bps: Transaction costs in basis points (default 25)

    Returns:
        Dict containing:
            - basket_cost: Cost to buy underlying basket
            - etf_value: Value of ETF shares received
            - transaction_costs: Total transaction costs
            - gross_profit: Profit before costs
            - net_profit: Profit after costs
            - return_pct: Return percentage

    Example:
        >>> creation_profit(100.50, 5000000, 50000, 25.0)
        {'basket_cost': 5000000.0, 'etf_value': 5025000.0,
         'transaction_costs': 12562.5, 'gross_profit': 25000.0,
         'net_profit': 12437.5, 'return_pct': 0.249}
    """
    if creation_unit_size <= 0:
        raise ValueError("creation_unit_size must be positive")

    # Cost to buy underlying basket
    basket_cost = basket_value

    # Value of ETF shares received
    etf_value = etf_price * creation_unit_size

    # Calculate transaction costs
    transaction_costs = basket_value * (transaction_costs_bps / 10000)

    # Calculate profits
    gross_profit = etf_value - basket_cost
    net_profit = gross_profit - transaction_costs
    return_pct = (net_profit / basket_cost) * 100

    return {
        "basket_cost": basket_cost,
        "etf_value": etf_value,
        "transaction_costs": transaction_costs,
        "gross_profit": gross_profit,
        "net_profit": net_profit,
        "return_pct": return_pct,
    }


def redemption_profit(
    etf_price: float,
    basket_value: float,
    creation_unit_size: int,
    transaction_costs_bps: float = 25.0,
) -> Dict[str, float]:
    """
    Calculate profit from ETF redemption arbitrage.

    Redemption process:
    1. Buy undervalued ETF shares
    2. Short underlying basket as hedge
    3. Deliver ETF shares to issuer, receive basket
    4. Cover short with received basket
    5. Profit = discount spread - transaction costs

    Args:
        etf_price: Current market price of ETF per share
        basket_value: Total value of underlying basket (for one creation unit)
        creation_unit_size: Number of ETF shares in creation unit
        transaction_costs_bps: Transaction costs in basis points (default 25)

    Returns:
        Dict containing:
            - etf_cost: Cost to buy ETF shares
            - basket_value_received: Value of basket received
            - transaction_costs: Total transaction costs
            - gross_profit: Profit before costs
            - net_profit: Profit after costs
            - return_pct: Return percentage

    Example:
        >>> redemption_profit(99.50, 5000000, 50000, 25.0)
        {'etf_cost': 4975000.0, 'basket_value_received': 5000000.0,
         'transaction_costs': 12437.5, 'gross_profit': 25000.0,
         'net_profit': 12562.5, 'return_pct': 0.253}
    """
    if creation_unit_size <= 0:
        raise ValueError("creation_unit_size must be positive")

    # Cost to buy ETF shares
    etf_cost = etf_price * creation_unit_size

    # Value of basket received from redemption
    basket_value_received = basket_value

    # Calculate transaction costs
    transaction_costs = etf_cost * (transaction_costs_bps / 10000)

    # Calculate profits
    gross_profit = basket_value_received - etf_cost
    net_profit = gross_profit - transaction_costs
    return_pct = (net_profit / etf_cost) * 100

    return {
        "etf_cost": etf_cost,
        "basket_value_received": basket_value_received,
        "transaction_costs": transaction_costs,
        "gross_profit": gross_profit,
        "net_profit": net_profit,
        "return_pct": return_pct,
    }


def simulate_stale_inav(
    holdings: Dict[str, float],
    current_prices: Dict[str, float],
    stale_prices: Dict[str, float],
    halted_tickers: list,
    creation_unit_size: int = 50000,
) -> Dict[str, float]:
    """
    Simulate iNAV calculation with stale prices for halted stocks.

    Demonstrates the August 24, 2015 problem: iNAV used stale prices for
    halted stocks, making displayed "fair value" unreliable.

    Args:
        holdings: Dict mapping ticker to shares in creation unit
        current_prices: Dict with actual current prices (for opened stocks)
        stale_prices: Dict with stale prices (15-30 min old)
        halted_tickers: List of tickers that are halted
        creation_unit_size: Number of ETF shares in creation unit

    Returns:
        Dict containing:
            - inav_with_stale: iNAV calculated with stale prices for halted stocks
            - inav_true: True iNAV if all stocks had current prices
            - error_pct: Percentage error in iNAV due to stale prices
            - num_halted: Number of halted components
            - pct_halted: Percentage of components halted

    Example:
        Demonstrates that iNAV showing $71 might be based on stale data,
        making RSP at $50 vs $71 iNAV not a reliable arbitrage signal.
    """
    # Calculate iNAV using stale prices for halted stocks
    prices_with_stale = {}
    for ticker in holdings.keys():
        if ticker in halted_tickers:
            prices_with_stale[ticker] = stale_prices.get(ticker, 0)
        else:
            prices_with_stale[ticker] = current_prices.get(ticker, 0)

    inav_with_stale = calculate_inav(holdings, prices_with_stale, creation_unit_size)

    # Calculate true iNAV if all had current prices
    inav_true = calculate_inav(holdings, current_prices, creation_unit_size)

    # Calculate error
    error = inav_with_stale - inav_true
    error_pct = (error / inav_true) * 100 if inav_true != 0 else 0

    # Calculate statistics
    num_halted = len(halted_tickers)
    pct_halted = (num_halted / len(holdings)) * 100 if holdings else 0

    return {
        "inav_with_stale": inav_with_stale,
        "inav_true": inav_true,
        "error_pct": error_pct,
        "num_halted": num_halted,
        "pct_halted": pct_halted,
    }
