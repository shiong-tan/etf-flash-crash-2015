"""
Repository Structure Verification

Verifies all expected files and directories are present and correctly structured.
"""

import sys
from pathlib import Path


def check_structure():
    """Verify repository structure"""
    root = Path(__file__).parent.parent
    issues = []

    print("ETF Flash Crash 2015 Repository Verification")
    print("=" * 50)
    print()

    # Check infrastructure files
    print("📋 Checking infrastructure files...")
    required_files = [
        '.gitignore',
        'requirements.txt',
        'README.md',
    ]

    for file in required_files:
        if (root / file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} MISSING")
            issues.append(f"Missing: {file}")

    # Check directories
    print()
    print("📁 Checking directory structure...")
    required_dirs = {
        'guide': [
            '01-background',
            '02-the-event',
            '03-deep-dive',
            '04-market-maker-perspective',
            '05-aftermath'
        ],
        'src': ['__init__.py', 'etf_pricing.py', 'order_book.py', 'visualization.py'],
        'assets/charts': ['etf_vs_nav.svg', 'luld_flow.svg', 'orderbook_airpocket.svg', 'timeline_visual.svg'],
        'assets/data': ['aug24_price_data.csv', 'luld_halts.csv', 'README.md'],
        'notebooks': ['01-understanding-the-crash.ipynb'],
        'tests': ['test_etf_pricing.py', 'test_order_book.py', 'verify_repository.py']
    }

    for dir_name, expected_files in required_dirs.items():
        dir_path = root / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
            for file in expected_files:
                file_path = dir_path / file
                if file_path.exists():
                    if file_path.is_dir():
                        print(f"    ✅ {file}/")
                    else:
                        size = file_path.stat().st_size
                        print(f"    ✅ {file} ({size:,} bytes)")
                else:
                    print(f"    ❌ {file} MISSING")
                    issues.append(f"Missing: {dir_name}/{file}")
        else:
            print(f"  ❌ {dir_name}/ MISSING")
            issues.append(f"Missing directory: {dir_name}")

    # Check guide markdown files
    print()
    print("📝 Checking guide content...")
    guide_sections = {
        '01-background': [
            'what-are-etfs.md',
            'order-types.md',
            'luld-mechanism.md',
            'how-market-makers-work.md'
        ],
        '02-the-event': [
            'timeline.md',
            'pre-crash-conditions.md',
            'opening-chaos.md',
            'who-was-affected.md'
        ],
        '03-deep-dive': [
            'nav-disconnect.md',
            'case-study-rsp.md',
            'case-study-retail.md'
        ],
        '04-market-maker-perspective': [
            'jane-street-overview.md',
            'role-of-market-makers.md',
            'hedging-under-stress.md',
            'luld-from-mm-view.md'
        ],
        '05-aftermath': [
            'regulatory-changes.md',
            'broker-reforms.md',
            'lasting-lessons.md'
        ]
    }

    total_guide_files = 0
    for section, files in guide_sections.items():
        section_path = root / 'guide' / section
        if section_path.exists():
            for file in files:
                file_path = section_path / file
                if file_path.exists():
                    total_guide_files += 1
                    size = file_path.stat().st_size
                    print(f"  ✅ guide/{section}/{file} ({size:,} bytes)")
                else:
                    print(f"  ❌ guide/{section}/{file} MISSING")
                    issues.append(f"Missing: guide/{section}/{file}")

    # Module imports
    print()
    print("🐍 Checking Python modules...")
    sys.path.insert(0, str(root / 'src'))

    try:
        import etf_pricing
        print("  ✅ etf_pricing module imports successfully")

        # Check key functions
        funcs = ['calculate_nav', 'calculate_inav', 'arbitrage_spread',
                 'creation_profit', 'simulate_stale_inav']
        for func in funcs:
            if hasattr(etf_pricing, func):
                print(f"    ✅ {func}()")
            else:
                print(f"    ❌ {func}() MISSING")
                issues.append(f"Missing function: etf_pricing.{func}")
    except Exception as e:
        print(f"  ❌ etf_pricing import failed: {e}")
        issues.append(f"Import error: etf_pricing - {e}")

    try:
        import order_book
        print("  ✅ order_book module imports successfully")

        if hasattr(order_book, 'OrderBook'):
            print("    ✅ OrderBook class")
        else:
            print("    ❌ OrderBook class MISSING")
            issues.append("Missing class: order_book.OrderBook")
    except Exception as e:
        print(f"  ❌ order_book import failed: {e}")
        issues.append(f"Import error: order_book - {e}")

    try:
        import visualization
        print("  ✅ visualization module imports successfully")

        viz_funcs = ['plot_price_vs_inav', 'plot_order_book', 'plot_luld_bands']
        for func in viz_funcs:
            if hasattr(visualization, func):
                print(f"    ✅ {func}()")
            else:
                print(f"    ❌ {func}() MISSING")
                issues.append(f"Missing function: visualization.{func}")
    except Exception as e:
        print(f"  ❌ visualization import failed: {e}")
        issues.append(f"Import error: visualization - {e}")

    # Summary
    print()
    print("=" * 50)
    print("Summary:")
    print(f"  Total guide files: {total_guide_files}")
    print(f"  Total issues: {len(issues)}")

    if issues:
        print()
        print("⚠️  Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print()
        print("✅ All checks passed! Repository is complete and ready to use.")
        return True


if __name__ == '__main__':
    success = check_structure()
    sys.exit(0 if success else 1)
