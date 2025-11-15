"""
Data loading and preprocessing for August 24, 2015 analysis.
Handles historical data, synthetic data generation, and data validation.

This module provides utilities for loading ETF price data, halt information,
futures data, and ETF holdings for analyzing the August 24, 2015 flash crash.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings


# Data directory structure
DATA_DIR = Path(__file__).parent.parent / 'assets' / 'data'


class Aug24DataLoader:
    """
    Load and validate data for August 24, 2015 analysis.

    This class provides methods to load ETF prices, halt logs, futures data,
    and ETF holdings. When historical data is unavailable, it generates
    realistic synthetic data based on known facts about the flash crash.

    Data sources:
    1. Historical ETF prices (minute-level if available)
    2. S&P 500 futures data
    3. Halt log (from SEC reports)
    4. ETF holdings data
    5. Synthetic/estimated data where real data unavailable

    Attributes:
        data_dir: Path to data directory

    Example:
        >>> loader = Aug24DataLoader()
        >>> rsp_data = loader.load_etf_prices('RSP')
        >>> halts = loader.load_halt_log()
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize data loader.

        Args:
            data_dir: Optional custom data directory path.
                     Defaults to assets/data/
        """
        self.data_dir = data_dir or DATA_DIR
        self._validate_data_directory()

    def _validate_data_directory(self):
        """Check if required data files exist."""
        if not self.data_dir.exists():
            warnings.warn(
                f"Data directory not found: {self.data_dir}. "
                "Creating directory..."
            )
            self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_etf_prices(self,
                       symbol: str,
                       data_type: str = 'minute') -> pd.DataFrame:
        """
        Load ETF price data.

        Tries to load from existing aug24_price_data.csv file. If not found
        or symbol not in file, generates synthetic data based on known facts.

        Args:
            symbol: ETF ticker (e.g., 'RSP', 'SPY', 'IVV')
            data_type: Data frequency - 'minute', 'tick', or 'daily'
                      (currently only 'minute' supported)

        Returns:
            DataFrame with columns:
                - timestamp (index): Datetime of observation
                - price: Last trade price
                - volume: Trading volume
                - inav: Indicative NAV (for ETFs)
                - bid: Best bid price (if available)
                - ask: Best ask price (if available)
                - spread_bps: Bid-ask spread in basis points (if available)

        Example:
            >>> loader = Aug24DataLoader()
            >>> rsp = loader.load_etf_prices('RSP')
            >>> print(rsp.head())
        """
        # Try loading from aug24_price_data.csv
        main_file = self.data_dir / 'aug24_price_data.csv'

        if main_file.exists():
            try:
                df = pd.read_csv(main_file)
                df['timestamp'] = pd.to_datetime(df['timestamp'])

                # Filter to requested symbol
                df_symbol = df[df['ticker'] == symbol].copy()

                if len(df_symbol) > 0:
                    # Process the data
                    df_symbol = df_symbol.set_index('timestamp').sort_index()

                    # Handle HALTED prices (set to NaN)
                    df_symbol.loc[df_symbol['price'] == 'HALTED', 'price'] = np.nan

                    # Convert price columns to numeric
                    numeric_cols = ['price', 'volume']
                    for col in numeric_cols:
                        if col in df_symbol.columns:
                            df_symbol[col] = pd.to_numeric(df_symbol[col], errors='coerce')

                    # Add optional columns if not present
                    for col in ['bid', 'ask', 'spread_bps', 'inav']:
                        if col not in df_symbol.columns:
                            df_symbol[col] = np.nan

                    return df_symbol[['price', 'volume', 'inav', 'bid', 'ask', 'spread_bps']]

            except Exception as e:
                warnings.warn(
                    f"Error loading data from {main_file}: {e}. "
                    "Generating synthetic data."
                )

        # Fallback: Try individual file
        filename = self.data_dir / f'{symbol}_{data_type}_aug24.csv'

        if filename.exists():
            try:
                df = pd.read_csv(filename)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.set_index('timestamp').sort_index()
                return df
            except Exception as e:
                warnings.warn(f"Error loading {filename}: {e}")

        # Last resort: Generate synthetic data
        warnings.warn(
            f"Historical data not found for {symbol}. "
            "Generating synthetic data based on known facts."
        )
        return self._generate_synthetic_etf_data(symbol)

    def load_halt_log(self) -> pd.DataFrame:
        """
        Load complete halt log for August 24, 2015.

        Based on SEC DERA research note data. Loads from luld_halts.csv
        if available, otherwise generates synthetic halt data.

        Returns:
            DataFrame with columns:
                - ticker: Security symbol
                - type: 'ETF' or 'Stock'
                - halt_start: Trading halt start time
                - halt_end: Trading halt end time
                - duration_sec: Halt duration in seconds
                - price_before: Price before halt
                - price_after: Price after halt resumed
                - reference_price: LULD reference price
                - band_pct: LULD band percentage
                - trigger_reason: Reason for halt
                - halt_number: Sequential halt number for this security

        Example:
            >>> loader = Aug24DataLoader()
            >>> halts = loader.load_halt_log()
            >>> rsp_halts = halts[halts['ticker'] == 'RSP']
            >>> print(f"RSP had {len(rsp_halts)} halts")
        """
        filename = self.data_dir / 'luld_halts.csv'

        if filename.exists():
            try:
                df = pd.read_csv(filename)
                df['halt_start'] = pd.to_datetime(df['halt_start'])
                df['halt_end'] = pd.to_datetime(df['halt_end'])
                return df
            except Exception as e:
                warnings.warn(f"Error loading halt log: {e}")

        # Generate synthetic data
        warnings.warn("Halt log not found. Generating synthetic halt data.")
        return self._generate_synthetic_halt_data()

    def load_sp500_futures(self) -> pd.DataFrame:
        """
        Load S&P 500 futures data for August 24, 2015.

        Loads E-mini S&P 500 futures prices during the flash crash period.

        Returns:
            DataFrame with minute-level futures prices:
                - timestamp (index): Time of observation
                - price: Futures price
                - volume: Trading volume

        Example:
            >>> loader = Aug24DataLoader()
            >>> futures = loader.load_sp500_futures()
            >>> min_price = futures['price'].min()
            >>> print(f"Futures low: ${min_price:.2f}")
        """
        filename = self.data_dir / 'sp500_futures_minute.csv'

        if filename.exists():
            try:
                df = pd.read_csv(filename)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.set_index('timestamp').sort_index()
                return df
            except Exception as e:
                warnings.warn(f"Error loading futures data: {e}")

        warnings.warn("Futures data not found. Generating synthetic data.")
        return self._generate_synthetic_futures_data()

    def load_etf_holdings(self,
                         symbol: str,
                         date: str = '2015-08-24') -> Dict[str, float]:
        """
        Load ETF holdings (constituent stocks and weights).

        Returns the basket composition for creation/redemption.

        Args:
            symbol: ETF ticker
            date: Date for holdings (default: 2015-08-24)

        Returns:
            Dictionary mapping ticker to number of shares per creation unit:
                {ticker: shares}

        Example:
            >>> loader = Aug24DataLoader()
            >>> holdings = loader.load_etf_holdings('RSP')
            >>> print(f"RSP holds {len(holdings)} stocks")
        """
        filename = self.data_dir / 'holdings' / f'{symbol}_holdings.csv'

        if filename.exists():
            try:
                df = pd.read_csv(filename)
                # Expect columns: ticker, shares (or ticker, weight)
                if 'shares' in df.columns:
                    return dict(zip(df['ticker'], df['shares']))
                elif 'weight' in df.columns:
                    return dict(zip(df['ticker'], df['weight']))
                else:
                    warnings.warn(f"Unexpected format in {filename}")
            except Exception as e:
                warnings.warn(f"Error loading holdings: {e}")

        warnings.warn(f"Holdings not found for {symbol}. Generating synthetic.")
        return self._generate_synthetic_holdings(symbol)

    # Synthetic data generation methods

    def _generate_synthetic_etf_data(self, symbol: str) -> pd.DataFrame:
        """
        Generate realistic synthetic ETF price data based on known facts.

        Uses:
        - Known opening and low prices from SEC reports
        - Known number and timing of halts
        - Realistic intraday recovery patterns

        Args:
            symbol: ETF ticker

        Returns:
            DataFrame with synthetic minute-level data
        """
        # Known facts for major ETFs
        if symbol == 'RSP':
            # Guggenheim S&P 500 Equal Weight ETF
            # Source: SEC Staff Report
            data_points = [
                ('2015-08-24 09:30:00', 76.15, 71.23),  # Open (price, inav)
                ('2015-08-24 09:31:30', 68.50, 71.23),  # First drop
                ('2015-08-24 09:33:00', 58.75, 71.23),  # Second drop
                ('2015-08-24 09:35:00', np.nan, 71.23),  # HALTED
                ('2015-08-24 09:40:00', 55.80, 71.50),  # Resume after halt
                ('2015-08-24 09:42:00', 48.20, 71.50),  # Continued drop
                ('2015-08-24 09:44:30', 43.77, 71.50),  # LOWEST POINT
                ('2015-08-24 09:47:00', 52.00, 71.80),  # Start recovery
                ('2015-08-24 09:55:00', 63.00, 72.00),  # Recovery continues
                ('2015-08-24 10:05:00', 68.50, 72.20),  # Approaching fair value
                ('2015-08-24 10:30:00', 70.80, 72.30),  # Stabilizing
                ('2015-08-24 11:00:00', 71.20, 72.40),  # Nearly recovered
                ('2015-08-24 16:00:00', 71.40, 72.50),  # Close
            ]

        elif symbol == 'IUSV':
            # iShares Core S&P U.S. Value ETF
            # Famous for stop-loss execution at $87.32
            data_points = [
                ('2015-08-24 09:30:00', 108.69, 107.50),
                ('2015-08-24 09:35:00', 102.30, 107.50),
                ('2015-08-24 09:40:00', 95.40, 107.80),
                ('2015-08-24 09:42:00', 87.32, 108.00),  # Stop execution
                ('2015-08-24 09:50:00', 98.50, 108.20),
                ('2015-08-24 10:15:00', 105.00, 108.50),
                ('2015-08-24 16:00:00', 107.20, 108.60),
            ]

        elif symbol == 'SPY':
            # SPDR S&P 500 ETF (largest, most liquid)
            data_points = [
                ('2015-08-24 09:30:00', 199.12, 195.80),
                ('2015-08-24 09:35:00', 195.50, 195.80),
                ('2015-08-24 09:40:00', 192.30, 196.00),
                ('2015-08-24 09:45:00', 191.20, 196.20),  # Low
                ('2015-08-24 10:00:00', 194.50, 196.50),
                ('2015-08-24 11:00:00', 197.80, 197.00),
                ('2015-08-24 16:00:00', 198.50, 197.20),
            ]

        elif symbol == 'IVV':
            # iShares Core S&P 500 ETF
            # Traded at premium vs SPY during crash
            data_points = [
                ('2015-08-24 09:30:00', 202.45, 195.80),
                ('2015-08-24 09:35:00', 198.20, 195.80),
                ('2015-08-24 09:40:00', np.nan, 196.00),  # HALTED
                ('2015-08-24 09:50:00', 199.50, 196.50),
                ('2015-08-24 11:00:00', 201.00, 197.00),
                ('2015-08-24 16:00:00', 201.80, 197.20),
            ]

        else:
            # Generic ETF crash pattern
            data_points = [
                ('2015-08-24 09:30:00', 100.00, 98.00),
                ('2015-08-24 09:40:00', 85.00, 98.20),
                ('2015-08-24 09:45:00', 80.00, 98.50),
                ('2015-08-24 10:00:00', 88.00, 98.80),
                ('2015-08-24 11:00:00', 95.00, 99.00),
                ('2015-08-24 16:00:00', 97.50, 99.20),
            ]

        # Create minute-level timeline
        timestamps = pd.date_range(
            '2015-08-24 09:30:00',
            '2015-08-24 16:00:00',
            freq='1min'
        )

        # Interpolate prices between known points
        data_df = pd.DataFrame(data_points, columns=['time', 'price', 'inav'])
        data_df['time'] = pd.to_datetime(data_df['time'])
        data_df = data_df.set_index('time')

        # Reindex to minute frequency with forward fill
        data_df = data_df.reindex(timestamps, method='ffill')

        # Add synthetic volume (higher during stress)
        base_volume = 5000
        stress_multiplier = np.where(
            (data_df.index >= '2015-08-24 09:30:00') &
            (data_df.index <= '2015-08-24 10:00:00'),
            5.0,  # 5x volume during stress
            1.0
        )
        data_df['volume'] = (base_volume * stress_multiplier *
                            np.random.uniform(0.5, 1.5, len(data_df))).astype(int)

        # Add bid/ask (wider during stress)
        mid_price = data_df['price'].fillna(method='ffill').fillna(method='bfill')
        normal_spread = mid_price * 0.0001  # 1 bp normal
        stress_spread = mid_price * 0.02    # 200 bps during stress

        is_stressed = (
            (data_df.index >= '2015-08-24 09:30:00') &
            (data_df.index <= '2015-08-24 10:00:00')
        )
        spread = np.where(is_stressed, stress_spread, normal_spread)

        data_df['bid'] = mid_price - spread / 2
        data_df['ask'] = mid_price + spread / 2
        data_df['spread_bps'] = (spread / mid_price) * 10000

        # Reset index to make timestamp a column
        data_df = data_df.reset_index()
        data_df.columns = ['timestamp'] + list(data_df.columns[1:])
        data_df = data_df.set_index('timestamp')

        return data_df

    def _generate_synthetic_halt_data(self) -> pd.DataFrame:
        """
        Generate realistic halt log based on SEC data.

        Known facts:
        - 1,278 halts across 471 securities
        - 80% were ETFs
        - RSP had 10 halts
        - Most halts were 5 minutes (LULD standard)

        Returns:
            DataFrame with halt information
        """
        etfs = ['RSP', 'SPY', 'IVV', 'SPLV', 'DVY', 'VTI', 'IUSV', 'VTV']

        halts = []

        for etf in etfs:
            # RSP had the most halts (10)
            if etf == 'RSP':
                num_halts = 10
            elif etf in ['IUSV', 'DVY', 'SPLV']:
                num_halts = np.random.randint(5, 8)
            else:
                num_halts = np.random.randint(2, 5)

            # Start halts at market open
            halt_time = pd.Timestamp('2015-08-24 09:31:00')
            reference_price = 100.0 if etf != 'RSP' else 76.15

            for i in range(num_halts):
                # Each halt is ~5 minutes
                halt_start = halt_time
                halt_end = halt_time + pd.Timedelta(minutes=5)

                # Price drops before each halt
                price_before = reference_price * (1 - 0.05)  # -5% triggers LULD
                price_after = price_before * 0.95  # Continues to drop

                halts.append({
                    'ticker': etf,
                    'type': 'ETF',
                    'halt_start': halt_start,
                    'halt_end': halt_end,
                    'duration_sec': 300,
                    'price_before': price_before,
                    'price_after': price_after,
                    'reference_price': reference_price,
                    'band_pct': 5.0,
                    'trigger_reason': 'LULD_lower_band',
                    'halt_number': i + 1
                })

                # Next halt 1-2 minutes after previous ends
                halt_time = halt_end + pd.Timedelta(minutes=np.random.randint(1, 3))
                reference_price = price_after  # Update reference

        return pd.DataFrame(halts)

    def _generate_synthetic_futures_data(self) -> pd.DataFrame:
        """
        Generate S&P 500 futures data.

        Known facts:
        - Opened around 1867
        - Dropped to ~1820 at worst
        - Recovered most losses by 11 AM

        Returns:
            DataFrame with minute-level futures prices
        """
        timestamps = pd.date_range(
            '2015-08-24 09:00:00',
            '2015-08-24 16:00:00',
            freq='1min'
        )

        # Model as Gaussian drop centered at 9:40 AM
        time_array = np.arange(len(timestamps))
        crash_center = 40  # 9:40 AM is 40 minutes after 9:00
        crash_magnitude = 47  # Drop of 47 points

        # Price path
        prices = 1867 - crash_magnitude * np.exp(-((time_array - crash_center) / 15) ** 2)

        # Add some noise
        prices += np.random.normal(0, 0.5, len(prices))

        # Add gradual recovery
        recovery = np.where(
            time_array > crash_center + 20,
            (time_array - crash_center - 20) * 0.3,
            0
        )
        prices += recovery

        df = pd.DataFrame({
            'timestamp': timestamps,
            'price': prices,
            'volume': np.random.randint(1000, 5000, len(timestamps))
        })

        return df.set_index('timestamp')

    def _generate_synthetic_holdings(self, symbol: str) -> Dict[str, float]:
        """
        Generate synthetic ETF holdings.

        Args:
            symbol: ETF ticker

        Returns:
            Dictionary of {ticker: shares_per_creation_unit}
        """
        if symbol == 'RSP':
            # Guggenheim S&P 500 Equal Weight
            # Holds all 500 S&P stocks in equal weight
            return {f'STOCK{i:03d}': 1.0 for i in range(500)}

        elif symbol == 'SPY':
            # SPDR S&P 500 - market cap weighted
            # Simplified: top holdings get more weight
            holdings = {}
            for i in range(500):
                # Power law distribution
                weight = 100.0 / (i + 1) ** 0.5
                holdings[f'STOCK{i:03d}'] = weight
            return holdings

        else:
            # Generic 100-stock portfolio
            return {f'STOCK{i:03d}': 1.0 for i in range(100)}

    # Data export methods

    def export_analysis_dataset(self, output_path: Path):
        """
        Export complete dataset for analysis.

        Creates comprehensive CSV with all data needed for analysis.
        Combines multiple ETFs into a single file.

        Args:
            output_path: Path where CSV should be saved

        Example:
            >>> loader = Aug24DataLoader()
            >>> loader.export_analysis_dataset(Path('flash_crash_data.csv'))
        """
        etfs = ['RSP', 'SPY', 'IVV', 'IUSV']

        combined_data = []

        for etf in etfs:
            try:
                prices = self.load_etf_prices(etf)
                prices['symbol'] = etf
                combined_data.append(prices.reset_index())
            except Exception as e:
                warnings.warn(f"Could not load {etf}: {e}")

        if combined_data:
            df = pd.concat(combined_data, ignore_index=True)
            df.to_csv(output_path, index=False)
            print(f"Exported analysis dataset to {output_path}")
            print(f"  - {len(df)} total rows")
            print(f"  - {df['symbol'].nunique()} ETFs")
            print(f"  - Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        else:
            warnings.warn("No data to export")


def calculate_fair_value_timeline(
    holdings: Dict[str, float],
    underlying_prices: pd.DataFrame
) -> pd.Series:
    """
    Calculate fair value (NAV/iNAV) over time.

    Computes the basket value based on constituent holdings and their
    current market prices.

    Args:
        holdings: Dictionary mapping ticker to shares per creation unit
                 Example: {'AAPL': 10.5, 'MSFT': 8.2, ...}
        underlying_prices: DataFrame with:
                          - Index: timestamps
                          - Columns: ticker symbols
                          - Values: prices at each timestamp

    Returns:
        Series with fair value at each timestamp

    Example:
        >>> holdings = {'AAPL': 10, 'MSFT': 5}
        >>> prices = pd.DataFrame({
        ...     'AAPL': [150, 151, 152],
        ...     'MSFT': [300, 301, 302]
        ... }, index=pd.date_range('2015-08-24 09:30', periods=3, freq='1min'))
        >>> fv = calculate_fair_value_timeline(holdings, prices)
        >>> print(fv)
    """
    fair_values = []

    for timestamp, row in underlying_prices.iterrows():
        # Sum (shares * price) for all holdings
        fv = sum(
            holdings.get(ticker, 0) * row.get(ticker, 0)
            for ticker in holdings.keys()
        )
        fair_values.append(fv)

    return pd.Series(fair_values, index=underlying_prices.index, name='fair_value')
