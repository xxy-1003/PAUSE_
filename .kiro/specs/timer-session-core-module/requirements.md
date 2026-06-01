# Requirements Document

## Introduction

The Timer + Session Core Module is the foundational component of the PAUSE productivity application, providing timer management, session tracking, and audio notification capabilities. This module serves as the single source of truth for all timer and session data, enabling future analytics features including heatmaps, dashboards, and productivity reports.

## Glossary

- **Timer_Manager**: Component that manages all timer operations including focus sessions, breaks, and interval breaks with state transitions and persistence
- **Session_Manager**: Component that tracks completed sessions, manages daily goals, and provides session summaries for analytics
- **Audio_Manager**: Component that manages audio notifications for timer events with support for built-in sounds and custom uploads
- **Focus_Overlay**: Component that provides full-screen overlay during focus sessions to minimize distractions
- **State_Manager**: Component that maintains application state persistence across Streamlit reruns using st.session_state for active timer state
- **Timer_Mode**: Enumeration of timer states: FOCUS, BREAK, INTERVAL_BREAK
- **Audio_Event**: Enumeration of audio notification events: FOCUS_START, FOCUS_END, BREAK_START, BREAK_END, INTERVAL_BREAK_START, INTERVAL_BREAK_END
- **Sound_Type**: Enumeration of sound types: CLASSIC_BELL, NATURE_SOUND, ZEN_BELL, DIGITAL_BEEP, SOFT_CHIMES, CUSTOM
- **Completion_Status**: Enumeration of session completion states: COMPLETED, CANCELLED, ABANDONED
- **Timer_Configuration**: Data structure containing timer settings including durations and audio preferences
- **Timer_State**: Data structure representing active timer state including mode, elapsed time, and pause status
- **Session_Record**: Data structure containing complete session data for analytics and persistence
- **Audio_Configuration**: Data structure containing audio settings including sound mappings and volume levels

## Requirements

### Requirement 1: Timer Management

**User Story:** As a user, I want to manage focus sessions, breaks, and interval breaks, so that I can structure my work time effectively.

#### Acceptance Criteria

1. WHEN a user starts a timer with a specified duration and mode, THE Timer_Manager SHALL create a new timer with a unique TimerID
2. WHEN a user pauses an active timer, THE Timer_Manager SHALL stop the countdown and record the pause start time
3. WHEN a user resumes a paused timer, THE Timer_Manager SHALL continue the countdown from the remaining time
4. WHEN a timer completes its duration, THE Timer_Manager SHALL transition to the next appropriate mode and trigger completion events
5. WHEN a user cancels an active timer, THE Timer_Manager SHALL stop the timer and discard the session data
6. THE Timer_Manager SHALL enforce duration constraints: Focus (30-120 min), Break (10-60 min), Interval Break (1-30 min)
7. THE Timer_Manager SHALL schedule interval breaks based on frequency configuration (20-60 min)
8. THE Timer_Manager SHALL maintain accurate elapsed time accounting for pause periods
9. THE Timer_Manager SHALL provide real-time remaining time for active timers
10. THE Timer_Manager SHALL validate all timer state transitions according to the state machine diagram

### Requirement 2: Session Tracking

**User Story:** As a user, I want to track my completed sessions and daily progress, so that I can monitor my productivity and achieve my goals.

#### Acceptance Criteria

1. WHEN a timer completes successfully, THE Session_Manager SHALL create a session record with all relevant data
2. WHEN a session is created, THE Session_Manager SHALL assign a unique SessionID and record the start time
3. WHEN a session is completed, THE Session_Manager SHALL update the session record with end time and completion status
4. THE Session_Manager SHALL calculate daily statistics including total focus time and completed sessions
5. THE Session_Manager SHALL track progress toward daily goals (1-10 sessions)
6. WHEN a user sets a daily goal, THE Session_Manager SHALL store the goal and track progress against it
7. THE Session_Manager SHALL provide session summaries including focus duration, break duration, and interval break count
8. THE Session_Manager SHALL maintain session records with all analytics fields: pause_count, pause_duration, target_focus_duration, actual_focus_duration
9. THE Session_Manager SHALL serve as the single source of truth for all session data
10. THE Session_Manager SHALL provide efficient querying for real-time analytics calculation

