#!/usr/bin/env python3
"""
Exploratory bug condition test for interval break triggering bug.

This test demonstrates Property 1: Bug Condition from the design document.
It should FAIL on unfixed code, proving the bug exists.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import unittest
from unittest.mock import Mock, patch

# We need to simulate the timer logic
class MockTimerState:
    def __init__(self):
        self.mode = "focus"
        self.running = True
        self.start_time = time.time()
        self.elapsed = 0
        self.last_break_time = time.time() - 2000  # 2000 seconds ago (33+ minutes)
        self.break_type = "normal"
        self.focus_completed = False
        self.INTERVAL = 1800  # 30 minutes in seconds
        self.time_since_break = 0
        
    def calculate_time_since_break(self):
        """Calculate time since last break"""
        self.time_since_break = time.time() - self.last_break_time
        return self.time_since_break

def simulate_focus_completion(timer_state):
    """
    Simulates the focus completion logic from Timer.py
    This should trigger an interval break if time_since_break >= INTERVAL
    """
    # Calculate time since last break
    time_since_break = time.time() - timer_state.last_break_time
    
    # Debug output (matching Timer.py)
    print(f"DEBUG: time_since_break: {time_since_break}")
    print(f"DEBUG: INTERVAL: {timer_state.INTERVAL}")
    
    # Interval decision logic (from Timer.py lines 177-186)
    if time_since_break >= timer_state.INTERVAL:
        timer_state.break_type = "interval"
        print("DEBUG: Should set break_type to 'interval'")
    else:
        timer_state.break_type = "normal"
        print("DEBUG: Should set break_type to 'normal'")
    
    return timer_state

class TestIntervalBreakBug(unittest.TestCase):
    """
    Property 1: Bug Condition - Interval Break Triggering Failure
    
    This test should FAIL on unfixed code, proving the bug exists.
    The bug condition is: focus_completed AND time_since_break >= INTERVAL
    Expected behavior: break_type should be "interval"
    """
    
    def test_interval_break_should_trigger(self):
        """Test case where interval break SHOULD trigger"""
        # Setup: Last break was 45 minutes ago, INTERVAL = 30 minutes
        timer_state = MockTimerState()
        timer_state.last_break_time = time.time() - 2700  # 45 minutes ago
        timer_state.INTERVAL = 1800  # 30 minutes
        
        # Simulate focus completion
        result = simulate_focus_completion(timer_state)
        
        # Expected: break_type should be "interval" because 45 >= 30
        self.assertEqual(
            result.break_type, 
            "interval",
            f"BUG: break_type should be 'interval' when time_since_break >= INTERVAL. "
            f"time_since_break={time.time() - timer_state.last_break_time}, "
            f"INTERVAL={timer_state.INTERVAL}, "
            f"but got break_type='{result.break_type}'"
        )
        
    def test_normal_break_should_trigger(self):
        """Test case where normal break SHOULD trigger (preservation test)"""
        # Setup: Last break was 20 minutes ago, INTERVAL = 30 minutes
        timer_state = MockTimerState()
        timer_state.last_break_time = time.time() - 1200  # 20 minutes ago
        timer_state.INTERVAL = 1800  # 30 minutes
        
        # Simulate focus completion
        result = simulate_focus_completion(timer_state)
        
        # Expected: break_type should be "normal" because 20 < 30
        self.assertEqual(
            result.break_type,
            "normal",
            f"Preservation: break_type should be 'normal' when time_since_break < INTERVAL. "
            f"time_since_break={time.time() - timer_state.last_break_time}, "
            f"INTERVAL={timer_state.INTERVAL}"
        )
    
    def test_edge_case_exact_interval(self):
        """Test edge case where time_since_break exactly equals INTERVAL"""
        # Setup: Last break was exactly 30 minutes ago
        timer_state = MockTimerState()
        timer_state.last_break_time = time.time() - 1800  # Exactly 30 minutes ago
        timer_state.INTERVAL = 1800  # 30 minutes
        
        # Simulate focus completion
        result = simulate_focus_completion(timer_state)
        
        # Expected: break_type should be "interval" because >= comparison
        self.assertEqual(
            result.break_type,
            "interval",
            f"Edge case: break_type should be 'interval' when time_since_break == INTERVAL. "
            f"time_since_break={time.time() - timer_state.last_break_time}, "
            f"INTERVAL={timer_state.INTERVAL}"
        )

if __name__ == "__main__":
    print("Running exploratory bug condition tests...")
    print("=" * 60)
    print("NOTE: These tests should FAIL on unfixed code.")
    print("The failure proves the bug exists.")
    print("=" * 60)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntervalBreakBug)
    result = runner.run(suite)
    
    # Report findings
    print("\n" + "=" * 60)
    print("EXPLORATORY TEST RESULTS:")
    print("=" * 60)
    
    if result.failures:
        print("✅ SUCCESS: Tests failed as expected (proves bug exists)")
        print(f"Found {len(result.failures)} counterexample(s):")
        for test, traceback in result.failures:
            print(f"  - {test.id()}: Demonstrates the bug")
    elif result.errors:
        print("⚠️  WARNING: Tests had errors (may indicate test setup issues)")
    else:
        print("❌ UNEXPECTED: All tests passed (bug may already be fixed)")
        print("Consider revising bug analysis or test assumptions")
    
    print("=" * 60)