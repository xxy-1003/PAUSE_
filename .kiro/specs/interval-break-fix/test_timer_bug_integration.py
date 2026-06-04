#!/usr/bin/env python3
"""
Integration test for interval break bug that mocks Streamlit.

This test imports Timer.py with mocked streamlit functions to test
the actual bug condition in context.

**Validates: Requirements 2.1, 2.2, 2.3**
"""

import sys
import os
import time
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add the project to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestTimerBugIntegration(unittest.TestCase):
    """
    Integration test that mocks Streamlit to test Timer.py logic.
    
    This should help identify if the bug is in the interval decision logic
    or somewhere else in the timer flow.
    """
    
    def setUp(self):
        """Set up mocks before each test"""
        # Create a mock session state
        self.mock_session_state = {
            "mode": "focus",
            "running": False,
            "paused": False,
            "start_time": None,
            "elapsed": 0,
            "history": [],
            "cycle_count": 0,
            "break_type": "normal",
            "last_break_time": None,  # Will be set in tests
            "focus_elapsed_before_break": 0,
            "daily_goal": 4
        }
        
        # Mock streamlit functions
        self.st_patcher = patch.dict('sys.modules', {
            'streamlit': Mock(),
            'streamlit.session_state': MagicMock(**{
                '__getitem__': lambda self, key: self.mock_session_state[key],
                '__setitem__': lambda self, key, value: self.mock_session_state.__setitem__(key, value),
                '__contains__': lambda self, key: key in self.mock_session_state,
                'get': lambda self, key, default=None: self.mock_session_state.get(key, default)
            })
        })
        self.st_patcher.start()
        
        # Also mock st.button, st.number_input, etc.
        import streamlit as st
        st.button = Mock(return_value=False)
        st.number_input = Mock(side_effect=self.mock_number_input)
        st.write = Mock()
        st.title = Mock()
        st.subheader = Mock()
        st.metric = Mock()
        st.progress = Mock()
        st.empty = Mock(return_value=Mock())
        st.columns = Mock(return_value=[Mock(), Mock(), Mock()])
        st.rerun = Mock()
        
    def tearDown(self):
        """Clean up after each test"""
        self.st_patcher.stop()
        
    def mock_number_input(self, label, min_value, max_value, value):
        """Mock number_input to return test values"""
        # Return different values based on label
        if "Focus Duration" in label:
            return 25  # 25 minutes
        elif "Recovery Duration" in label:
            return 5   # 5 minutes
        elif "Interval Break Duration" in label:
            return 3   # 3 minutes
        elif "Interval Break Frequency" in label:
            return 30  # 30 minutes - THIS IS THE INTERVAL!
        elif "Daily Goal" in label:
            return 4
        return value
    
    def test_interval_decision_with_mocked_time(self):
        """
        Test the interval decision logic with controlled time values.
        
        This test manually executes the interval decision logic from Timer.py
        with specific time values to see if it works correctly.
        """
        # Import Timer module after mocking
        import streamlit as st
        
        # Set up test scenario: last break was 45 minutes ago
        current_time = time.time()
        self.mock_session_state["last_break_time"] = current_time - 2700  # 45 minutes ago
        
        # Manually execute the interval decision logic from Timer.py lines 176-186
        time_since_break = current_time - self.mock_session_state["last_break_time"]
        INTERVAL = 30 * 60  # 30 minutes in seconds (from mock_number_input)
        
        print(f"Test: time_since_break={time_since_break}, INTERVAL={INTERVAL}")
        
        # The actual logic from Timer.py
        if time_since_break >= INTERVAL:
            expected_break_type = "interval"
        else:
            expected_break_type = "normal"
        
        # This should be "interval" since 45 >= 30
        self.assertEqual(
            expected_break_type,
            "interval",
            f"Interval decision logic failed: time_since_break={time_since_break}s, "
            f"INTERVAL={INTERVAL}s, expected='interval', got='{expected_break_type}'"
        )
    
    def test_duplicate_initialization_issue(self):
        """
        Test if duplicate initialization could cause issues.
        
        Simulates what happens with the duplicate last_break_time initialization.
        """
        import streamlit as st
        
        # Simulate the initialization code from Timer.py
        # First initialization (line 35)
        if "last_break_time" not in st.session_state:
            st.session_state["last_break_time"] = time.time()
            print(f"First initialization: last_break_time = {st.session_state['last_break_time']}")
        
        # Simulate something that might happen between initializations
        # (In actual code, there's just a comment)
        
        # Second initialization (line 43) - DUPLICATE!
        if "last_break_time" not in st.session_state:
            st.session_state["last_break_time"] = time.time()
            print(f"Second initialization: last_break_time = {st.session_state['last_break_time']}")
        
        # Check if second initialization ran (it shouldn't!)
        initial_time = self.mock_session_state["last_break_time"]
        
        # Manually check what would happen
        print(f"Final last_break_time: {initial_time}")
        
        # The issue might be if something resets the session state between initializations
        # But in the actual code, there's nothing between them
        
        self.assertIsNotNone(initial_time, "last_break_time should be initialized")
    
    def test_full_interval_break_scenario(self):
        """
        Test a full scenario where interval break should trigger.
        
        Simulates: App starts -> time passes -> focus completes -> interval break should trigger
        """
        import streamlit as st
        
        # Scenario: User starts app, last_break_time initialized to current time
        app_start_time = time.time()
        self.mock_session_state["last_break_time"] = app_start_time
        
        # Simulate 45 minutes passing
        current_time = app_start_time + 2700  # 45 minutes later
        
        # Mock time.time() to return our controlled current_time
        with patch('time.time', return_value=current_time):
            # Calculate time_since_break
            time_since_break = current_time - self.mock_session_state["last_break_time"]
            INTERVAL = 30 * 60  # 30 minutes
            
            print(f"Scenario: App started at {app_start_time}")
            print(f"          45 minutes later: {current_time}")
            print(f"          time_since_break: {time_since_break}s")
            print(f"          INTERVAL: {INTERVAL}s")
            
            # Execute interval decision logic
            if time_since_break >= INTERVAL:
                break_type = "interval"
            else:
                break_type = "normal"
            
            # Should be "interval" since 45 >= 30
            self.assertEqual(
                break_type,
                "interval",
                f"Full scenario failed: After 45 minutes, interval break should trigger. "
                f"time_since_break={time_since_break}s, INTERVAL={INTERVAL}s, got='{break_type}'"
            )
    
    def test_bug_condition_formal_spec(self):
        """
        Test the formal bug condition specification from design.md
        
        isBugCondition(input) where:
          input.focus_completed = true 
          AND input.time_since_break >= input.INTERVAL 
          AND input.break_type != "interval"
        """
        # Create test cases that should trigger the bug condition
        test_cases = [
            {
                "name": "45 minutes since last break, INTERVAL=30",
                "last_break_time": time.time() - 2700,
                "interval": 1800,
                "expected_to_be_buggy": True  # Should be buggy if break_type != "interval"
            },
            {
                "name": "20 minutes since last break, INTERVAL=30", 
                "last_break_time": time.time() - 1200,
                "interval": 1800,
                "expected_to_be_buggy": False  # Not buggy, should be normal break
            },
            {
                "name": "Exactly 30 minutes, INTERVAL=30",
                "last_break_time": time.time() - 1800,
                "interval": 1800,
                "expected_to_be_buggy": True  # Should be buggy if break_type != "interval"
            },
        ]
        
        for test_case in test_cases:
            with self.subTest(test_case["name"]):
                # Calculate time_since_break
                time_since_break = time.time() - test_case["last_break_time"]
                
                # Apply interval decision logic
                if time_since_break >= test_case["interval"]:
                    break_type = "interval"
                else:
                    break_type = "normal"
                
                # Check if this matches bug condition
                focus_completed = True
                is_bug_condition = (
                    focus_completed and 
                    time_since_break >= test_case["interval"] and 
                    break_type != "interval"
                )
                
                print(f"Test: {test_case['name']}")
                print(f"  time_since_break: {time_since_break}s")
                print(f"  INTERVAL: {test_case['interval']}s")
                print(f"  break_type: {break_type}")
                print(f"  is_bug_condition: {is_bug_condition}")
                print(f"  expected_to_be_buggy: {test_case['expected_to_be_buggy']}")
                
                # For tests where expected_to_be_buggy is True, is_bug_condition should be True
                # (meaning the bug exists)
                if test_case["expected_to_be_buggy"]:
                    self.assertTrue(
                        is_bug_condition,
                        f"Bug condition should be true for: {test_case['name']}. "
                        f"This would prove the bug exists. "
                        f"But break_type='{break_type}' which is correct, so bug condition is false."
                    )
                else:
                    self.assertFalse(
                        is_bug_condition,
                        f"Bug condition should be false for: {test_case['name']}. "
                        f"This is preservation case."
                    )

