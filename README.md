# To run the app 

In one terminal, enter: 
npm start (this will start the user-interface)

In other terminal, enter: 
python ulog_handler.py

project definition doc (WIP):
https://docs.google.com/document/d/1pTCY0YA-20DkAHzHnJZbEh7n0wO2gGdwymcTZyWWrAE/edit?usp=sharing

trying to automate tests in: https://docs.google.com/spreadsheets/d/1WgXU_PrZwft7PrXGb5A6-wC0A0WEi-KLgqL1SpU1dvw/edit#gid=218938510

next steps: 
- validate fastforward flight timestamps logic 
- implement: actuator control, battery, gps 
- have the code read threshold and topic names in ulog form a file, and store the read values into a "Configuration Dictionary"

## Implementation Plan for Enhancements

### Step 1: Configuration Management
- **Goal**: Externalize configuration settings.
- **Action**: Create a configuration file or use environment variables.
- **Expected Outcome**: Simplified management and deployment.

### Step 2: Separate Concerns
- **Goal**: Break down the `BatteryStatus` class into smaller classes.
- **Action**: Create `VoltageChecker`, `CurrentChecker`, etc.
- **Expected Outcome**: Improved modularity and readability.

### Step 3: Dependency Injection
- **Goal**: Enhance testability and modularity.
- **Action**: Refactor classes to accept dependencies via constructors.
- **Expected Outcome**: Easier testing and maintenance.

### Step 4: Asynchronous Processing
- **Goal**: Improve responsiveness and scalability.
- **Action**: Implement asynchronous features in Flask routes.
- **Expected Outcome**: Better performance under load.

### Step 5: Error Handling and Logging
- **Goal**: Increase robustness and debuggability.
- **Action**: Implement standardized error handling and logging.
- **Expected Outcome**: Easier monitoring and troubleshooting.

### Step 6: Automated Testing
- **Goal**: Ensure reliability and facilitate modifications.
- **Action**: Develop comprehensive testing suites.
- **Expected Outcome**: Early detection of regressions.

### Step 7: Use Service Layer
- **Goal**: Decouple business logic from web handling logic.
- **Action**: Introduce a service layer.
- **Expected Outcome**: Centralized and reusable business logic.

Each step is designed to build upon the previous, ensuring a smooth transition and minimal disruption during development.
- have the code read threshold and topic names in ulog form a file, and store the read values into a "Configuration Dictionary"