### Requirement 3: Audio Notifications

**User Story:** As a user, I want audio notifications for timer events, so that I can stay informed without constantly checking the timer.

#### Acceptance Criteria

1. WHEN a timer event occurs (FOCUS_START, FOCUS_END, etc.), THE Audio_Manager SHALL play the configured sound for that event
2. THE Audio_Manager SHALL support built-in sound types: CLASSIC_BELL, NATURE_SOUND, ZEN_BELL, DIGITAL_BEEP, SOFT_CHIMES
3. WHEN a user uploads a custom audio file, THE Audio_Manager SHALL validate the file format (mp3, wav only)
4. WHEN a user uploads a custom audio file, THE Audio_Manager SHALL enforce size limits (5MB maximum)
5. WHEN a user uploads a custom audio file, THE Audio_Manager SHALL enforce duration limits (15 seconds maximum, 1 second minimum)
6. THE Audio_Manager SHALL allow users to preview sounds before selection
7. THE Audio_Manager SHALL allow users to set default sounds for each audio event type
8. THE Audio_Manager SHALL manage volume levels (0.0 to 1.0) for each sound configuration
9. WHEN audio playback fails, THE Audio_Manager SHALL fall back to system notifications
10. THE Audio_Manager SHALL prevent concurrent audio playback to avoid sound overlap

### Requirement 4: Focus Mode Overlay

**User Story:** As a user, I want a distraction-free environment during focus sessions, so that I can maintain concentration on my work.

#### Acceptance Criteria

1. WHEN a focus session starts, THE Focus_Overlay SHALL display a full-screen overlay
2. THE Focus_Overlay SHALL display remaining time and current timer mode
3. THE Focus_Overlay SHALL provide pause/resume and exit buttons
4. WHEN a user exits the overlay, THE Focus_Overlay SHALL close the overlay while the timer continues running in background
5. THE Focus_Overlay SHALL block interactions with the underlying application
6. THE Focus_Overlay SHALL update the display in real-time as the timer counts down
7. THE Focus_Overlay SHALL maintain visibility and functionality across browser interactions
8. THE Focus_Overlay SHALL provide clear visual feedback for overlay state changes
9. THE Focus_Overlay SHALL coordinate with Timer_Manager for timer state synchronization
10. THE Focus_Overlay SHALL handle browser window resizing and orientation changes gracefully

### Requirement 5: State Persistence

**User Story:** As a user, I want my timer state to persist across page refreshes and browser sessions, so that I don't lose progress unexpectedly.

#### Acceptance Criteria

1. THE State_Manager SHALL persist active timer state in st.session_state for real-time access
2. THE State_Manager SHALL save active timer state to SQLite active_timer table for recovery across Streamlit reruns
3. WHEN the application loads, THE State_Manager SHALL attempt to recover active timer state from SQLite
4. WHEN timer state changes, THE State_Manager SHALL update both st.session_state and SQLite active_timer table
5. WHEN a timer completes or is cancelled, THE State_Manager SHALL clear the active timer state from both storage locations
6. THE State_Manager SHALL validate state integrity during recovery operations
7. THE State_Manager SHALL handle state corruption by attempting recovery from st.session_state backup
8. THE State_Manager SHALL provide a consistent interface for state save/load operations
9. THE State_Manager SHALL coordinate between memory state and SQLite persistence
10. THE State_Manager SHALL maintain data consistency across all persistence layers

### Requirement 6: Database Schema

**User Story:** As a system architect, I want a well-defined database schema, so that data is stored efficiently and supports analytics requirements.

#### Acceptance Criteria

