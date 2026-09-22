# Plan 2: Resolve the urllib3 + Python 3.14 compatibility issue

## Overview
This plan resolves the urllib3 compatibility issue while maintaining the working Python 3.9 environment as the default. The problem is that urllib3 1.25.11 (which is required by pybittorrent 0.5.6) uses the legacy PEP 302 import mechanism (find_module/load_module) that Python 3.14 no longer supports.

## Solution Approach

### 2.1 Python version selection
Based on current testing, maintain Python 3.9 as the stable default version since it successfully runs the core functionality (except for peers file parsing).

### 2.2 Immediate fixes for Python 3.9
- Fix peers file parsing issue (Plan 1)
- Fix function name mismatch in client.py (entry point points to download_torrent but function is download_torrent_file)

### 2.3 Long-term Python version strategy
Explore and document alternative approaches for future upgrades:
- Test Python 3.10 (if working)
- Test Python 3.11 (if working)
- Document the incompatibility with Python 3.14+

### 2.4 Environment maintenance
- Ensure consistent environment configuration
- Document the chosen Python version and any constraints
- Provide clear migration path for future Python upgrades

### 2.5 Implementation steps
1. Fix peers file parsing (Plan 1)
2. Fix function name mismatch in client.py
3. Test on Python 3.9
4. Document Python version strategy
5. If needed, provide patch approach for future Python version upgrades

## Acceptance Criteria
- Successfully run `poetry run download-torrent` with Python 3.9
- All functionality works (torrent download, progress bar, peer management)
- No import errors or runtime crashes
- Project maintains compatibility with existing code
- Clear documentation of Python version strategy

## Risk Mitigation
- Keep current Python 3.9 environment stable
- Document any workarounds for future Python version upgrades
- Maintain working fallback for critical use cases
- Document known incompatibilities with newer Python versions

## Alternative Approach
If exploring newer Python versions reveals compatibility issues, consider:
- Maintaining Python 3.9 support only
- Adding explicit Python version constraint in pyproject.toml
- Documenting Python 3.10+ incompatibility
- Providing migration path for future upgrades

## Status
COMPLETE — 2026-09-22. Resolution: stay on Python 3.9 (urllib3 1.25.11 legacy-loader breakage on 3.12+ documented in README). Entry-point consistency kept on `download_torrent_file` (the "mismatch" no longer existed on main; the worktree rename was discarded — see plan 4 decision 1). Import chain verified via `poetry run download-torrent --help`.
