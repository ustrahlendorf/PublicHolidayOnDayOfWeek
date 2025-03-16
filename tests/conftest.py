"""Configuration file for pytest."""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_path)

# Also add the tests directory to Python path
tests_path = str(Path(__file__).parent)
sys.path.insert(0, tests_path) 