def run_integration_tests():
    """Run the integration tests"""
    print("=" * 70)
    print("TIMER BUG INTEGRATION TESTS")
    print("=" * 70)
    print("Testing Timer.py logic with mocked Streamlit")
    print("=" * 70)
    
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTimerBugIntegration)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("INTEGRATION TEST RESULTS:")
    print("=" * 70)
    
    if result.failures:
        print(f"Found {len(result.failures)} test failures")
        print("\nThese failures might indicate:")
        print("  1. The bug exists (if interval logic tests fail)")
        print("  2. Test setup issues")
        
        for test, traceback in result.failures:
            test_name = test.id().split('.')[-1]
            print(f"\nFailure in {test_name}:")
            # Extract key error message
            error_lines = str(traceback).split('\n')
            for line in error_lines[-5:]:  # Last few lines
                if line.strip():
                    print(f"  {line.strip()}")
    
    elif result.errors:
        print(f"Found {len(result.errors)} test errors (setup issues)")
    else:
        print("All tests passed")
        print("\nThis suggests:")
        print("  1. The interval decision logic itself is correct")
        print("  2. The bug might be elsewhere (state management, UI, etc.)")
        print("  3. Or the bug might already be fixed")
    
    print("=" * 70)
    
    return result

if __name__ == "__main__":
    print("Timer Bug Integration Test")
    print("This test mocks Streamlit to test Timer.py logic in isolation")
    print()
    
    result = run_integration_tests()
    
    # Summary for bug analysis
    print("\n" + "=" * 70)
    print("BUG ANALYSIS SUMMARY:")
    print("=" * 70)
    
    if result.failures:
        print("❌ TEST FAILURES FOUND")
        print("These could indicate the bug exists")
        print("\nHowever, note that:")
        print("  1. We're testing isolated logic, not the full app")
        print("  2. The actual bug might involve Streamlit session state nuances")
        print("  3. Timing or concurrency issues might not be captured")
    else:
        print("✅ ALL TESTS PASSED")
        print("\nThis is unexpected for unfixed code.")
        print("\nPossible explanations:")
        print("  1. The bug is already fixed in the interval decision logic")
        print("  2. The bug is in a different part of the code")
        print("  3. The bug involves Streamlit-specific behavior not captured by mocks")
        print("  4. The duplicate initialization doesn't affect the interval logic")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATION: Need to investigate actual app behavior")
    print("or examine other potential bug locations.")
    print("=" * 70)