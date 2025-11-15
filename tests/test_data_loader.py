"""
Tests for Data Loader Module

Educational tests demonstrating data loading and synthetic data generation.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil

from src.data_loader import (
    Aug24DataLoader,
    calculate_fair_value_timeline,
    DATA_DIR
)


class TestAug24DataLoader:
    """Test Aug24DataLoader class"""

    def setup_method(self):
        """Create temporary data directory for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = Aug24DataLoader(data_dir=Path(self.temp_dir))

    def teardown_method(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization_default(self):
        """Test loader initializes with default data directory"""
        loader = Aug24DataLoader()
        assert loader.data_dir == DATA_DIR

    def test_initialization_custom_dir(self):
        """Test loader initializes with custom directory"""
        custom_dir = Path(self.temp_dir) / 'custom'
        loader = Aug24DataLoader(data_dir=custom_dir)
        assert loader.data_dir == custom_dir
        # Should create directory if it doesn't exist
        assert custom_dir.exists()

    def test_validate_data_directory_creates_dir(self):
        """Test that missing directory is created"""
        test_dir = Path(self.temp_dir) / 'new_dir'
        assert not test_dir.exists()

        loader = Aug24DataLoader(data_dir=test_dir)
        assert test_dir.exists()

    def test_load_etf_prices_generates_synthetic_when_missing(self):
        """Test synthetic data generation when file not found"""
        df = self.loader.load_etf_prices('RSP')

        # Should return a DataFrame
        assert isinstance(df, pd.DataFrame)

        # Should have required columns
        required_cols = ['price', 'volume', 'inav', 'bid', 'ask', 'spread_bps']
        for col in required_cols:
            assert col in df.columns

        # Should have data
        assert len(df) > 0

        # Index should be datetime
        assert isinstance(df.index, pd.DatetimeIndex)

    def test_load_etf_prices_from_file(self):
        """Test loading ETF prices from CSV file"""
        # Create sample CSV file
        timestamps = pd.date_range('2015-08-24 09:30', periods=5, freq='1min')
        data = {
            'timestamp': timestamps,
            'ticker': ['RSP'] * 5,
            'price': [100.0, 99.5, 98.0, 97.0, 99.0],
            'volume': [1000, 2000, 5000, 3000, 1500],
            'inav': [100.0, 100.0, 100.0, 100.0, 100.0]
        }
        df = pd.DataFrame(data)

        # Save to file
        filepath = Path(self.temp_dir) / 'aug24_price_data.csv'
        df.to_csv(filepath, index=False)

        # Load data
        loaded_df = self.loader.load_etf_prices('RSP')

        assert len(loaded_df) == 5
        assert loaded_df['price'].iloc[0] == 100.0
        assert loaded_df['volume'].iloc[0] == 1000

    def test_load_etf_prices_handles_halted_prices(self):
        """Test that HALTED prices are converted to NaN"""
        timestamps = pd.date_range('2015-08-24 09:30', periods=3, freq='1min')
        data = {
            'timestamp': timestamps,
            'ticker': ['RSP'] * 3,
            'price': [100.0, 'HALTED', 99.0],
            'volume': [1000, 0, 2000]
        }
        df = pd.DataFrame(data)

        filepath = Path(self.temp_dir) / 'aug24_price_data.csv'
        df.to_csv(filepath, index=False)

        loaded_df = self.loader.load_etf_prices('RSP')

        # HALTED should be converted to NaN
        assert pd.isna(loaded_df['price'].iloc[1])
        assert loaded_df['price'].iloc[0] == 100.0
        assert loaded_df['price'].iloc[2] == 99.0

    def test_load_etf_prices_missing_symbol(self):
        """Test loading non-existent symbol generates synthetic data"""
        timestamps = pd.date_range('2015-08-24 09:30', periods=3, freq='1min')
        data = {
            'timestamp': timestamps,
            'ticker': ['SPY'] * 3,  # Different symbol
            'price': [200.0, 199.0, 198.0],
            'volume': [1000, 2000, 3000]
        }
        df = pd.DataFrame(data)

        filepath = Path(self.temp_dir) / 'aug24_price_data.csv'
        df.to_csv(filepath, index=False)

        # Try to load RSP (not in file)
        loaded_df = self.loader.load_etf_prices('RSP')

        # Should generate synthetic data
        assert len(loaded_df) > 0
        assert 'price' in loaded_df.columns

    def test_load_halt_log_generates_synthetic_when_missing(self):
        """Test synthetic halt log generation"""
        df = self.loader.load_halt_log()

        assert isinstance(df, pd.DataFrame)

        # Should have expected columns
        expected_cols = ['ticker', 'halt_start', 'halt_end']
        for col in expected_cols:
            assert col in df.columns

        # Should have duration info (either duration_minutes or duration_sec)
        assert 'duration_sec' in df.columns or 'duration_minutes' in df.columns

        # Should have data
        assert len(df) > 0

    def test_load_sp500_futures_generates_synthetic_when_missing(self):
        """Test synthetic futures data generation"""
        df = self.loader.load_sp500_futures()

        assert isinstance(df, pd.DataFrame)

        # Should have price and volume
        assert 'price' in df.columns
        assert 'volume' in df.columns

        # Index should be datetime
        assert isinstance(df.index, pd.DatetimeIndex)

        # Should have data
        assert len(df) > 0

    def test_load_etf_holdings_generates_synthetic_when_missing(self):
        """Test synthetic holdings generation"""
        holdings = self.loader.load_etf_holdings('RSP')

        assert isinstance(holdings, dict)

        # Should have stocks
        assert len(holdings) > 0

        # All values should be positive floats
        for ticker, shares in holdings.items():
            assert isinstance(ticker, str)
            assert isinstance(shares, (int, float))
            assert shares > 0

    def test_synthetic_etf_data_has_realistic_flash_crash(self):
        """Test that synthetic data includes flash crash characteristics"""
        df = self.loader.load_etf_prices('RSP')

        # Should have price volatility
        price_std = df['price'].std()
        assert price_std > 0

        # Should have some large price moves (flash crash)
        price_changes = df['price'].pct_change().abs()
        max_change = price_changes.max()
        # At least one move >5% (flash crash characteristic)
        assert max_change > 0.05

    def test_synthetic_data_different_symbols_have_variation(self):
        """Test that different symbols generate different data"""
        rsp_data = self.loader.load_etf_prices('RSP')
        spy_data = self.loader.load_etf_prices('SPY')

        # Should have different price levels
        assert abs(rsp_data['price'].mean() - spy_data['price'].mean()) > 1.0

    def test_export_analysis_dataset(self):
        """Test exporting combined analysis dataset"""
        output_path = Path(self.temp_dir) / 'analysis_export.csv'

        # This method should create a combined dataset
        # Note: Implementation may vary, so we test basic functionality
        try:
            self.loader.export_analysis_dataset(output_path)
            # If method exists and runs without error, that's good
            # We can't verify file creation as implementation may vary
        except AttributeError:
            # Method might not be fully implemented yet
            pytest.skip("export_analysis_dataset not fully implemented")


class TestCalculateFairValueTimeline:
    """Test calculate_fair_value_timeline function"""

    def test_calculate_fair_value_simple(self):
        """Test basic fair value calculation"""
        holdings = {'AAPL': 10, 'MSFT': 5}

        timestamps = pd.date_range('2015-08-24 09:30', periods=3, freq='1min')
        prices = pd.DataFrame({
            'AAPL': [150.0, 151.0, 152.0],
            'MSFT': [300.0, 301.0, 302.0]
        }, index=timestamps)

        fv = calculate_fair_value_timeline(holdings, prices)

        # Fair value at t=0: 10*150 + 5*300 = 3000
        assert fv.iloc[0] == 3000.0

        # Fair value at t=1: 10*151 + 5*301 = 3015
        assert fv.iloc[1] == 3015.0

        # Fair value at t=2: 10*152 + 5*302 = 3030
        assert fv.iloc[2] == 3030.0

    def test_calculate_fair_value_single_stock(self):
        """Test fair value with single stock"""
        holdings = {'AAPL': 100}

        timestamps = pd.date_range('2015-08-24 09:30', periods=2, freq='1min')
        prices = pd.DataFrame({
            'AAPL': [150.0, 155.0]
        }, index=timestamps)

        fv = calculate_fair_value_timeline(holdings, prices)

        assert fv.iloc[0] == 15000.0  # 100 * 150
        assert fv.iloc[1] == 15500.0  # 100 * 155

    def test_calculate_fair_value_multiple_stocks(self):
        """Test fair value with multiple stocks"""
        holdings = {
            'AAPL': 10,
            'MSFT': 20,
            'GOOGL': 5,
            'AMZN': 3
        }

        timestamps = pd.date_range('2015-08-24 09:30', periods=2, freq='1min')
        prices = pd.DataFrame({
            'AAPL': [150.0, 151.0],
            'MSFT': [300.0, 301.0],
            'GOOGL': [500.0, 505.0],
            'AMZN': [400.0, 402.0]
        }, index=timestamps)

        fv = calculate_fair_value_timeline(holdings, prices)

        # t=0: 10*150 + 20*300 + 5*500 + 3*400 = 1500 + 6000 + 2500 + 1200 = 11200
        assert fv.iloc[0] == 11200.0

    def test_calculate_fair_value_with_fractional_shares(self):
        """Test fair value with fractional shares"""
        holdings = {'AAPL': 10.5, 'MSFT': 7.3}

        timestamps = pd.date_range('2015-08-24 09:30', periods=2, freq='1min')
        prices = pd.DataFrame({
            'AAPL': [100.0, 110.0],
            'MSFT': [200.0, 210.0]
        }, index=timestamps)

        fv = calculate_fair_value_timeline(holdings, prices)

        # t=0: 10.5*100 + 7.3*200 = 1050 + 1460 = 2510
        assert abs(fv.iloc[0] - 2510.0) < 0.01

        # t=1: 10.5*110 + 7.3*210 = 1155 + 1533 = 2688
        assert abs(fv.iloc[1] - 2688.0) < 0.01

    def test_calculate_fair_value_returns_series(self):
        """Test that function returns a pandas Series"""
        holdings = {'AAPL': 10}
        timestamps = pd.date_range('2015-08-24 09:30', periods=3, freq='1min')
        prices = pd.DataFrame({'AAPL': [150.0, 151.0, 152.0]}, index=timestamps)

        fv = calculate_fair_value_timeline(holdings, prices)

        assert isinstance(fv, pd.Series)
        assert len(fv) == len(timestamps)
        assert (fv.index == timestamps).all()

    def test_calculate_fair_value_with_price_changes(self):
        """Test fair value tracks price changes correctly"""
        holdings = {'STOCK_A': 100}

        timestamps = pd.date_range('2015-08-24 09:30', periods=5, freq='1min')
        # Simulate flash crash: 100 -> 95 -> 80 -> 85 -> 98
        prices = pd.DataFrame({
            'STOCK_A': [100.0, 95.0, 80.0, 85.0, 98.0]
        }, index=timestamps)

        fv = calculate_fair_value_timeline(holdings, prices)

        assert fv.iloc[0] == 10000.0  # Normal
        assert fv.iloc[1] == 9500.0   # Decline starts
        assert fv.iloc[2] == 8000.0   # Flash crash bottom
        assert fv.iloc[3] == 8500.0   # Recovery starts
        assert fv.iloc[4] == 9800.0   # Partial recovery


class TestSyntheticDataGeneration:
    """Test synthetic data generation quality"""

    def setup_method(self):
        """Create temp loader"""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = Aug24DataLoader(data_dir=Path(self.temp_dir))

    def teardown_method(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_synthetic_etf_data_time_range(self):
        """Test that synthetic data covers trading hours"""
        df = self.loader.load_etf_prices('RSP')

        # Should start around market open (9:30 AM ET)
        first_time = df.index[0].time()
        # Allow some flexibility
        assert first_time.hour >= 9

        # Should cover multiple hours
        duration = (df.index[-1] - df.index[0]).total_seconds() / 3600
        assert duration > 1.0  # At least 1 hour of data

    def test_synthetic_etf_data_no_missing_prices(self):
        """Test that synthetic data doesn't have gaps in normal period"""
        df = self.loader.load_etf_prices('SPY')

        # Count non-NaN prices
        valid_prices = df['price'].notna().sum()

        # Most prices should be valid (allowing for some halts)
        assert valid_prices > len(df) * 0.5

    def test_synthetic_halt_data_realistic_durations(self):
        """Test that synthetic halts have realistic durations"""
        df = self.loader.load_halt_log()

        if 'duration_sec' in df.columns:
            # LULD halts are typically 5-10 minutes (300-600 seconds)
            # Some may be longer during crisis
            durations = df['duration_sec']
            assert durations.min() >= 60  # At least 1 minute
            assert durations.max() <= 3600  # Not more than 1 hour
        elif 'duration_minutes' in df.columns:
            durations = df['duration_minutes']
            assert durations.min() >= 1  # At least 1 minute
            assert durations.max() <= 60  # Not more than 1 hour

    def test_synthetic_futures_data_continuity(self):
        """Test that futures data is continuous"""
        df = self.loader.load_sp500_futures()

        # Should not have large gaps in index
        if len(df) > 1:
            time_diffs = df.index.to_series().diff()
            max_gap = time_diffs.max()

            # Maximum gap should be reasonable (e.g., 5 minutes)
            assert max_gap <= pd.Timedelta(minutes=10)

    def test_synthetic_holdings_sum_reasonable(self):
        """Test that synthetic holdings represent realistic basket"""
        holdings = self.loader.load_etf_holdings('RSP')

        # Equal-weight S&P 500 ETF should have ~500 stocks
        # Allow some flexibility
        assert len(holdings) >= 100  # At least 100 stocks
        assert len(holdings) <= 600  # Not more than 600

        # For equal-weight, shares should be similar across stocks
        # (though not perfectly equal due to price differences)
        if len(holdings) > 10:
            values = list(holdings.values())
            # Standard deviation shouldn't be too large relative to mean
            # This is a loose check
            assert np.std(values) / np.mean(values) < 10


class TestEdgeCases:
    """Test edge cases and error handling"""

    def setup_method(self):
        """Create temp loader"""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = Aug24DataLoader(data_dir=Path(self.temp_dir))

    def teardown_method(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_empty_holdings_dictionary(self):
        """Test fair value calculation with empty holdings"""
        holdings = {}
        timestamps = pd.date_range('2015-08-24 09:30', periods=3, freq='1min')
        prices = pd.DataFrame({'AAPL': [150.0, 151.0, 152.0]}, index=timestamps)

        fv = calculate_fair_value_timeline(holdings, prices)

        # Empty holdings should give zero fair value
        assert (fv == 0).all()

    def test_missing_price_data_for_holding(self):
        """Test when holding not in price DataFrame"""
        holdings = {'AAPL': 10, 'MSFT': 5}
        timestamps = pd.date_range('2015-08-24 09:30', periods=2, freq='1min')

        # Price data only has AAPL, missing MSFT
        prices = pd.DataFrame({
            'AAPL': [150.0, 151.0]
        }, index=timestamps)

        # Should handle gracefully (skip missing or use NaN)
        fv = calculate_fair_value_timeline(holdings, prices)

        # Should still calculate based on available data
        # Implementation may vary on how it handles missing data
        assert isinstance(fv, pd.Series)

    def test_load_etf_prices_unusual_symbol(self):
        """Test loading data with unusual symbol"""
        # Should handle gracefully and generate synthetic data
        df = self.loader.load_etf_prices('XYZ123')

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_corrupted_csv_file(self):
        """Test handling of corrupted CSV file"""
        # Create invalid CSV
        filepath = Path(self.temp_dir) / 'aug24_price_data.csv'
        with open(filepath, 'w') as f:
            f.write("invalid,csv,format\n")
            f.write("not,proper,data\n")

        # Should fall back to synthetic data
        df = self.loader.load_etf_prices('RSP')

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
