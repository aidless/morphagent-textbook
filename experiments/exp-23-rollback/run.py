#!/usr/bin/env python3
"""Experiment 23: 自动回滚测试

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
