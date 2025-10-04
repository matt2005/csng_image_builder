---
mode: agent
model: Claude Sonnet 4 (copilot)
---

Add Vscode tasks to lint shell scripts using shellcheck and to lint python scripts using pylint. Use the coding standards in .github/copilot-instructions.md as a guide.
Only lint/format files under the files folders crankshaft/stage*/files/**/*.sh and crankshaft/stage*/files/**/*.py
The pylint task should use a pylintrc file in the root of the repository for configuration.
Make sure the tasks work on both Windows and Linux.