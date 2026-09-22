import os
import sys
import argparse

if sys.version_info >= (3, 10):
    raise SystemExit(
        "torrent-client requires Python 3.9.x: pybittorrent 0.5.6 pins "
        "urllib3 1.25.11, which uses the legacy PEP 302 import mechanism "
        "removed in Python 3.12+. See README.md (Python version strategy)."
    )

from PyBitTorrent import TorrentClient

def download_torrent_file():
    parser = argparse.ArgumentParser(description="Download a torrent file")
    parser.add_argument("torrent", help="Path to the .torrent file")
    args = parser.parse_args()

    client = TorrentClient(
        torrent=args.torrent,
        max_peers=50,
        use_progress_bar=True,
        peers_file="./peers_file.txt",
        output_dir=os.path.expanduser("~/Downloads")
    )
    client.start()
