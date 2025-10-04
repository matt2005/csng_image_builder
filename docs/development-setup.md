# Development Environment Setup

## Code Quality Tools

This project includes automated linting and code quality checks for both shell scripts and Python files in the deployment configuration.

### VS Code Tasks

The following VS Code tasks are available for code quality checking:

#### 1. Lint Shell Scripts (shellcheck)
- **Purpose**: Checks shell scripts for syntax errors, style issues, and best practices
- **Target Files**: `crankshaft/stage*/files/**/*.sh`
- **Tool**: ShellCheck
- **Task ID**: `Lint Shell Scripts (shellcheck)`

#### 2. Lint Python Scripts (pylint)
- **Purpose**: Checks Python scripts for code quality, style, and potential issues
- **Target Files**: `crankshaft/stage*/files/**/*.py`
- **Tool**: Pylint
- **Task ID**: `Lint Python Scripts (pylint)`

#### 3. Lint Current Shell Script
- **Purpose**: Lints the currently open shell script file
- **Task ID**: `Lint Current Shell Script (shellcheck)`

#### 4. Lint Current Python Script
- **Purpose**: Lints the currently open Python script file
- **Task ID**: `Lint Current Python Script (pylint)`

#### 5. Lint All Scripts
- **Purpose**: Runs both shell and Python linting in parallel
- **Task ID**: `Lint All Scripts (shellcheck + pylint)`
- **Default**: This is the default build task (Ctrl+Shift+P -> "Tasks: Run Build Task")

### Cross-Platform Support

The tasks are configured to work on both Windows and Linux:

- **Windows**: Uses PowerShell with `Get-ChildItem` for file discovery
- **Linux**: Uses bash with `find` for file discovery

### Tool Installation

#### Windows
- **Python/Pylint**: Automatically managed through VS Code Python environment
- **ShellCheck**: Downloaded automatically to `tools/shellcheck.exe` (first run may require manual download)

#### Linux
- **Python/Pylint**: Install via package manager: `sudo apt install python3-pylint`
- **ShellCheck**: Install via package manager: `sudo apt install shellcheck`

### Configuration Files

- **`.pylintrc`**: Pylint configuration for Python code style and quality rules
- **`.shellcheckrc`**: ShellCheck configuration for shell script analysis

### Running Linting

1. **Via VS Code Command Palette**:
   - `Ctrl+Shift+P` → "Tasks: Run Task" → Select desired linting task

2. **Via Keyboard Shortcut**:
   - `Ctrl+Shift+B` → Runs the default "Lint All Scripts" task

3. **Via VS Code Terminal**:
   - Open terminal and run individual commands as needed

### Problem Matcher Integration

The tasks include problem matchers that:
- Parse linting output and display issues in VS Code's Problems panel
- Provide clickable links to jump directly to problematic code
- Show severity levels (error, warning, info, style)
- Include rule codes for reference

### File Targeting

The linting tasks specifically target deployment files in:
```
crankshaft/stage*/files/**/*.(sh|py)
```

This focuses on the actual deployment scripts while excluding build artifacts and other non-deployment code.

### Setup Instructions

1. **First Time Setup**:
   - Open the project in VS Code
   - Python environment should be configured automatically
   - For Windows: ShellCheck will be downloaded on first use
   - For Linux: Install tools via package manager

2. **Running Lints**:
   - Use `Ctrl+Shift+B` to run all linting tasks
   - Check the Problems panel for any issues found
   - Fix issues and re-run linting to verify fixes

3. **Customization**:
   - Modify `.pylintrc` to adjust Python linting rules
   - Modify `.shellcheckrc` to adjust shell script rules
   - Update task configurations in `.vscode/tasks.json` as needed