1. THE Database SHALL include a sessions table with all required analytics fields
2. THE sessions table SHALL include fields: session_id, user_id, date, start_time, end_time, focus_duration, break_duration, interval_breaks, pause_count, pause_duration, target_focus_duration, actual_focus_duration, completion_status, and configuration fields
3. THE sessions table SHALL enforce completion_status constraint: COMPLETED, CANCELLED, or ABANDONED
4. THE Database SHALL include an active_timer table for timer state persistence
5. THE active_timer table SHALL include fields: timer_id, user_id, mode, start_time, elapsed_time, total_duration, is_paused, pause_start_time, interval_break_count, last_interval_break_time
6. THE active_timer table SHALL enforce mode constraint: FOCUS, BREAK, or INTERVAL_BREAK
7. THE Database SHALL include audio_configurations table for audio settings
8. THE audio_configurations table SHALL enforce event_type constraint: FOCUS_START, FOCUS_END, BREAK_START, BREAK_END, INTERVAL_BREAK_START, INTERVAL_BREAK_END
9. THE audio_configurations table SHALL enforce volume constraint: 0.0 to 1.0 inclusive
10. THE Database SHALL include audio_files table for custom audio storage
11. THE audio_files table SHALL enforce file_type constraint: mp3 or wav only
12. THE audio_files table SHALL enforce file_size constraint: ≤ 5MB (5242880 bytes)
13. THE audio_files table SHALL enforce duration constraint: 1 to 15 seconds inclusive
14. THE Database SHALL include daily_goals table for goal tracking
15. THE daily_goals table SHALL enforce target_sessions constraint: 1 to 10 inclusive
16. ALL Database tables SHALL include appropriate indexes for efficient querying
17. ALL Database tables SHALL include created_at and updated_at timestamps for audit purposes

### Requirement 7: Analytics Compatibility

**User Story:** As a data analyst, I want session data structured for analytics, so that I can generate insights and reports without complex data transformation.

#### Acceptance Criteria

1. THE Session_Record SHALL include all fields necessary for real-time analytics calculation
2. THE sessions table SHALL contain sufficient data for calculating daily heatmaps without aggregation tables
3. THE sessions table SHALL contain sufficient data for calculating weekly charts without aggregation tables
4. THE sessions table SHALL contain sufficient data for generating productivity reports without aggregation tables
5. ALL analytics metrics SHALL be calculable directly from session records using efficient SQL queries
6. THE system SHALL support on-demand calculation of session completion rates from completion_status field
7. THE system SHALL support on-demand calculation of focus efficiency from target_focus_duration and actual_focus_duration fields
8. THE system SHALL support on-demand calculation of productivity trends from date and start_time fields
9. THE system SHALL support on-demand calculation of user behavior insights from configuration fields
10. THE system SHALL provide data export capability in CSV format for external analysis

### Requirement 8: Error Handling

**User Story:** As a user, I want the system to handle errors gracefully, so that I can continue using the application even when problems occur.

#### Acceptance Criteria

1. WHEN timer state corruption is detected, THE system SHALL attempt recovery from st.session_state backup
2. IF timer state recovery fails, THE system SHALL discard corrupted state and notify the user
3. WHEN audio playback fails, THE system SHALL fall back to system notification sounds
4. WHEN audio playback fails, THE system SHALL display visual notifications as backup
5. WHEN database connection is lost, THE system SHALL switch to in-memory cache for current session
6. WHEN database connection is lost, THE system SHALL queue session data for later persistence
7. WHEN file upload validation fails, THE system SHALL provide clear error messages to the user
8. WHEN state validation fails, THE system SHALL log the error for debugging purposes
9. WHEN unexpected errors occur, THE system SHALL maintain basic functionality where possible
10. ALL error conditions SHALL be logged with sufficient context for troubleshooting

### Requirement 9: Performance Requirements

**User Story:** As a user, I want the timer to be accurate and responsive, so that I can rely on it for time management.

#### Acceptance Criteria

