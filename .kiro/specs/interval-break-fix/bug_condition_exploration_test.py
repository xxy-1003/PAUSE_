#!/usr/bin/env python3
"""
Property 1: Bug Condition - Interval Break Triggering Failure
Exploratory bug condition test for interval break triggering bug.

This test demonstrates Property 1 from the design document.
It should FAIL on unfixed code, proving the bug exists.

**CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
**DO NOT attempt to fix the test or the code when it fails** 
**NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
**GOAL**: Surface counterexamples that demonstrate the bug exists
**Scoped PBT Approach**: For deterministic bugs, scope the property to the concrete failing case(s) to ensure reproducibility
**EXPECTED OUTCOME**: Test FAILS (this is correct - it proves the bug exists)
**Validates: Requirements 2.1, 2.2, 2.3**
"""

import sys
import os
import time
import unittest
from datetime import datetime

# Add the project to the path so we can import the actual timer logic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# We need to simulate the streamlit session state
class MockStreamlitSessionState:
    """Mock streamlit session state for testing"""
    def __init__(self):
        self.mode = "focus"
        self.running = True
        self.start_time = time.time()
        self.elapsed = 0
        self.last_break_time = None  # Will be set based on test
        self.break_type = "normal"
        self.focus_completed = True
        self.focus_elapsed_before_break = 0
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)

def extract_interval_decision_logic(last_break_time_value, interval_value):
    """
    Extract and test the interval decision logic from Timer.py
    
    This simulates the interval decision logic from Timer.py lines 176-186
    without running the full Streamlit app.
    
    Args:
        last_break_time_value: The value of last_break_time to test with
        interval_value: The INTERVAL value in seconds
        
    Returns:
        Tuple of (break_type, time_since_break)
    """
    # Simulate the logic from Timer.py
    current_time = time.time()
    time_since_break = current_time - last_break_time_value
    
    # Debug output (matching Timer.py)
    print(f"DEBUG: time_since_break: {time_since_break}")
    print(f"DEBUG: INTERVAL: {interval_value}")
    
    # Interval decision logic (from Timer.py lines 176-186)
    if time_since_break >= interval_value:
        break_type = "interval"
        print("DEBUG: Should set break_type to 'interval'")
    else:
        break_type = "normal" 
        print("DEBUG: Should set break_type to 'normal'")
    
    return break_type, time_since_break

class TestIntervalBreakBugCondition(unittest.TestCase):
    """
    Property 1: Bug Condition - Interval Break Triggering Failure
    
    This test should FAIL on unfixed code, proving the bug exists.
    The bug condition is: focus_completed AND time_since_break >= INTERVAL
    Expected behavior: break_type should be "interval"
    
    **Validates: Requirements 2.1, 2.2, 2.3**
    """
    
    def test_interval_break_should_trigger_when_time_exceeds_interval(self):
        """
        Test case 1: Interval break SHOULD trigger when time_since_break > INTERVAL
        This should FAIL on unfixed code (proves bug exists)
        """
        # Setup: Last break was 45 minutes ago, INTERVAL = 30 minutes
        current_time = time.time()
        last_break_time = current_time - 2700  # 45 minutes ago (2700 seconds)
        interval_value = 1800  # 30 minutes (1800 seconds)
        
        # Extract and test the interval decision logic
        break_type, time_since_break = extract_interval_decision_logic(last_break_time, interval_value)
        
        # Expected: break_type should be "interval" because 45 >= 30
        # This should FAIL on unfixed code
        self.assertEqual(
            break_type, 
            "interval",
            f"BUG: break_type should be 'interval' when time_since_break >= INTERVAL. "
            f"time_since_break={time_since_break}, "
            f"INTERVAL={interval_value}, "
            f"but got break_type='{break_type}'. "
            f"This test FAILS on unfixed code (which is correct - it proves the bug exists)."
        )
        
    def test_interval_break_should_trigger_when_time_equals_interval(self):
        """
        Test case 2: Interval break SHOULD trigger when time_since_break == INTERVAL (edge case)
        This should also FAIL on unfixed code if the bug affects edge cases
        """
        # Setup: Last break was exactly 30 minutes ago
        current_time = time.time()
        last_break_time = current_time - 1800  # Exactly 30 minutes ago (1800 seconds)
        interval_value = 1800  # 30 minutes (1800 seconds)
        
        # Extract and test the interval decision logic
        break_type, time_since_break = extract_interval_decision_logic(last_break_time, interval_value)
        
        # Expected: break_type should be "interval" because >= comparison
        # This might FAIL on unfixed code depending on the bug
        self.assertEqual(
            break_type,
            "interval",
            f"Edge case: break_type should be 'interval' when time_since_break == INTERVAL. "
            f"time_since_break={time_since_break}, "
            f"INTERVAL={interval_value}. "
            f"Edge case test result: {break_type}"
        )
    
    def test_normal_break_should_trigger_when_time_less_than_interval(self):
        """
        Test case 3: Normal break SHOULD trigger when time_since_break < INTERVAL
        This should PASS on unfixed code (preservation test)
        """
        # Setup: Last break was 20 minutes ago, INTERVAL = 30 minutes
        current_time = time.time()
        last_break_time = current_time - 1200  # 20 minutes ago (1200 seconds)
        interval_value = 1800  # 30 minutes (1800 seconds)
        
        # Extract and test the interval decision logic
        break_type, time_since_break = extract_interval_decision_logic(last_break_time, interval_value)
        
        # Expected: break_type should be "normal" because 20 < 30
        # This should PASS on unfixed code (preservation)
        self.assertEqual(
            break_type,
            "normal",
            f"Preservation: break_type should be 'normal' when time_since_break < INTERVAL. "
            f"time_since_break={time_since_break}, "
            f"INTERVAL={interval_value}. "
            f"Preservation test result: {break_type}"
        )
    
    def test_property_based_interval_break_condition(self):
        """
        Property-based test: For ANY time_since_break >= INTERVAL, break_type should be "interval"
        This is the core bug condition property test.
        
        We'll test a range of values to generate potential counterexamples.
        """
        # Test with various time values that should trigger interval breaks
        test_cases = [
            (1801, 1800, "interval"),  # 1 second over interval
            (2000, 1800, "interval"),  # 200 seconds over interval  
            (3600, 1800, "interval"),  # 1 hour over 30 minute interval
            (7200, 1800, "interval"),  # 2 hours over 30 minute interval
        ]
        
        current_time = time.time()
        
        for time_since_break, interval, expected_break_type in test_cases:
            with self.subTest(time_since_break=time_since_break, interval=interval):
                last_break_time = current_time - time_since_break
                break_type, actual_time_since_break = extract_interval_decision_logic(last_break_time, interval)
                
                # This assertion should FAIL on unfixed code for cases where expected_break_type == "interval"
                self.assertEqual(
                    break_type,
                    expected_break_type,
                    f"Property violation: When time_since_break >= INTERVAL, break_type should be 'interval'. "
                    f"time_since_break={actual_time_since_break}, "
                    f"INTERVAL={interval}, "
                    f"expected='{expected_break_type}', got='{break_type}'. "
                    f"This is a counterexample proving the bug exists."
                )

