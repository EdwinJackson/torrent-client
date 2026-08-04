#!/usr/bin/env python3
import re
import argparse
import os

def clean_peers_file(file_path: str = "peers_file.txt") -> None:
    ip_port_pattern = re.compile(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$')
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        match = ip_port_pattern.match(line)
        if match:
            cleaned_line = f"{match.group(1)}:{match.group(2)}\n"
            cleaned_lines.append(cleaned_line)
    
    with open(file_path, 'w') as f:
        f.writelines(cleaned_lines)
    
    print(f"Cleaned {file_path}: {len(cleaned_lines)} valid peers remaining")

def main():
    parser = argparse.ArgumentParser(description="Clean peers file by removing invalid entries")
    parser.add_argument("peers_file", nargs="?", help="Path to the peers file", default="peers_file.txt")
    args = parser.parse_args()
    clean_peers_file(args.peers_file)

if __name__ == "__main__":
    main()
