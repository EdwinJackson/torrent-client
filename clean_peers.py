#!/usr/bin/env python3
import re
import argparse
import os

def is_valid_ip(ip: str) -> bool:
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

def is_valid_port(port: str) -> bool:
    try:
        num = int(port)
        return 1 <= num <= 65535
    except ValueError:
        return False

def clean_peers_file(file_path: str = "peers_file.txt") -> None:
    ip_port_pattern = re.compile(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$')
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    seen_peers = set()
    
    for line in lines:
        original_line = line.strip()
        if not original_line:
            continue
        
        match = ip_port_pattern.match(original_line)
        if not match:
            continue
        
        ip = match.group(1)
        port = match.group(2)
        
        if not is_valid_ip(ip):
            continue
        
        if not is_valid_port(port):
            continue
        
        peer = f"{ip}:{port}"
        if peer in seen_peers:
            continue
        
        seen_peers.add(peer)
        cleaned_lines.append(f"{ip}:{port}\n")
    
    backup_path = file_path + ".backup"
    if os.path.exists(file_path):
        os.rename(file_path, backup_path)
    
    with open(file_path, 'w') as f:
        f.writelines(cleaned_lines)
    
    print(f"Cleaned {file_path}: {len(cleaned_lines)} valid peers remaining")
    if os.path.exists(backup_path):
        print(f"Original file backed up to {backup_path}")

def main():
    parser = argparse.ArgumentParser(description="Clean peers file by removing invalid entries")
    parser.add_argument("peers_file", nargs="?", help="Path to the peers file", default="peers_file.txt")
    args = parser.parse_args()
    clean_peers_file(args.peers_file)

if __name__ == "__main__":
    main()
