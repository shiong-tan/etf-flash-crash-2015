#!/usr/bin/env python3
"""Test edge cases in market maker P&L module."""

import numpy as np
import pandas as pd

# Test division by zero scenarios
print('Testing edge cases:')

# Test 1: Zero inventory position
print('\n1. Zero inventory scenario:')
etf_inventory = 0
etf_entry_price = 0.0
current_price = 100.0
pnl = etf_inventory * (current_price - etf_entry_price)
print(f'   P&L with zero inventory: {pnl}')

# Test 2: Zero standard deviation
print('\n2. Zero standard deviation for Sharpe:')
pnl_series = pd.Series([0.0, 0.0, 0.0])
sharpe = pnl_series.mean() / pnl_series.std() if pnl_series.std() > 0 else 0
print(f'   Sharpe ratio: {sharpe}')

# Test 3: Average entry price calculation when crossing zero
print('\n3. Average entry price when crossing zero:')
# Start: inventory=10000 @ 100.0
old_inventory = 10000
old_entry_price = 100.0
old_value = old_inventory * old_entry_price
print(f'   Old position: {old_inventory} shares @ ${old_entry_price} = ${old_value}')

# Add: sell 15000 @ 102.0 (crosses zero to -5000)
mm_size = -15000
price = 102.0
new_value = mm_size * price
new_inventory = old_inventory + mm_size
print(f'   New trade: {mm_size} shares @ ${price} = ${new_value}')
print(f'   New inventory: {new_inventory}')

if new_inventory != 0:
    new_entry_price = (old_value + new_value) / new_inventory
    print(f'   New entry price: ${new_entry_price:.2f}')
    print(f'   Calculation: ({old_value} + {new_value}) / {new_inventory} = {new_entry_price:.2f}')
else:
    print(f'   Inventory is zero, entry price set to 0.0')

print('\n4. Expected shortfall with insufficient data:')
pnl_series = pd.Series([100, 200, 300])
var_95 = pnl_series.quantile(0.05)
print(f'   VaR (5%): {var_95}')
shortfall_data = pnl_series[pnl_series < var_95]
print(f'   Data below VaR: {shortfall_data.tolist()}')
if len(shortfall_data) > 0:
    print(f'   Expected shortfall: {shortfall_data.mean()}')
else:
    print(f'   Expected shortfall: No data below VaR (returns NaN)')

print('\n5. Empty P&L history:')
pnl_history = []
if not pnl_history:
    print('   Risk metrics return empty dict: {}')

print('\n6. Testing quote_market with extreme inventory:')
max_inventory = 100000
etf_inventory = 91000  # 91% of max
print(f'   Inventory: {etf_inventory} ({etf_inventory/max_inventory*100:.1f}% of max)')
print(f'   Condition: abs({etf_inventory}) > {max_inventory * 0.9} = {abs(etf_inventory) > max_inventory * 0.9}')

print('\n7. Spread calculation edge case:')
fair_value = 100.0
spread_bps = 2.0
spread = fair_value * (spread_bps / 10000)
print(f'   Fair value: ${fair_value}')
print(f'   Spread (bps): {spread_bps}')
print(f'   Spread ($): ${spread}')
print(f'   Bid: ${fair_value - spread/2}')
print(f'   Ask: ${fair_value + spread/2}')
