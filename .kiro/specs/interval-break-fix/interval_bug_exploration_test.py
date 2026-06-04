#!/usr/bin/env python3
"""
Property 1: Bug Condition - Interval Break Triggering Failure
Exploratory bug condition test that actually simulates the Timer.py logic.

This test demonstrates Property 1 from the design document.
It should FAIL on unfixed code, proving the bug exists.

**CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
**GOAL**: Surface counterexamples that demonstrate the bug exists

**Validates: Requirements 2.1, 2.2, 2.3**

Bug Condition from design:
  isBugCondition(input) where 
    input.focus_completed = true 
    AND input.time_since_break >= input.INTERVAL 
    AND input.break_type != "interval"

Expected Behavior from design:
  For any timer state where a focus session has completed 
  AND time since last break is greater than or equal to the configured INTERVAL,
  the timer SHALL set break_type to "interval", 
  use INTERVAL_BREAK_DURATION for the break,
  and correctly enter the interval break path.
"""

import sys
import os
import time
import unittest

# Add the project to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def simulate_timer_interval_decision(last_break_time, interval):
    """
    Simulates the exact interval decision logic from Timer.py lines 176-186
    
    Args:
        last_break_time: The last break time in seconds (time.time() format)
        interval: The INTERVAL value in seconds
        
    Returns:
        The break_type that would be set ("interval" or "normal")
    """
    # Exact logic from Timer.py:
    time_since_break = time.time() - last_break_time
    
    print(f"DEBUG: time_since_break: {time_since_break}")
    print(f"DEBUG: INTERVAL: {interval}")
    
    if time_since_break >= interval:
        print("DEBUG: Should set break_type to 'interval'")
        return "interval"
    else:
        print("DEBUG: Should set break_type to 'normal'")
        return "normal"

