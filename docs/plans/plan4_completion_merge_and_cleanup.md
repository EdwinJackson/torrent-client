# Plan 4: Finish Plans 1–3, merge branches, clean up worktrees

## Current State (verified 2026-09-22)
- `main` (a175158, in sync with `origin/main`): peers_file.txt still broken (129 lines, blank-line separated); old unvalidated `clean_peers.py`; empty README; `requires-python = ">=3.7,<4.0"`; no `.python-version`; no CI.
- `peers-file-cleanup` (fa05146, worktree `../torrent-client_peers-file-cleanup`): enhanced cleaner + cleaned 56-line peers_file.txt. Untracked `peers_file.txt.backup` in worktree. **Verified clean merge into main** (`git merge-tree --write-tree` → b77d83d, no conflicts).
- `torrent-client_urllib3_python314_fix` (1418837, worktree `../torrent-client_urllib3_python314_fix`): sole commit duplicates the plan2 doc already on main. **Uncommitted** changes rename `download_torrent_file` → `download_torrent` (3 files) — no other work exists on this branch.
- `docs/plans/plan3_environment_standardization.md`: untracked.

## Decisions (reconciliation calls)
1. **Keep `download_torrent_file` naming.** main is already self-consistent (`pyproject.toml`, `client.py`, `__main__.py` all agree); plan 2 §2.2's "mismatch" no longer exists. The uncommitted rename in the urllib3 worktree is a style-only delta → **discard it**. (To adopt `download_torrent` instead, merge those 3 files first in Phase 2 — same end state otherwise.)
2. **Discard `peers_file.txt.backup`** after Phase 1 verification — the original 129-line file is preserved in git history (blob `0fa8e62`), so the backup is redundant.
3. **No CI creation.** plan3 §3.4 says "CI/CD tests pass"; the repo has no pipeline and building one is net-new scope. The CI-related acceptance items are satisfied vacuously + noted in README. Flag: override if CI is actually wanted.
4. **Plan 2 §2.3/2.4 and Plan 3 §3.1/3.6 are the same work** (version pin + strategy documentation) — done once, in Phase 3.
5. Full network download (plan1 §1.4 "download completes") is verified only as far as the environment allows: peers parsing + CLI invocation without errors; document the limit.

## Phase 1 — Merge Plan 1 work into main
1. `git merge --no-ff peers-file-cleanup -m "Merge branch 'peers-file-cleanup': Plan 1 peers file fix"` (from main worktree).
2. Verify on main: `peers_file.txt` has 56 lines, zero blank lines (`grep -c '^$' peers_file.txt` → 0); all lines match `^\d+\.\d+\.\d+\.\d+:\d+$`; `clean_peers.py` contains `is_valid_ip`/`is_valid_port`.
3. Idempotence check: `python3 clean_peers.py /tmp/peers_copy` (copy of the file) → file unchanged, "56 valid peers".

## Phase 2 — Resolve the urllib3 worktree
1. Confirm the dirty diff is exactly the 3-file rename (`git diff` in worktree) — nothing else is lost.
2. `git -C ../torrent-client_urllib3_python314_fix checkout -- pyproject.toml src/torrent_client/__main__.py src/torrent_client/client.py`.
3. Remove worktree: `git worktree remove ../torrent-client_urllib3_python314_fix`.
4. Force-delete branch (content-duplicate, never an ancestor → `-D`): `git branch -D torrent-client_urllib3_python314_fix`.

## Phase 3 — Commit plan3 doc + implement Plans 2-remainder & 3 on main
1. `git add docs/plans/plan3_environment_standardization.md docs/plans/plan4_completion_merge_and_cleanup.md` + commit.
2. `pyproject.toml`: `requires-python = ">=3.9,<3.10"`.
3. Create `.python-version` containing `3.9` (mise.toml already pins 3.9 — leave).
4. Runtime guard in `src/torrent_client/client.py` top:
   `if sys.version_info >= (3, 10): raise SystemExit("torrent-client requires Python 3.9.x (urllib3 1.25.11 incompatibility; see README)")`.
5. README.md (currently 0 bytes): setup instructions (mise → poetry install), supported version **3.9**, Python-version strategy incl. urllib3 1.25.11 legacy-loader breakage on 3.12+/3.14, migration path (bump requests/urllib3, revalidate pybittorrent), note that no CI exists.
6. `poetry lock` (Poetry 2.x — refreshes lock against new constraint); confirm no spurious version churn; `poetry check`.

## Phase 4 — End-to-end verification
- `mise exec -- python -V` → 3.9.x; `poetry env info -p` resolves; `poetry run python -V` → 3.9.x.
- Entry points import: `poetry run python -c "from torrent_client.client import download_torrent_file"`.
- `poetry run download-torrent --help` → argparse usage, no crash (exercises PyBitTorrent/urllib3 import chain on 3.9 → plan2 acceptance "no import errors").
- `poetry run clean-peers <tmp copy>` → idempotent on the 56-line file.
- Guard check: run `client.py` import under any available 3.12+/3.14 → SystemExit message, not an ImportError stack.
- Full-download test: attempt `poetry run download-torrent` only if a local/sample .torrent exists (torrents.yml holds a magnet, not a file) → otherwise record as manual-acceptance gap.

## Phase 5 — Cleanup + finish
1. Remove merged worktree + branch: `git worktree remove ../torrent-client_peers-file-cleanup` (after deleting its `peers_file.txt.backup`, decision 2), `git branch -d peers-file-cleanup`.
2. `git worktree prune`; `git worktree list` → main only.
3. Annotate plan docs: append `Status: COMPLETE — merged/landed <date>` to plans 1–3.
4. `git push` (main → origin/main).

## Acceptance
- `git worktree list` shows only the primary checkout; `git branch` shows only `main` (+ origin remote refs).
- main contains: cleaned peers_file.txt, enhanced clean_peers.py, pinned Python constraint + `.python-version` + runtime guard, populated README, refreshed lock, all 4 plan docs tracked.
- Phase 4 checks all green; `git log` shows merge commit from Phase 1 and implementation commits from Phases 3/5; pushed.

## Status
COMPLETE — 2026-09-22. All five phases executed: Plan 1 merged (`afed1c3`), urllib3 worktree+branch discarded, env standardization landed, verification green (incl. pre-fix `ValueError` reproduction), worktrees reduced to primary checkout only. Extra defect found+fixed in Phase 4: `clean-peers` console script was never installed (root module unpackaged; entry bypassed argparse) → `clean_peers.py` added to `packages`, entry points to `clean_peers:main`.
