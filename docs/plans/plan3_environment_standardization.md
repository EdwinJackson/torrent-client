# Plan 3: Align environments

## Overview
This plan ensures consistent and reliable environment setup across the project, focusing on maintaining stable Python 3.9 as the primary version.

## Current Issue
- Inconsistent Python environments (3.9 works, 3.14 fails)
- No centralized Python version management
- Potential dependency conflicts between environments

## Solution Approach

### 3.1 Python version selection
- Maintain Python 3.9 as the official project version (Plan 2 strategy)
- Document Python 3.10+ testing results when available
- Clearly define supported Python versions (3.9)

### 3.2 Environment standardization
**3.2.1 Poetry Configuration**
```toml
[tool.poetry.dependencies]
python = ">=3.9,<3.10"
# other dependencies as defined
```

**3.2.2 Runtime Configuration**
- Update any CI/CD pipeline files to use Python 3.9
- Update README with supported Python version
- Add version check in application code

### 3.3 Environment management tools
- Use mise for Python version management (currently configured)
- Ensure `.python-version` file is present with "3.9"
- Document environment setup process in README

### 3.4 Testing and validation
- Add Python version tests to CI/CD (3.9)
- Verify peer-to-peer compatibility
- Test against future Python versions when available

### 3.5 Dependency management
- Run `poetry lock --regenerate` with Python 3.9
- Ensure all dependencies are compatible with Python 3.9
- Update lock file for consistency

### 3.6 Documentation updates
- Update README with supported Python version (3.9)
- Add environment setup instructions
- Document Python 3.14 incompatibility
- Provide migration path for future upgrades

## Acceptance Criteria
- Project has Python 3.9 as the well-defined supported version
- Environment setup is consistent and reproducible
- CI/CD tests pass on Python 3.9
- Clear documentation for developers on environment setup
- No environment-specific runtime errors

## Risk Mitigation
- Maintain backward compatibility
- Document incompatibilities with newer Python versions
- Keep working fallback for critical use cases
- Document known limitations with Python 3.10+

## Implementation Steps
1. Update pyproject.toml with Python version constraint (3.9)
2. Run `poetry lock --regenerate` to resolve dependencies
3. Update environment files (.python-version, etc.)
4. Update documentation (README, CI configs)
5. Run comprehensive tests on Python 3.9
6. Document Python version strategy and migration path

## Status
COMPLETE — 2026-09-22. `requires-python = ">=3.9,<3.10"`, `.python-version` = 3.9, `mise.toml` 3.9, runtime guard in `client.py` (fires on 3.10+, verified), README documents setup/strategy/migration, `poetry lock` regenerated (only the 3.7/3.8-only `typing-extensions` entry dropped). CI item skipped by decision (no pipeline exists; local project — plan 4 decision 3).
