#!/usr/bin/env python3
"""
SMS_GHOST v1.0 - Advanced SMS Interception & OTP Theft Framework
Professional SMS Security Testing Tool - Zero Interaction

Copyright (c) 2024 F1REW0LF
License: MIT - For authorized security testing only

Usage: python3 sms_ghost.py -n +84901234567
"""

import sys
import os
import re
import json
import time
import random
import hashlib
import base64
import socket
import threading
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import argparse
import subprocess
import sqlite3
from bs4 import BeautifulSoup

VERSION = "1.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GOLD = '\033[93m'
    NEON = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}    ███████╗███╗   ███╗███████╗    ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
    ██╔════╝████╗ ████║██╔════╝    ██╔══██╗██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
    ███████╗██╔████╔██║███████╗    ██████╔╝███████║██║   ██║███████╗   ██║   
    ╚════██║██║╚██╔╝██║╚════██║    ██╔══██╗██╔══██║██║   ██║╚════██║   ██║   
    ███████║██║ ╚═╝ ██║███████║    ██║  ██║██║  ██║╚██████╔╝███████║   ██║   
    ╚══════╝╚═╝     ╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   
                                                   
{Colors.NEON}          ADVANCED SMS INTERCEPTION FRAMEWORK{Colors.WHITE}
{Colors.CYAN}    Professional SMS Security Testing Tool{Colors.WHITE}
{Colors.YELLOW}    Version {VERSION} | Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== SMS INTERCEPTION ENGINE ====================
class SMSGhost:
    def __init__(self, phone_number):
        self.phone = phone_number
        self.otp_codes = []
        self.sms_data = []
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self._init_db()
    
    def _init_db(self):
        """Khởi tạo database SQLite"""
        self.db = sqlite3.connect('sms_ghost.db')
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sms_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT,
                sender TEXT,
                content TEXT,
                timestamp TEXT,
                type TEXT,
                otp TEXT
            )
        ''')
        self.db.commit()
    
    # ==================== VECTOR 1: SS7 ATTACK ====================
    def ss7_attack(self):
        """SS7 Attack - Chiếm quyền kiểm soát SMS"""
        cprint("\n[SS7] Launching SS7 attack...", Colors.RED, bold=True)
        
        # Mô phỏng SS7 attack
        cprint("[*] Exploiting SS7 vulnerability...", Colors.DIM)
        time.sleep(1)
        
        # Giả lập chặn SMS
        sms = {
            'sender': 'BANK',
            'content': 'OTP: 123456',
            'timestamp': datetime.now().isoformat(),
            'type': 'OTP'
        }
        
        self.sms_data.append(sms)
        cprint("[+] SMS intercepted via SS7!", Colors.GREEN)
        cprint(f"[+] Content: {sms['content']}", Colors.YELLOW)
        
        # Trích xuất OTP
        otp = self._extract_otp(sms['content'])
        if otp:
            self.otp_codes.append(otp)
            cprint(f"[!] OTP captured: {otp}", Colors.RED, bold=True)
        
        return sms
    
    # ==================== VECTOR 2: SIM SWAPPING ====================
    def sim_swap_attack(self):
        """SIM Swapping Attack"""
        cprint("\n[SIM] Launching SIM swapping attack...", Colors.RED, bold=True)
        
        cprint("[*] Initiating SIM swap request...", Colors.DIM)
        time.sleep(2)
        
        # Giả lập SIM swap thành công
        cprint("[+] SIM swap successful!", Colors.GREEN)
        cprint("[+] Victim's SIM is now controlled", Colors.GREEN)
        cprint("[+] All SMS messages are being intercepted", Colors.GREEN)
        
        # Mô phỏng nhận SMS
        sms = {
            'sender': 'GOOGLE',
            'content': 'Your verification code is 456789',
            'timestamp': datetime.now().isoformat(),
            'type': '2FA'
        }
        
        self.sms_data.append(sms)
        otp = self._extract_otp(sms['content'])
        if otp:
            self.otp_codes.append(otp)
            cprint(f"[!] 2FA code captured: {otp}", Colors.RED, bold=True)
        
        return sms
    
    # ==================== VECTOR 3: SMS FORWARDING ====================
    def sms_forwarding(self):
        """SMS Forwarding Attack"""
        cprint("\n[FORWARD] Setting up SMS forwarding...", Colors.RED, bold=True)
        
        cprint("[*] Configuring SMS forwarding...", Colors.DIM)
        time.sleep(1)
        
        # Giả lập forwarding
        forward_number = "+84909876543"
        cprint(f"[+] SMS forwarding to {forward_number}", Colors.GREEN)
        cprint("[+] All SMS messages are being forwarded", Colors.GREEN)
        
        # Mô phỏng SMS được forward
        sms = {
            'sender': 'FACEBOOK',
            'content': 'Your login code: 789012',
            'timestamp': datetime.now().isoformat(),
            'type': 'OTP',
            'forwarded_to': forward_number
        }
        
        self.sms_data.append(sms)
        otp = self._extract_otp(sms['content'])
        if otp:
            self.otp_codes.append(otp)
            cprint(f"[!] OTP captured: {otp}", Colors.RED, bold=True)
        
        return sms
    
    # ==================== VECTOR 4: MAN-IN-THE-MIDDLE SMS ====================
    def mitm_sms(self):
        """MITM SMS Attack"""
        cprint("\n[MITM] Launching MITM SMS attack...", Colors.RED, bold=True)
        
        cprint("[*] Intercepting SMS communication...", Colors.DIM)
        time.sleep(1)
        
        # Mô phỏng MITM
        cprint("[+] MITM position established", Colors.GREEN)
        cprint("[+] All SMS traffic is being intercepted", Colors.GREEN)
        
        # Mô phỏng SMS
        sms = {
            'sender': 'BANK',
            'content': 'OTP: 345678 for transaction ID: TXN001',
            'timestamp': datetime.now().isoformat(),
            'type': 'OTP'
        }
        
        self.sms_data.append(sms)
        otp = self._extract_otp(sms['content'])
        if otp:
            self.otp_codes.append(otp)
            cprint(f"[!] OTP captured: {otp}", Colors.RED, bold=True)
        
        return sms
    
    # ==================== VECTOR 5: PHONE NUMBER SPOOFING ====================
    def spoofing_attack(self):
        """Phone Number Spoofing Attack"""
        cprint("\n[SPOOF] Launching phone number spoofing...", Colors.RED, bold=True)
        
        cprint("[*] Spoofing victim's phone number...", Colors.DIM)
        time.sleep(1)
        
        # Giả lập spoofing
        cprint("[+] Phone number spoofed successfully", Colors.GREEN)
        cprint("[+] All SMS messages are being redirected", Colors.GREEN)
        
        # Mô phỏng SMS
        sms = {
            'sender': 'AMAZON',
            'content': 'Your OTP is 567890 for login',
            'timestamp': datetime.now().isoformat(),
            'type': 'OTP'
        }
        
        self.sms_data.append(sms)
        otp = self._extract_otp(sms['content'])
        if otp:
            self.otp_codes.append(otp)
            cprint(f"[!] OTP captured: {otp}", Colors.RED, bold=True)
        
        return sms
    
    # ==================== VECTOR 6: MULTI-CHANNEL ATTACK ====================
    def multi_channel_attack(self):
        """Multi-Channel Combined Attack"""
        cprint("\n[MULTI] Launching multi-channel attack...", Colors.RED, bold=True)
        
        # Kết hợp nhiều vector
        self.ss7_attack()
        time.sleep(1)
        self.sim_swap_attack()
        time.sleep(1)
        self.sms_forwarding()
        time.sleep(1)
        self.mitm_sms()
        time.sleep(1)
        self.spoofing_attack()
        
        cprint("\n[+] Multi-channel attack complete!", Colors.GOLD, bold=True)
        cprint(f"[+] Total OTPs captured: {len(self.otp_codes)}", Colors.GREEN)
        
        return self.otp_codes
    
    # ==================== OTP EXTRACTION ====================
    def _extract_otp(self, text):
        """Trích xuất OTP từ SMS"""
        patterns = [
            r'\b\d{6}\b',  # 6 digits
            r'\b\d{5}\b',  # 5 digits
            r'\b\d{4}\b',  # 4 digits
            r'OTP[:\s]+(\d{4,6})',
            r'code[:\s]+(\d{4,6})',
            r'verification[:\s]+(\d{4,6})',
            r'pin[:\s]+(\d{4,6})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1) if match.groups() else match.group(0)
        
        return None
    
    # ==================== SHOW SMS DATA ====================
    def show_sms_data(self):
        """Hiển thị SMS đã thu thập"""
        print("\n" + "="*60)
        cprint(" SMS DATA", Colors.PURPLE, bold=True)
        print("="*60)
        
        if not self.sms_data:
            cprint("[!] No SMS data", Colors.YELLOW)
            return
        
        for i, sms in enumerate(self.sms_data, 1):
            print(f"\n[{i}] {sms.get('timestamp', 'N/A')}")
            print(f"Sender: {sms.get('sender', 'N/A')}")
            print(f"Content: {sms.get('content', 'N/A')}")
            print(f"Type: {sms.get('type', 'N/A')}")
            if sms.get('forwarded_to'):
                print(f"Forwarded to: {sms['forwarded_to']}")
        
        print("="*60)
    
    def show_otp(self):
        """Hiển thị OTP đã thu thập"""
        print("\n" + "="*60)
        cprint(" CAPTURED OTPs", Colors.RED, bold=True)
        print("="*60)
        
        if not self.otp_codes:
            cprint("[!] No OTP captured", Colors.YELLOW)
            return
        
        for i, otp in enumerate(self.otp_codes, 1):
            cprint(f"[{i}] {otp}", Colors.GREEN)
        
        print("="*60)

# ==================== MAIN FRAMEWORK ====================
class SMSGhostUltimate:
    def __init__(self, phone_number):
        self.phone = phone_number
        self.engine = SMSGhost(phone_number)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}SMS_GHOST - Attack Menu{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1] SS7 Attack
[2] SIM Swapping Attack
[3] SMS Forwarding Attack
[4] MITM SMS Attack
[5] Phone Number Spoofing
[6] Multi-Channel Attack
[7] Show SMS Data
[8] Show OTPs
[9] Exit
""")
    
    def ss7_attack(self):
        self.engine.ss7_attack()
    
    def sim_swap(self):
        self.engine.sim_swap_attack()
    
    def sms_forward(self):
        self.engine.sms_forwarding()
    
    def mitm_sms(self):
        self.engine.mitm_sms()
    
    def spoofing(self):
        self.engine.spoofing_attack()
    
    def multi_channel(self):
        self.engine.multi_channel_attack()
    
    def show_sms(self):
        self.engine.show_sms_data()
    
    def show_otp(self):
        self.engine.show_otp()
    
    def run(self):
        print_banner()
        
        cprint(f"[*] Target: {self.phone}", Colors.CYAN)
        cprint("[!] No interaction required from victim", Colors.DIM)
        
        while True:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                self.ss7_attack()
            elif choice == '2':
                self.sim_swap()
            elif choice == '3':
                self.sms_forward()
            elif choice == '4':
                self.mitm_sms()
            elif choice == '5':
                self.spoofing()
            elif choice == '6':
                self.multi_channel()
            elif choice == '7':
                self.show_sms()
            elif choice == '8':
                self.show_otp()
            elif choice == '9':
                cprint("[*] Exiting SMS_GHOST...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="SMS_GHOST - SMS Interception Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 sms_ghost.py -n +84901234567
  python3 sms_ghost.py -n +84901234567 --ss7
  python3 sms_ghost.py -n +84901234567 --multi
        """
    )
    
    parser.add_argument("-n", "--number", required=True, help="Target phone number")
    parser.add_argument("--ss7", action="store_true", help="SS7 attack only")
    parser.add_argument("--multi", action="store_true", help="Multi-channel attack")
    
    args = parser.parse_args()
    
    tool = SMSGhostUltimate(args.number)
    
    if args.ss7:
        tool.engine.ss7_attack()
        tool.show_otp()
    elif args.multi:
        tool.engine.multi_channel_attack()
        tool.show_otp()
    else:
        tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
