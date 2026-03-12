# Project Rules

This document defines the coding and architecture rules
that AI agents must follow when implementing tasks.

These rules override default AI behavior.

---

# Architecture Rules

The project follows a modular architecture.

Rules:

- Each module must have a single responsibility.
- Services must not access browser APIs directly unless specified.
- Cross-module calls must go through service interfaces.

Example:

Background → CaptureService → FileNameService → DownloadService

Direct coupling between modules is prohibited.

---

# Code Style Rules

Language:
TypeScript

Rules:

- Use ES modules
- Use async/await instead of callbacks
- Avoid global variables
- Prefer pure functions where possible

Naming conventions:

Classes:
PascalCase

Functions:
camelCase

Files:
PascalCase.ts for services

Example:

CaptureService.ts
FileNameService.ts

---

# Chrome Extension Rules

All browser API calls must be isolated.

Allowed locations:

src/services
src/background

UI code must not call Chrome APIs directly.

---

# File Structure Rules

Project structure must remain consistent.

src/

background/
services/
options/


New files must follow this structure.

---

# Dependency Rules

Modules must follow this dependency order.

UI
↓
Background
↓
Services

Services must not depend on UI modules.

---

# Error Handling Rules

All service functions must:

- Return structured results
- Avoid throwing uncaught exceptions

Example result format:

{
  success: true,
  data: ...
}

---

# AI Implementation Rules

When implementing a task:

1. Read architecture.md
2. Follow module boundaries
3. Do not change unrelated files
4. Do not refactor entire modules unless required
5. Keep implementation minimal

---

# Testing Rules

When adding logic:

- Add unit tests when possible
- Ensure project builds successfully

Commands:

dotnet build
dotnet test

AI must fix build failures before completing tasks.

---

# Task Execution Rules

For each task:

1. Implement feature
2. Build project
3. Run tests
4. Fix errors

If build fails after multiple attempts:

Create a bug ticket.

---

# Forbidden Actions

AI must not:

- Rewrite the entire project
- Modify configuration files unnecessarily
- Change architecture without explicit task instruction
- Remove existing modules