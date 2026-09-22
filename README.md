# torrent-client

Minimal torrent downloader built on PyBitTorrent, managed with Poetry. Local project — no CI.

## Requirements

- [mise](https://mise.jdx.dev) — pins **Python 3.9** (`mise.toml`, `.python-version`)
- [Poetry](https://python-poetry.org) 2.x

## Setup

```bash
mise install      # provisions Python 3.9
poetry install
```

## Usage

```bash
poetry run download-torrent <path-to.torrent>   # download to ~/Downloads
poetry run clean-peers [peers_file.txt]         # validate/repair the peers file
```

Torrents are tracked in `torrents.yml` as **magnet URIs** (easy to manage in bulk; no loose `.torrent` files). Peer list is read from `./peers_file.txt`.

## Peers file

`peers_file.txt` must contain one `IP:PORT` per line — no blank lines. Malformed entries previously crashed PyBitTorrent's parser with `ValueError: not enough values to unpack (expected 2, got 1)`. `clean-peers` (see `clean_peers.py`) fixes a file in place: strips blank/whitespace lines, validates IP octets (0–255) and ports (1–65535), drops duplicates, and keeps a `.backup` of the pre-clean file.

## Python version strategy

**Supported: Python 3.9 only** — `requires-python = ">=3.9,<3.10"` in `pyproject.toml`, enforced at runtime by a guard in `src/torrent_client/client.py`.

Why: `pybittorrent 0.5.6` pins `urllib3 1.25.11`, which relies on the legacy PEP 302 import mechanism (`find_module`/`load_module`) removed in Python 3.12. On newer interpreters (first hit on 3.14) importing `requests`/`urllib3` fails outright. There is no upstream fix for the pinned urllib3.

### Migration path for future upgrades

1. Move to a `pybittorrent` release that allows `urllib3 >= 1.26` (or 2.x), or drop the dependency.
2. Widen `requires-python`, delete the runtime guard, update `.python-version`/`mise.toml`, run `poetry lock`.
3. Revalidate: `poetry run python -c "from torrent_client.client import download_torrent_file"`, `poetry run download-torrent --help`, `poetry run clean-peers`, then a real download from a magnet in `torrents.yml`.

## History

Environment reconciliation (Plans 1–3) is documented in `docs/plans/` — notably the peers-file fix (merged from `peers-file-cleanup`) and this Python pinning.
