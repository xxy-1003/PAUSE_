# Implementation Plan: Timer + Session Core Module

## Overview

This implementation plan focuses on building a Streamlit MVP prototype for the Timer + Session Core Module. The plan follows a sequential approach starting with database setup, then implementing core managers (Timer, Session, Audio), followed by the Focus Mode Overlay, and finally integrating everything with state persistence. All tasks use Python as the implementation language.

## Tasks

- [~] 1. Set up project structure and SQLite database
  - Create project directory structure
  - Set up SQLite database with all required tables
  - Create database connection utilities
  - _Requirements: 6.1-6.17_

- [ ] 2. Implement Timer Manager
  - [-] 2.1 Create TimerManager class with core interface
    - Implement startTimer, pauseTimer, resumeTimer, completeTimer, cancelTimer methods
    - Add TimerMode enum (FOCUS, BREAK, INTERVAL_BREAK)
    - _Requirements: 1.1-1.10, 12.1_
  
  - [~] 2.2 Implement timer state machine and validation
    - Implement state transitions according to state machine diagram
    - Add duration constraints validation (Focus: 30-120 min, Break: 10-60 min, Interval Break: 1-30 min)
    - Add interval break scheduling based on frequency (20-60 min)
    - _Requirements: 1.6-1.10, 11.1_
  
  - [ ]* 2.3 Write unit tests for Timer Manager
    - Test state transitions and validation logic
    - Test duration constraints and interval break scheduling
    - _Requirements: 1.1-1.10_

- [ ] 3. Implement Session Manager
  - [-] 3.1 Create SessionManager class with core interface
    - Implement createSession, completeSession, getDailySessions, getSessionSummary methods
    - Add CompletionStatus enum (COMPLETED, CANCELLED, ABANDONED)
    - _Requirements: 2.1-2.10, 12.2_
  
  - [~] 3.2 Implement session analytics and goal tracking
    - Implement getTotalFocusTimeToday, getDailyGoalProgress, setDailyGoal methods
    - Add daily statistics calculation (total focus time, completed sessions)
    - Add goal progress tracking (1-10 sessions)
    - _Requirements: 2.4-2.7, 7.1-7.10_
  
  - [ ]* 3.3 Write unit tests for Session Manager
    - Test session creation and completion
    - Test daily statistics calculation
    - Test goal progress tracking
    - _Requirements: 2.1-2.10_

- [~] 4. Checkpoint - Core managers implementation
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Audio Manager
  - [-] 5.1 Create AudioManager class with core interface
    - Implement playSound, previewSound, uploadCustomSound, getAvailableSounds, setDefaultSound methods
    - Add AudioEvent enum (FOCUS_START, FOCUS_END, BREAK_START, BREAK_END, INTERVAL_BREAK_START, INTERVAL_BREAK_END)
    - Add SoundType enum (CLASSIC_BELL, NATURE_SOUND, ZEN_BELL, DIGITAL_BEEP, SOFT_CHIMES, CUSTOM)
    - _Requirements: 3.1-3.10, 12.3_
  
  - [~] 5.2 Implement audio file management and validation
    - Add built-in sound support (base64 encoded audio files)
    - Implement custom audio upload validation (mp3, wav only, 5MB max, 1-15 seconds)
    - Add volume control (0.0 to 1.0)
    - _Requirements: 3.2-3.8, 11.8-11.10_
  
  - [ ]* 5.3 Write unit tests for Audio Manager
    - Test sound playback functionality
    - Test custom file upload validation
    - Test volume control and event mapping
    - _Requirements: 3.1-3.10_

- [ ] 6. Implement Focus Mode Overlay
  - [-] 6.1 Create FocusOverlay class with core interface
    - Implement showOverlay, hideOverlay, updateDisplay, isOverlayVisible, blockInteractions methods
    - Create full-screen overlay component using Streamlit components
    - _Requirements: 4.1-4.10, 12.4_
  
  - [~] 6.2 Implement overlay display and interaction
    - Add remaining time display and current mode indicator
    - Implement pause/resume and exit buttons
    - Add overlay state synchronization with Timer Manager
    - _Requirements: 4.2-4.9_
  
  - [ ]* 6.3 Write unit tests for Focus Overlay
    - Test overlay display and visibility
    - Test interaction blocking functionality
    - Test timer state synchronization
    - _Requirements: 4.1-4.10_

- [~] 7. Checkpoint - UI components implementation
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement State Persistence
  - [-] 8.1 Create StateManager class with core interface
    - Implement saveActiveTimerState, loadActiveTimerState, clearActiveTimerState, hasActiveTimer methods
    - Integrate with st.session_state for real-time state management
    - _Requirements: 5.1-5.10, 12.5_
  
  - [~] 8.2 Implement SQLite persistence for active timer state
    - Add saveActiveTimerToSQLite, loadActiveTimerFromSQLite, clearActiveTimerFromSQLite methods
    - Implement state recovery across Streamlit reruns
    - Add state validation and integrity checks
    - _Requirements: 5.2-5.9, 8.1-8.3_
  
  - [ ]* 8.3 Write unit tests for State Manager
    - Test state save/load operations
    - Test SQLite persistence and recovery
    - Test state validation and error handling
    - _Requirements: 5.1-5.10_