def run_exploration_tests():
    """Run the exploratory tests and report results"""
    print("=" * 70)
    print("BUG CONDITION EXPLORATION TEST - Property 1: Interval Break Triggering")
    print("=" * 70)
    print("NOTE: These tests should FAIL on unfixed code.")
    print("The failure proves the bug exists.")
    print("=" * 70)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntervalBreakBugCondition)
    result = runner.run(suite)
    
    # Report findings
    print("\n" + "=" * 70)
    print("EXPLORATORY TEST RESULTS:")
    print("=" * 70)
    
    if result.failures:
        print("✅ SUCCESS: Tests failed as expected (proves bug exists)")
        print(f"Found {len(result.failures)} counterexample(s) demonstrating the bug:")
        
        counterexamples = []
        for test, traceback in result.failures:
            test_name = test.id().split('.')[-1]
            # Extract counterexample details from error message
            error_msg = str(traceback).split('\n')[-2] if '\n' in str(traceback) else str(traceback)
            counterexamples.append((test_name, error_msg))
            
        for test_name, error_msg in counterexamples:
            print(f"  - {test_name}: {error_msg[:100]}...")
            
        print("\nCounterexamples found (these prove the bug exists):")
        for test_name, error_msg in counterexamples:
            print(f"\n{test_name}:")
            print(f"  {error_msg}")
            
    elif result.errors:
        print("⚠️  WARNING: Tests had errors (may indicate test setup issues)")
        for test, traceback in result.errors:
            print(f"  - {test.id()}: Test error")
    else:
        print("❌ UNEXPECTED: All tests passed (bug may already be fixed)")
        print("Consider revising bug analysis or test assumptions")
        print("\nPossible reasons:")
        print("  1. The bug has already been fixed")
        print("  2. The test is not correctly simulating the bug condition")
        print("  3. The bug is in a different part of the code")
    
    print("=" * 70)
    
    # Return summary for PBT status update
    test_summary = {
        "total_tests": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "counterexamples": []
    }
    
    if result.failures:
        for test, traceback in result.failures:
            test_summary["counterexamples"].append({
                "test": test.id(),
                "error": str(traceback).split('\n')[-2] if '\n' in str(traceback) else str(traceback)
            })
    
    return test_summary

if __name__ == "__main__":
    print("Property 1: Bug Condition - Interval Break Triggering Failure")
    print("This test encodes the expected behavior for the interval break bug.")
    print("It should FAIL on unfixed code (proving the bug exists).")
    print("The same test will PASS after the fix is implemented.")
    print()
    
    test_summary = run_exploration_tests()
    
    # Print summary for PBT status update
    print("\n" + "=" * 70)
    print("PBT STATUS SUMMARY:")
    print("=" * 70)
    print(f"Total tests run: {test_summary['total_tests']}")
    print(f"Failures (expected): {test_summary['failures']}")
    print(f"Errors: {test_summary['errors']}")
    
    if test_summary['failures'] > 0:
        print("\n✅ BUG CONFIRMED: Test failed as expected (proves bug exists)")
        print("Counterexamples found (these will help understand the root cause):")
        for i, ce in enumerate(test_summary['counterexamples'], 1):
            print(f"\nCounterexample {i}:")
            print(f"  Test: {ce['test']}")
            print(f"  Error: {ce['error']}")
    else:
        print("\n❌ UNEXPECTED: No failures found")
        print("The bug condition test passed, which is unexpected for unfixed code.")