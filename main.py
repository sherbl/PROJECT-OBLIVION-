#!/usr/bin/env python3
import argparse
import yaml
import sys
import time
import socket

class Logger(object):
    def __init__(self, filename="scan.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def print_banner():
    banner = """\033[1;31m
 ██████╗ ██████╗ ██╗     ██╗██╗   ██╗██╗ ██████╗ ███╗   ██╗
██╔═══██╗██╔══██╗██║     ██║██║   ██║██║██╔═══██╗████╗  ██║
██║   ██║██████╔╝██║     ██║██║   ██║██║██║   ██║██╔██╗ ██║
██║   ██║██╔══██╗██║     ██║╚██╗ ██╔╝██║██║   ██║██║╚██╗██║
╚██████╔╝██████╔╝███████╗██║ ╚████╔╝ ██║╚██████╔╝██║ ╚████║
 ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                           
        >> OFFENSIVE FRAMEWORK: PROJECT OBLIVION <<
         [*] STATUS: READY FOR ENGAGEMENT [*]
                 ****Sherbl.ab****
============================================================\033[0m"""
    print(banner)

def load_config():
    try:
        with open("config/settings.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("[-] config/settings.yaml not found.")
        return None

def resolve_target(target):
    """מנקה את הקלט (במקרה של URL) וממיר דומיין לכתובת IP"""
    # מסיר http:// או https:// ונתיבים כדי לקבל רק את הדומיין/IP נקי
    clean_target = target.replace('http://', '').replace('https://', '').split('/')[0]
    try:
        # פונקציה זו יודעת לקבל גם IP וגם דומיין. אם זה דומיין היא תמיר ל-IP.
        ip = socket.gethostbyname(clean_target)
        return clean_target, ip
    except socket.gaierror:
        return clean_target, None

def main():
    parser = argparse.ArgumentParser(description="Advanced Red Team Vuln Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target Domain or IP address")
    args = parser.parse_args()

    # שלב המרת הדומיין ל-IP
    original_target, target_ip = resolve_target(args.target)
    
    if not target_ip:
        print(f"\n[-] Error: Could not resolve target '{original_target}'. Please check the domain name.")
        sys.exit(1)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = f"scan_{target_ip.replace('.', '_')}_{timestamp}.log"
    
    # הפעלת שמירת הלוגים רק אם הכתובת תקינה
    sys.stdout = Logger(log_file) 

    print_banner()

    config = load_config()
    if config is None:
        return

    print("="*50)
    print("[*] Initialization Complete")
    
    # הצגת הפענוח למשתמש
    if original_target != target_ip:
        print(f"[*] Target locked: {original_target} -> Resolved to IP: {target_ip}")
    else:
        print(f"[*] Target locked: {target_ip}")
        
    print("="*50)

    from core.engine import ScannerEngine
    engine = ScannerEngine(config)
    # אנחנו מעבירים למנוע את ה-IP הנקי כדי ש-Nmap ו-Shodan יעבדו בצורה חלקה
    engine.run(target_ip)
    
    print(f"\n[+] Terminal output successfully saved to log file: {log_file}")

if __name__ == "__main__":
    main()