- [ ] 9. Implement data models and validation
  - [ ] 9.1 Create TimerConfiguration data model
    - Implement validation for focusDuration (30-120), breakDuration (10-60), intervalBreakDuration (1-30), intervalBreakFrequency (20-60)
    - Add audioEnabled flag and defaultSounds mapping
    - _Requirements: 11.1_
  
  - [~] 9.2 Create TimerState data model
    - Implement validation for elapsedTime ≤ totalDuration, isPaused consistency, intervalBreakCount ≥ 0
    - Add timerId, mode, startTime, elapsedTime, totalDuration fields
    - _Requirements: 11.2-11.4_
  
  - [~] 9.3 Create SessionRecord data model
    - Implement validation for endTime ≥ startTime, focusDuration + breakDuration ≤ (endTime - startTime)
    - Add all analytics fields: pause_count, pause_duration, target_focus_duration, actual_focus_duration
    - _Requirements: 11.5-11.7_
  
  - [ ]* 9.4 Write property tests for data models
    - **Property 1: TimerConfiguration validation constraints**
    - **Property 2: TimerState consistency properties**
    - **Property 3: SessionRecord temporal constraints**
    - **Validates: Requirements 11.1-11.7**

- [~] 10. Checkpoint - Data layer implementation
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Integration and wiring
  - [~] 11.1 Wire Timer Manager with Audio Manager
    - Connect timer events to audio notifications
    - Implement event-to-sound mapping
    - _Requirements: 1.1-1.10, 3.1-3.10_
  
  - [~] 11.2 Wire Timer Manager with Session Manager
    - Connect timer completion to session creation
    - Implement session data collection from timer state
    - _Requirements: 1.1-1.10, 2.1-2.10_
  
  - [~] 11.3 Wire Timer Manager with Focus Overlay
    - Connect timer state changes to overlay updates
    - Implement overlay show/hide based on timer mode
    - _Requirements: 1.1-1.10, 4.1-4.10_
  
  - [~] 11.4 Wire all components with State Manager
    - Connect all managers to state persistence
    - Implement coordinated state save/load operations
    - _Requirements: 5.1-5.10, 8.1-8.10_
  
  - [ ]* 11.5 Write integration tests
    - Test end-to-end timer flow with all components
    - Test state persistence across Streamlit reruns
    - Test error handling and recovery scenarios
    - _Requirements: 8.1-8.10, 9.1-9.10_

- [ ] 12. Create Streamlit UI components
  - [~] 12.1 Create main timer control UI
    - Implement timer start/pause/resume/cancel controls
    - Add timer mode selection and duration configuration
    - Display remaining time and current mode
    - _Requirements: 1.1-1.10_
  
  - [~] 12.2 Create session dashboard UI
    - Implement daily statistics display
    - Add goal progress visualization
    - Show session history and summaries
    - _Requirements: 2.4-2.7, 7.1-7.10_
  
  - [~] 12.3 Create audio configuration UI
    - Implement sound selection for each event type
    - Add custom audio upload interface
    - Include volume controls and sound preview
    - _Requirements: 3.1-3.10_
  
  - [~] 12.4 Create application settings UI
    - Implement timer configuration settings
    - Add database management controls
    - Include data export functionality
    - _Requirements: 11.1-11.12, 7.10_

- [~] 13. Final checkpoint - Complete integration
  - Ensure all tests pass, ask the user if questions arise.
  - Verify all 7 core areas are implemented: Timer Manager, Session Manager, Audio Manager, Focus Mode Overlay, SQLite Database, State Persistence, Analytics-ready session storage

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Focus is on practical, implementable tasks for a Streamlit MVP prototype
- Excluded from tasks: Webhooks, Anonymous analytics, Connection pooling, CSP security, Timing attack protection, Cross-origin security, Multi-server architecture, Enterprise infrastructure
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from design document
- Unit tests validate specific examples and edge cases
- Implementation uses Python as specified by user

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["2.1", "3.1", "5.1", "6.1", "8.1", "9.1"] },
    { "id": 2, "tasks": ["2.2", "3.2", "5.2", "6.2", "8.2", "9.2", "9.3"] },
    { "id": 3, "tasks": ["2.3", "3.3", "5.3", "6.3", "8.3", "9.4"] },
    { "id": 4, "tasks": ["11.1", "11.2", "11.3", "11.4"] },
    { "id": 5, "tasks": ["11.5", "12.1", "12.2", "12.3", "12.4"] }
  ]
}
```