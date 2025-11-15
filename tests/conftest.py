"""
Pytest configuration for ETF Flash Crash 2015 tests.

This file automatically configures the Python path to allow
tests to import modules from the src directory.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add src directory to Python path
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

# Verify paths are accessible
assert project_root.exists(), f"Project root not found: {project_root}"
assert src_dir.exists(), f"Source directory not found: {src_dir}"
