# Detailed Design for Permutation Calculator App

## Overview
This application will compute permutations based on user-inputted numbers. The system is divided into two main components: the frontend (Gradio UI) and the backend (business logic, APIs, database interactions).

## Module Structure

### Module: permutation_calculator

#### Classes and Functions

1. **Class: PermutationCalculator**
   - **Purpose**: Handles the logic for calculating permutations.
   - **Methods**:
     - `__init__(self)`: Initializes any required attributes.
     - `calculate_permutations(self, n: int) -> List[List[int]]`: 
       - Accepts an integer `n` and returns a list of lists representing all possible permutations of numbers from `0` to `n-1`.
     - `factorial(self, number: int) -> int`: 
       - Computes and returns the factorial of a number, used for calculations of permutations.
     - `get_permutation_count(self, n: int) -> int`: 
       - Computes and returns the total number of permutations for `n`.

2. **Class: UserInputHandler**
   - **Purpose**: Manages user interactions and input validation.
   - **Methods**:
     - `__init__(self)`: Initializes needed attributes.
     - `get_user_input(self) -> int`: 
       - Prompts the user for a number and returns the validated integer input.
     - `validate_input(self, user_input: str) -> int`: 
       - Validates the user input and converts it to an integer, raising an exception for invalid input.
  
3. **Class: ResponseFormatter**
   - **Purpose**: Formats the output data to be user-friendly.
   - **Methods**:
     - `__init__(self)`: No specific attributes needed for initialization.
     - `format_permutations(self, permutations: List[List[int]]) -> str`: 
       - Accepts a list of permutations and returns a formatted string for display.
     - `format_error(self, message: str) -> str`: 
       - Formats and returns an error message to be displayed to the user.

4. **Class: GradioUI**
   - **Purpose**: Interface for Gradio UI to connect frontend and backend logic.
   - **Methods**:
     - `__init__(self, permutation_calculator: PermutationCalculator, input_handler: UserInputHandler, formatter: ResponseFormatter)`: 
       - Initializes the UI with required dependency injections.
     - `launch_interface(self)`: 
       - Sets up the Gradio interface elements such as text input and output display.
     - `process_input(self, user_input: str) -> str`: 
       - Invokes methods from the backend classes to compute and return the permutations based on user input.

## Data Flow

- User opens the Gradio interface and inputs a number.
- `GradioUI` calls `UserInputHandler` to validate and retrieve user input.
- Valid input is forwarded to `PermutationCalculator` to compute permutations.
- The resulting permutations are formatted using `ResponseFormatter`.
- The formatted output is displayed back on the Gradio interface.

## Database Interactions
- As this application does not require persistent storage, no database interactions are defined. Data handling and computation are performed in memory.

## Frontend and Backend Allocation
- **Frontend (Gradio UI)**:
  - Managed by `GradioUI` class which handles all user interactions and display.
  
- **Backend (Business Logic, APIs)**:
  - `PermutationCalculator`, `UserInputHandler`, and `ResponseFormatter` handle all computations and data processing.

The overall design is structured to provide clear separation of concerns, with distinct classes handling user input, computation, and output formatting. This will facilitate maintainable and scalable code.