1. THE Timer_Manager SHALL maintain timer accuracy within ±1 second per minute
2. THE system SHALL use high-resolution timers for precise counting
3. THE system SHALL compensate for browser throttling through background synchronization
4. THE in-memory cache SHALL implement LRU eviction policy for memory management
5. THE database SHALL include indexes on frequently queried columns (date, user_id)
6. THE system SHALL implement connection pooling for SQLite database operations
7. THE Audio_Manager SHALL preload frequently used sounds for faster playback
8. THE system SHALL implement audio caching with size limits for performance
9. THE Focus_Overlay SHALL update display efficiently without causing browser lag
10. THE system SHALL handle multiple active timers without significant performance degradation

### Requirement 10: Security Requirements

**User Story:** As a security-conscious user, I want my data protected and privacy respected, so that I can trust the application with my productivity information.

#### Acceptance Criteria

1. THE system SHALL isolate user session data in the database using user_id foreign keys
2. THE system SHALL validate all user-provided audio files before upload
3. THE system SHALL sanitize all user input to prevent injection attacks
4. THE system SHALL implement clear data retention and deletion policies
5. THE system SHALL provide user control over data export and deletion
6. THE system SHALL offer anonymous analytics option for aggregated data
7. THE system SHALL implement Content Security Policy for overlay functionality
8. THE system SHALL handle cross-origin resources securely
9. THE system SHALL protect against timing attacks in timer operations
10. ALL file uploads SHALL be validated for type, size, and content before storage

### Requirement 11: Data Validation

**User Story:** As a system administrator, I want data integrity enforced, so that analytics calculations are accurate and reliable.

#### Acceptance Criteria

1. WHEN saving Timer_Configuration, THE system SHALL validate: focusDuration (30-120), breakDuration (10-60), intervalBreakDuration (1-30), intervalBreakFrequency (20-60)
2. WHEN saving Timer_State, THE system SHALL validate: elapsedTime ≤ totalDuration
3. WHEN saving Timer_State, THE system SHALL validate: isPaused is true if pauseStartTime is set
4. WHEN saving Timer_State, THE system SHALL validate: intervalBreakCount ≥ 0
5. WHEN saving Session_Record, THE system SHALL validate: endTime ≥ startTime
6. WHEN saving Session_Record, THE system SHALL validate: focusDuration + breakDuration ≤ (endTime - startTime)
7. WHEN saving Session_Record, THE system SHALL validate: completionStatus is valid enum value
8. WHEN saving Audio_Configuration, THE system SHALL validate: volume (0.0 to 1.0 inclusive)
9. WHEN saving Audio_Configuration, THE system SHALL validate: filePath is valid for custom sounds
10. WHEN saving Audio_Configuration, THE system SHALL validate: name is non-empty
11. ALL data validation failures SHALL result in clear error messages to the user
12. ALL data validation SHALL occur before persistence to maintain database integrity

### Requirement 12: Integration Requirements

**User Story:** As a developer, I want clear integration points, so that I can extend the system with additional features and analytics.

#### Acceptance Criteria

1. THE Timer_Manager interface SHALL provide methods: startTimer, pauseTimer, resumeTimer, completeTimer, cancelTimer, getRemainingTime, getCurrentMode, isTimerActive
2. THE Session_Manager interface SHALL provide methods: createSession, completeSession, getDailySessions, getSessionSummary, getTotalFocusTimeToday, getDailyGoalProgress, setDailyGoal
3. THE Audio_Manager interface SHALL provide methods: playSound, previewSound, uploadCustomSound, getAvailableSounds, setDefaultSound
4. THE Focus_Overlay interface SHALL provide methods: showOverlay, hideOverlay, updateDisplay, isOverlayVisible, blockInteractions
5. THE State_Manager interface SHALL provide methods: saveActiveTimerState, loadActiveTimerState, clearActiveTimerState, hasActiveTimer
6. ALL component interfaces SHALL be well-documented with parameter types and return values
7. ALL data models SHALL be serializable to JSON for API compatibility
8. THE system SHALL provide webhook notifications for significant events (session completion, goal achievement)
9. THE system SHALL support future analytics engine integration through session data access
10. THE system SHALL maintain backward compatibility for data model changes where possible