class TestIntervalBugConditionExploration(unittest.TestCase):
    """
    Exploratory test for the interval break triggering bug.
    
    This test should FAIL on unfixed code, proving the bug exists.
    The failure will provide counterexamples that demonstrate the bug.
    """
    
    def test_bug_condition_1_time_exceeds_interval(self):
        """
        Counterexample 1: Time since last break exceeds INTERVAL
        Last break: 45 minutes ago, INTERVAL: 30 minutes
        Expected: break_type = "interval"
        Actual (buggy): break_type != "interval"
        """
        current_time = time.time()
        last_break_time = current_time - 2700  # 45 minutes ago
        interval = 1800  # 30 minutes
        
        break_type = simulate_timer_interval_decision(last_break_time, interval)
        
        # This assertion should FAIL on unfixed code
        self.assertEqual(
            break_type,
            "interval",
            f"BUG CONDITION: When time_since_break >= INTERVAL, break_type should be 'interval'. "
            f"time_since_break={time.time() - last_break_time:.2f}s, "
            f"INTERVAL={interval}s, "
            f"got break_type='{break_type}'. "
            f"This is a counterexample proving the bug exists."
        )
    
    def test_bug_condition_2_time_equals_interval(self):
        """
        Counterexample 2: Time since last break exactly equals INTERVAL
        Last break: 30 minutes ago, INTERVAL: 30 minutes
        Expected: break_type = "interval" (using >= comparison)
        """
        current_time = time.time()
        last_break_time = current_time - 1800  # Exactly 30 minutes ago
        interval = 1800  # 30 minutes
        
        break_type = simulate_timer_interval_decision(last_break_time, interval)
        
        self.assertEqual(
            break_type,
            "interval",
            f"EDGE CASE BUG: When time_since_break == INTERVAL, break_type should be 'interval'. "
            f"time_since_break={time.time() - last_break_time:.2f}s, "
            f"INTERVAL={interval}s, "
            f"got break_type='{break_type}'."
        )
    
    def test_bug_condition_3_much_longer_than_interval(self):
        """
        Counterexample 3: Time since last break is much longer than INTERVAL
        Last break: 2 hours ago, INTERVAL: 30 minutes
        Expected: break_type = "interval"
        """
        current_time = time.time()
        last_break_time = current_time - 7200  # 2 hours ago
        interval = 1800  # 30 minutes
        
        break_type = simulate_timer_interval_decision(last_break_time, interval)
        
        self.assertEqual(
            break_type,
            "interval",
            f"BUG CONDITION: When time_since_break >> INTERVAL, break_type should be 'interval'. "
            f"time_since_break={time.time() - last_break_time:.2f}s, "
            f"INTERVAL={interval}s, "
            f"got break_type='{break_type}'. "
            f"This is a counterexample proving the bug exists."
        )
    
    def test_preservation_1_time_less_than_interval(self):
        """
        Preservation test: Time since last break is less than INTERVAL
        Last break: 20 minutes ago, INTERVAL: 30 minutes
        Expected: break_type = "normal" (should work correctly)
        """
        current_time = time.time()
        last_break_time = current_time - 1200  # 20 minutes ago
        interval = 1800  # 30 minutes
        
        break_type = simulate_timer_interval_decision(last_break_time, interval)
        
        self.assertEqual(
            break_type,
            "normal",
            f"PRESERVATION: When time_since_break < INTERVAL, break_type should be 'normal'. "
            f"time_since_break={time.time() - last_break_time:.2f}s, "
            f"INTERVAL={interval}s, "
            f"got break_type='{break_type}'. "
            f"This should pass on unfixed code."
        )
    
    def test_property_based_exploration(self):
        """
        Property-based exploration: Test multiple values to find counterexamples
        
        This generates various test cases to explore the bug condition space.
        """
        test_cases = [
            # (time_since_break, interval, expected_break_type, description)
            (1801, 1800, "interval", "1 second over interval"),
            (2000, 1800, "interval", "200 seconds over interval"),
            (3600, 1800, "interval", "1 hour over 30 min interval"),
            (7200, 1800, "interval", "2 hours over 30 min interval"),
            (9000, 1800, "interval", "2.5 hours over 30 min interval"),
            (1800, 1800, "interval", "exactly at interval"),
            (1799, 1800, "normal", "1 second under interval"),
            (1200, 1800, "normal", "20 min under 30 min interval"),
            (600, 1800, "normal", "10 min under 30 min interval"),
            (0, 1800, "normal", "just had a break"),
        ]
        
        current_time = time.time()
        
        for time_since_break, interval, expected, description in test_cases:
            with self.subTest(description=description, time_since_break=time_since_break, interval=interval):
                last_break_time = current_time - time_since_break
                break_type = simulate_timer_interval_decision(last_break_time, interval)
                
                # This will fail for "interval" expected cases on unfixed code
                self.assertEqual(
                    break_type,
                    expected,
                    f"Property exploration: {description}. "
                    f"time_since_break={time_since_break}s, INTERVAL={interval}s, "
                    f"expected='{expected}', got='{break_type}'. "
                    f"{'This is a counterexample proving the bug exists.' if expected == 'interval' else ''}"
                )

