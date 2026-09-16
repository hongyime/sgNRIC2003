# State — sgNRIC2003

**Last updated**: 2026-09-16 (baseline review, opencode/Sisyphus-Junior)
**Branch**: master (up to date with origin after pull)

## Current Status
Baseline audit complete. No active development task in progress.

## Repo Summary
- **Purpose**: Singapore NRIC (2003 format) generator + validator + barcode generator
- **Stack**: Python 3, stdlib only
- **Files**:
  - `code/01_generate nric2003.py` — generates all T03xxxxx NRIC combos (prefix "T03", 5-digit numbers, suffixes A–Z)
  - `code/02_validate nric2003.py` — validates NRIC using official checksum algorithm (weights, check-digit tables)
  - `code/03_generate barcodes.py` — generates barcodes from NRIC numbers
  - `output/` — generated text lists + compressed barcode archives
  - `archive/` — historical NRIC card image + video

## Sensitivity Assessment
- **No personal data**: output files contain algorithmically-derived NRIC-format strings (T03xxxxx), NOT real citizen records
- The full set of valid NRICs for a given year/prefix is mathematically derivable from the public checksum algorithm
- `validated nric2003.txt` = subset passing checksum — still no PII (names, DOB, addresses)

## Open PRs / Issues
- 1 open Dependabot PR #88: bump `actions/labeler` from 6→7 (2026-08-24)
- 0 open issues

## Security Status
- Secret scan: **CLEAN** — no matches for password/api_key/secret/token in .py files

## Next Steps
- Merge or close Dependabot PR #88 (routine, low-risk)
- No urgent security work required
