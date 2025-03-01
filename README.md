[![progress-banner](https://backend.codecrafters.io/progress/shell/0f602f72-de0c-40a4-83de-540b08898632)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

# Custom Python Shell

This is a custom POSIX-compliant shell built using Python. It provides a command-line interface that executes commands, manages processes, and supports both built-in and external commands. The shell is designed to mimic many common functionalities of typical Unix-like shells such as Bash.

## Features

- **Prompting**: Displays a shell prompt for user interaction.
- **Command Handling**: Executes commands entered by the user and handles errors for invalid commands.
- **Built-in Commands**:
  - `cd` (Change directory)
  - `pwd` (Print working directory)
  - `echo` (Print text to the terminal)
  - `type` (Check type of a command - builtin, executable file, etc.)
  - `exit` (Exit the shell)
- **Command Parsing**: Handles single and double quotes for argument parsing and escapes special characters using backslashes.
- **Redirection**:
  - Redirects `stdout` and `stderr` to files.
  - Appends `stdout` and `stderr` to files.
- **Autocompletion**: Supports autocompletion for built-in commands and executable commands.
- **Program Execution**: Executes external programs and supports arguments.

## Features Implemented

### Core Features
- **Prompt**: Displays a command prompt.
- **REPL (Read-Eval-Print Loop)**: Continuously accepts and executes commands until the user exits.
- **Exit Command**: Exits the shell gracefully.

### Built-in Commands
- **Echo**: Prints a string or variable to the console.
- **Type**: Checks the type of the provided command (whether it's a built-in or an executable).
- **PWD**: Prints the current working directory.
- **CD**: Changes the current directory. Supports:
  - Absolute paths
  - Relative paths
  - Home directory

### Advanced Features
- **Quoting**: Handles different types of quoting for arguments:
  - Single quotes: `echo 'Hello World'`
  - Double quotes: `echo "Hello World"`
  - **Backslash handling**:
    - Outside quotes
    - Inside single and double quotes
  - Executing quoted executables.

### Redirection
- **Redirect stdout**: Allows redirecting the output of a command to a file.
  - `echo "Hello World" > output.txt`
- **Redirect stderr**: Redirects error messages to a file.
  - `command_that_fails 2> error.log`
- **Append stdout**: Appends command output to an existing file.
  - `echo "Hello Again" >> output.txt`
- **Append stderr**: Appends error messages to an existing file.
  - `command_that_fails 2>> error.log`

### Autocompletion
- **Builtin Completion**: Supports autocompletion for built-in commands.
- **Executable Completion**: Autocompletes executable files and commands.
- **Multiple Completions**: Handles multiple autocompletion suggestions.
- **Partial Completions**: Supports partial completions and fuzzy matching.

## Installation

### Prerequisites
- Python 3.x

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/custom-python-shell.git
    ```
2. Navigate into the project directory:
   ```bash
   cd custom-python-shell
   ```
3. Run the shell script:
   ```bash
   python3 shell.py
   ```
## Usage

Once the shell starts, you can type your commands. Some examples:

- `echo "Hello, World!"`: Prints "Hello, World!"
- `cd /path/to/directory`: Changes the current directory.
- `pwd`: Prints the current working directory.
- `type ls`: Checks if `ls` is a built-in or an executable.
- `exit`: Exits the shell.

### Redirection Examples:
- `echo "This is output" > output.txt`: Redirects the output to `output.txt`.
- `command_that_fails 2> error.log`: Redirects stderr to `error.log`.
- `echo "Appending output" >> output.txt`: Appends stdout to `output.txt`.
- `command_that_fails 2>> error.log`: Appends stderr to `error.log`.

### Autocompletion:
Start typing a command and press `Tab` to autocomplete. Try it with commands like `cd`, `echo`, or any executable file in your `$PATH`.
