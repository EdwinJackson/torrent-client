# Plan 1: Fix the peers file issue

## Overview
This plan resolves the peers file parsing issue by cleaning and validating the peers_file.txt format. The current file contains malformed entries causing `ValueError: not enough values to unpack (expected 2, got 1)` in PyBitTorrent's Utils.py.

## Current Issue
The peers_file.txt contains malformed entries. Looking at the preview lines:

```
93.158.213.92:6969

93.158.213.92:1337
```

There appear to be empty lines between valid entries which may cause parsing issues.

## Solution Approach

### 1.1 Analyze the current peers file format
- Read and examine the current peers_file.txt file
- Identify malformed entries and invalid formats

### 1.2 Develop enhanced cleaning script
- Enhance the existing `clean_peers.py` script to handle more edge cases
- Add robust validation logic for IP:PORT format
- Ensure script can handle various malformed entries gracefully

### 1.3 Execute cleaning
- Run the enhanced script on peers_file.txt
- Verify the cleaned file has valid IP:PORT entries only

### 1.4 Test the fix
- Run `poetry run download-torrent` with a test torrent file
- Verify the torrent download works without parsing errors

### Implementation Details

**File to modify:** `clean_peers.py`

**Key improvements needed:**
1. Better pattern matching for IP:PORT format
2. Robust error handling for malformed lines
3. Preservation of valid peers
4. Clean removal of invalid entries
5. Validation against realistic constraints (e.g., valid IP octets, port ranges)

**Edge Cases to Handle:**
- Empty lines or whitespace-only lines
- Malformed IP:PORT pairs (missing ":")
- Invalid IP address formats
- Invalid port numbers (out of range 1-65535)
- Duplicate entries
- Lines with trailing whitespace or newline characters
- Mixed line endings (CRLF vs LF)

## Acceptance Criteria
- peers_file.txt contains only valid IP:PORT pairs
- No parsing errors when reading peers file
- Torrent download completes successfully
- All existing valid peers are preserved

## Risk Mitigation
- Backup the original peers file before cleaning
- Test with a small sample before running on entire file
- Verify the script handles edge cases gracefully

