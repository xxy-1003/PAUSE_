# Bugfix Requirements Document

## Introduction

This bugfix addresses an issue in the Streamlit Pomodoro timer where interval breaks are not triggering correctly. When a user completes a focus session and enough time has passed since the last break (as defined by the INTERVAL setting), the system should automatically trigger an interval break. Currently, the interval break logic fails to activate even when `time_since_break >= INTERVAL`, causing the system to always fall back to normal breaks.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN a user completes a focus session AND time_since_break >= INTERVAL THEN the system does NOT set break_type to "interval"
1.2 WHEN a user completes a focus session AND time_since_break >= INTERVAL THEN the system does NOT use INTERVAL_BREAK_DURATION for the next break
1.3 WHEN a user completes a focus session AND time_since_break >= INTERVAL THEN the system falls back to normal break path instead of interval break path

### Expected Behavior (Correct)

2.1 WHEN a user completes a focus session AND time_since_break >= INTERVAL THEN the system SHALL set break_type to "interval"
2.2 WHEN a user completes a focus session AND time_since_break >= INTERVAL THEN the system SHALL use INTERVAL_BREAK_DURATION for the next break
2.3 WHEN a user completes a focus session AND time_since_break >= INTERVAL THEN the system SHALL enter the interval break path correctly

### Unchanged Behavior (Regression Prevention)

3.1 WHEN a user completes a focus session AND time_since_break < INTERVAL THEN the system SHALL CONTINUE TO set break_type to "normal"
3.2 WHEN a user completes a focus session AND time_since_break < INTERVAL THEN the system SHALL CONTINUE TO use BREAK_DURATION for the next break
3.3 WHEN interval break is NOT triggered THEN the system SHALL CONTINUE TO function normally with all other timer logic unchanged
3.4 WHEN in any timer state other than focus completion THEN the system SHALL CONTINUE TO maintain all existing state transitions and UI behavior
3.5 WHEN using manual mode switching THEN the system SHALL CONTINUE TO switch between focus and break modes correctly