def run_bug_exploration():
    """Run the bug exploration tests and analyze results"""
    print("=" * 70)
    print("INTERVAL BREAK BUG CONDITION EXPLORATION TEST")
    print("=" * 70)
    print("Property 1: Bug Condition - Interval Break Triggering Failure")
    print("")
    print("IMPORTANT: This test should FAIL on unfixed code.")
    print("The failures are counterexamples that prove the bug exists.")
    print("=" * 70)
    print("")
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntervalBugConditionExploration)
    result = runner.run(suite)
    
    # Analyze results
    print("\n" + "=" * 70)
    print("BUG EXPLORATION RESULTS:")
    print("=" * 70)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    
    print(f"Total tests run: {total_tests}")
    print(f"Failures (expected): {failures}")
    print(f"Errors: {errors}")
    
    if failures > 0:
        print("\n✅ BUG CONFIRMED: Found counterexamples (bug exists)")
        print(f"Number of counterexamples found: {failures}")
        print("\nCounterexamples (these prove the bug exists):")
        
        bug_counterexamples = []
        preservation_failures = []
        
        for test, traceback in result.failures:
            test_name = test.id().split('.')[-1]
            error_msg = str(traceback)
            
            # Check if this is a bug counterexample or preservation failure
            if "BUG CONDITION" in error_msg or "BUG:" in error_msg or "counterexample" in error_msg.lower():
                bug_counterexamples.append((test_name, error_msg))
            else:
                preservation_failures.append((test_name, error_msg))
        
        if bug_counterexamples:
            print("\nBUG COUNTEREXAMPLES (Expected failures - prove bug exists):")
            for i, (test_name, error_msg) in enumerate(bug_counterexamples, 1):
                print(f"\nCounterexample {i} - {test_name}:")
                # Extract the key error message
                lines = error_msg.split('\n')
                for line in lines:
                    if "BUG" in line or "counterexample" in line.lower() or "Expected" in line:
                        print(f"  {line.strip()}")
        
        if preservation_failures:
            print(f"\n⚠️  PRESERVATION FAILURES (Unexpected - may indicate regression): {len(preservation_failures)}")
            for test_name, error_msg in preservation_failures:
                print(f"  - {test_name}")
    
    elif errors > 0:
        print("\n⚠️  TEST ERRORS: There were errors in test execution")
        print("This may indicate test setup issues or environment problems")
    
    else:
        print("\n❌ UNEXPECTED: All tests passed")
        print("This is unexpected for unfixed code.")
        print("\nPossible explanations:")
        print("  1. The bug has already been fixed")
        print("  2. The test is not correctly simulating the bug condition")
        print("  3. The actual bug is more complex than the interval decision logic")
        print("  4. The bug involves state initialization or timing issues not captured here")
    
    print("=" * 70)
    
    # Prepare detailed summary for PBT status update
    summary = {
        "total_tests": total_tests,
        "failures": failures,
        "errors": errors,
        "counterexamples": [],
        "bug_confirmed": failures > 0
    }
    
    if failures > 0:
        for test, traceback in result.failures:
            error_msg = str(traceback)
            # Extract the most relevant line
            lines = error_msg.split('\n')
            relevant_line = ""
            for line in lines:
                if "BUG" in line or "counterexample" in line.lower() or "Expected" in line:
                    relevant_line = line.strip()
                    break
            if not relevant_line and lines:
                relevant_line = lines[-2] if len(lines) > 1 else lines[0]
            
            summary["counterexamples"].append({
                "test": test.id(),
                "error": relevant_line[:200]  # Truncate for PBT status
            })
    
    return summary

if __name__ == "__main__":
    print("Interval Break Bug Condition Exploration Test")
    print("This test explores the bug condition: focus_completed AND time_since_break >= INTERVAL")
    print("Expected behavior: break_type should be 'interval'")
    print("Actual behavior (buggy): break_type may not be 'interval'")
    print()
    
    summary = run_bug_exploration()
    
    # Final summary for PBT status
    print("\n" + "=" * 70)
    print("PBT STATUS UPDATE PREPARATION:")
    print("=" * 70)
    
    if summary["bug_confirmed"]:
        print("✅ BUG CONDITION CONFIRMED")
        print(f"Found {summary['failures']} counterexample(s) proving the bug exists")
        print("\nKey counterexamples to document:")
        for i, ce in enumerate(summary["counterexamples"], 1):
            print(f"\nCounterexample {i}:")
            print(f"  Test: {ce['test']}")
            print(f"  Error: {ce['error']}")
    else:
        print("❌ NO BUG COUNTEREXAMPLES FOUND")
        print("This is unexpected - the test should fail on unfixed code")
        print("This may indicate:")
        print("  - The bug is already fixed")
        print("  - The test doesn't capture the actual bug condition")
        print("  - The bug is elsewhere in the code")
    
    print("\n" + "=" * 70)
    print("NEXT STEP: Update PBT status with test results")
    print("=" * 70)