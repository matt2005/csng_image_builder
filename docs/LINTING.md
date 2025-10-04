# Code Linting Setup

This document describes the code linting setup for the crankshaft image builder project, following the coding standards outlined in `.github/copilot-instructions.md`.

## Scope

The linting tasks focus specifically on files within the stage directories:

- **Shell Scripts**: `crankshaft/stage*/files/**/*.sh`
- **Python Scripts**: `crankshaft/stage*/files/**/*.py`

These are the actual files that get deployed to the Raspberry Pi image, so maintaining their quality is critical.

## Available VS Code Tasks

The following tasks are configured in `.vscode/tasks.json`:

### Shell Script Linting (shellcheck)

- **Lint Shell Scripts (shellcheck)** - Lints all shell scripts in the `crankshaft/stage*/files/` directories
- **Lint Current Shell Script (shellcheck)** - Lints the currently open shell script file

### Python Script Linting (pylint)

- **Lint Python Scripts (pylint)** - Lints all Python scripts in the `crankshaft/stage*/files/` directories  
- **Lint Current Python Script (pylint)** - Lints the currently open Python script file

### Combined Tasks

- **Lint All Scripts (shellcheck + pylint)** - Runs both shell and Python linting in parallel (default build task)
- **Install Linting Tools** - Installs shellcheck and pylint on the system (Windows and Linux compatible)

## Cross-Platform Compatibility

The tasks are designed to work on both Windows and Linux:

### Windows
- Uses `bash` for file finding (requires Git Bash, WSL, or similar)
- PowerShell for tool installation
- Uses `python` command for pylint

### Linux
- Native `bash` for file operations
- `apt-get` for tool installation
- Uses `python3` command for pylint

## How to Use

### Using VS Code Tasks

1. **Open Command Palette**: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. **Run Task**: Type "Tasks: Run Task" and select it
3. **Choose Task**: Select one of the linting tasks from the list

### Keyboard Shortcuts

- **Run Default Build Task**: `Ctrl+Shift+B` (runs "Lint All Scripts")
- **Run Task**: `Ctrl+Shift+P` → "Tasks: Run Task"

### Manual Installation of Tools

If the tools aren't installed, run the "Install Linting Tools" task or install manually:

#### Windows
```powershell
# Install shellcheck (using scoop)
scoop install shellcheck

# Or using chocolatey
choco install shellcheck

# Install pylint
python -m pip install --user pylint
```

#### Linux
```bash
# Install shellcheck
sudo apt-get update
sudo apt-get install -y shellcheck

# Install pylint
python3 -m pip install --user pylint
```

## Configuration Files

### `.shellcheckrc`
- Configures shellcheck for bash shell scripts
- Follows Google Shell Style Guide requirements
- Disables checks not relevant for build scripts (SC1091, SC2034, SC2154)

### `.pylintrc`
- Configures pylint for Python 3.8+ compatibility
- Follows PEP 8 guidelines with project-specific adaptations
- Maximum line length: 88 characters
- Snake_case naming conventions
- Includes automotive/Raspberry Pi specific module ignores

## Coding Standards Enforced

### Shell Scripts
- **Style Guide**: Google Shell Style Guide
- **Error Handling**: Scripts should use `set -e` for error handling
- **Indentation**: 2 spaces
- **Naming**: kebab-case for script files, snake_case for variables
- **Comments**: Explain complex sections and script purpose

### Python Scripts  
- **Style Guide**: PEP 8
- **Python Version**: 3.8+ compatibility
- **Indentation**: 4 spaces
- **Naming**: snake_case for variables and functions, PascalCase for classes
- **Line Length**: 88 characters maximum
- **Imports**: Organized following PEP 8 import order

## Integration with Development Workflow

1. **Before Committing**: Run "Lint All Scripts" to check all deployment files
2. **During Development**: Use "Lint Current Script" for active file
3. **Code Reviews**: Ensure all linting checks pass
4. **CI/CD**: These tasks can be integrated into automated workflows

## Problem Matchers

The tasks include VS Code problem matchers that:
- Parse linter output and display issues in the Problems panel
- Enable click-to-navigate to error locations
- Provide severity indicators (error, warning, info, style)
- Show rule codes for reference

## File Patterns

The linting focuses on specific patterns to target only deployment files:

- `find crankshaft/stage*/files -name '*.sh' -type f` - Shell scripts in stage files
- `find crankshaft/stage*/files -name '*.py' -type f` - Python scripts in stage files

This ensures that only the files actually deployed to the Raspberry Pi image are linted, excluding build scripts and other auxiliary files.