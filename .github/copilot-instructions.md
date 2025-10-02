# Project Overview

This project creates a Raspberry Pi image based on pi-gen that boots into OpenAuto. It includes scripts and configurations to set up the environment, install necessary dependencies, and customize the system for optimal performance with OpenAuto.

The aim of this project is to provide a ready-to-use Raspberry Pi image that allows users to easily set up and run OpenAuto, a popular Android Auto head unit emulator, on their Raspberry Pi devices.

This project is intended for developers and enthusiasts who want to create a custom Raspberry Pi image with OpenAuto pre-installed, as well as for users who want a hassle-free way to get started with OpenAuto on their Raspberry Pi.

This project is maintained on GitHub, where users can find the source code, report issues, and contribute to the development of the project.

This project is a refactor of the repo found at https://github.com/opencardev/crankshaft which is a modified version of the original pi-gen project found at https://github.com/RPi-Distro/pi-gen. The original pi-gen project is maintained by the Raspberry Pi Foundation and is used to create the official Raspberry Pi OS images. The OpenCarDev Team has made significant modifications to pi-gen to create a custom image that boots directly into OpenAuto, this has made it difficult to keep up with changes made to the original pi-gen project. This refactor aims to separate the OpenAuto specific code from the pi-gen code, making it easier to maintain and update the project in the future.

## Folder Structure

- `/src`: Contains the source code.
- `/docs`: Contains documentation for the project, including specifications and user guides.

## Coding Standards

- For Python follow PEP 8 guidelines.
- For PowerShell scripts follow Microsoft PowerShell Style Guide.
- For shell scripts follow Google Shell Style Guide.
- Prefer using Python 3.x for all new scripts.
- Use comments to explain the purpose of complex code sections.
- Use meaningful variable and function names.
- Maintain consistent indentation (4 spaces for Python, 2 spaces for shell scripts).
- Write modular code with functions to enhance readability and reusability.
- Include error handling to manage exceptions gracefully.
- Write unit tests for critical functions to ensure code reliability.
- Use version control (e.g., Git) to track changes and collaborate effectively.
- Document code with docstrings and comments to explain functionality.
- Regularly review and refactor code to improve performance and maintainability.
- Follow best practices for security, such as validating user input and managing sensitive data appropriately.
- Use virtual environments for Python projects to manage dependencies.
- For shell scripts, use `set -e` to exit on errors and `set -u` to treat unset variables as errors.
- Use logging instead of print statements for better tracking and debugging.
- Ensure code is compatible with the target environment (e.g., Raspberry Pi OS version).
- Follow the DRY (Don't Repeat Yourself) principle to avoid code duplication.
- Use consistent naming conventions (e.g., snake_case for variables and functions in Python, kebab-case for shell scripts).
- Regularly update dependencies to their latest stable versions.
- Use linters (e.g., pylint for Python, shellcheck for shell scripts) to enforce coding standards.
- Write clear and concise commit messages that describe the changes made.
- Use branching strategies (e.g., feature branches, pull requests) for collaborative development.
- Conduct code reviews to ensure quality and adherence to standards.
- Maintain a changelog to document significant changes and updates to the project.
- Use existing libraries and frameworks where appropriate to avoid reinventing the wheel.
- Ensure the project is well-documented, including setup instructions, usage guides, and contribution guidelines.