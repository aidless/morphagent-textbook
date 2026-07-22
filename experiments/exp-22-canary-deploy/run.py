#!/usr/bin/env python3
"""Experiment 22: 金丝雀部署模拟

Usage: python run.py [--mock]
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    # Pass command line args
    mock_mode = "--mock" in sys.argv
    main()
