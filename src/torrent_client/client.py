import os
import argparse
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
