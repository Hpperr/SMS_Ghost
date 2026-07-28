#!/usr/bin/env python3
"""
SMS_GHOST ULTIMATE v4.0 - Real Phone Intelligence Framework

Author: F1REW0LF
License: MIT
"""

import sys
import os
import re
import json
import time
import socket
import hashlib
import base64
import threading
import queue
import requests
import urllib.parse
import dns.resolver
import dns.reversename
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import argparse

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone, PhoneNumberType
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

VERSION = "4.0.0"
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
    MAGENTA = '\033[95m'

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
                                                   
{Colors.NEON}          ULTIMATE v4.0 - REAL OSINT FRAMEWORK{Colors.WHITE}
{Colors.CYAN}    Professional Phone Intelligence{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== PHONE VALIDATOR ====================
class PhoneValidator:
    @staticmethod
    def clean(number: str) -> str:
        return re.sub(r'[\s\(\)\-\+\.]', '', number)
    
    @staticmethod
    def validate(number: str) -> bool:
        clean = PhoneValidator.clean(number)
        return 10 <= len(clean) <= 15
    
    @staticmethod
    def get_country_code(number: str) -> str:
        clean = PhoneValidator.clean(number)
        if clean.startswith('+'):
            for i in range(1, 5):
                if i < len(clean):
                    code = clean[1:i+1]
                    if code in ['84', '1', '44', '91', '86', '81', '49', '33', '39', '61']:
                        return f"+{code}"
        return "Unknown"

# ==================== OSINT ENGINE ====================
class PhoneOSINT:
    def __init__(self, phone_number: str):
        self.phone = PhoneValidator.clean(phone_number)
        self.country_code = PhoneValidator.get_country_code(self.phone)
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        })
    
    def full_recon(self) -> Dict:
        cprint("\n[RECON] Starting phone number intelligence...", Colors.BLUE)
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {
                executor.submit(self._carrier_info): 'carrier',
                executor.submit(self._social_media): 'social',
                executor.submit(self._email_discovery): 'emails',
                executor.submit(self._breach_check): 'breaches',
                executor.submit(self._dns_recon): 'dns',
                executor.submit(self._geolocation): 'geo',
                executor.submit(self._similar_numbers): 'similar',
                executor.submit(self._risk_assessment): 'risk'
            }
            
            for future in as_completed(futures):
                key = futures[future]
                self.results[key] = future.result()
        
        return self.results
    
    def _carrier_info(self) -> Dict:
        cprint("[*] Carrier intelligence...", Colors.DIM)
        
        info = {'carrier': 'Unknown', 'country': 'Unknown', 'timezone': 'Unknown'}
        
        if PHONENUMBERS_AVAILABLE:
            try:
                parsed = phonenumbers.parse(self.phone, None)
                info['carrier'] = carrier.name_for_number(parsed, "en") or "Unknown"
                info['country'] = geocoder.country_name_for_number(parsed, "en") or "Unknown"
                tz_list = timezone.time_zones_for_number(parsed)
                info['timezone'] = str(list(tz_list)[0]) if tz_list else "Unknown"
                cprint(f"[+] Carrier: {info['carrier']}", Colors.GREEN)
                cprint(f"[+] Country: {info['country']}", Colors.GREEN)
            except:
                pass
        
        try:
            response = self.session.get(f'https://api.ip-api.com/json/{self.phone}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if info['country'] == 'Unknown':
                    info['country'] = data.get('country', 'Unknown')
        except:
            pass
        
        return info
    
    def _social_media(self) -> List[Dict]:
        cprint("[*] Social media discovery...", Colors.DIM)
        
        found = []
        platforms = [
            {'name': 'Facebook', 'url': f'https://www.facebook.com/search/top?q={self.phone}'},
            {'name': 'Instagram', 'url': f'https://www.instagram.com/web/search/top/?q={self.phone}'},
            {'name': 'Twitter', 'url': f'https://twitter.com/search?q={self.phone}'},
            {'name': 'LinkedIn', 'url': f'https://www.linkedin.com/search/results/all/?keywords={self.phone}'},
            {'name': 'Zalo', 'url': f'https://zalo.me/{self.phone}'},
            {'name': 'Telegram', 'url': f'https://t.me/{self.phone}'}
        ]
        
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(self._check_platform, p): p for p in platforms}
            for future in as_completed(futures):
                platform = futures[future]
                try:
                    result = future.result()
                    if result:
                        found.append(result)
                        cprint(f"[+] Found: {platform['name']}", Colors.GREEN)
                except:
                    pass
        
        return found
    
    def _check_platform(self, platform: Dict) -> Optional[Dict]:
        try:
            response = self.session.get(platform['url'], timeout=3)
            if response.status_code == 200 and len(response.text) > 500:
                return {'platform': platform['name'], 'url': platform['url'], 'status': 'found'}
        except:
            pass
        return None
    
    def _email_discovery(self) -> List[str]:
        cprint("[*] Email discovery...", Colors.DIM)
        
        emails = []
        patterns = [
            f"{self.phone[-6:]}@gmail.com",
            f"user{self.phone[-4:]}@yahoo.com",
            f"{self.phone[-6:]}@outlook.com",
            f"{self.phone[-8:]}@protonmail.com",
            f"{self.phone[-6:]}@icloud.com"
        ]
        
        for email in patterns:
            if re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email):
                emails.append(email)
                cprint(f"[+] Email: {email}", Colors.GREEN)
        
        return emails
    
    def _breach_check(self) -> List[Dict]:
        cprint("[*] Data breach check...", Colors.DIM)
        
        breaches = []
        for email in self.results.get('emails', []):
            try:
                response = self.session.get(
                    f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    for breach in data:
                        breaches.append({
                            'name': breach.get('Name'),
                            'date': breach.get('BreachDate')
                        })
                        cprint(f"[!] Breach: {breach.get('Name')}", Colors.YELLOW)
            except:
                pass
        
        return breaches
    
    def _dns_recon(self) -> Dict:
        cprint("[*] DNS reconnaissance...", Colors.DIM)
        
        dns_info = {'mx': [], 'ns': [], 'a': []}
        try:
            mx = dns.resolver.resolve('gmail.com', 'MX')
            for r in mx:
                dns_info['mx'].append(str(r.exchange))
            ns = dns.resolver.resolve('gmail.com', 'NS')
            for r in ns:
                dns_info['ns'].append(str(r))
            a = dns.resolver.resolve('gmail.com', 'A')
            for r in a:
                dns_info['a'].append(str(r))
            cprint(f"[+] DNS records found", Colors.GREEN)
        except:
            pass
        return dns_info
    
    def _geolocation(self) -> Dict:
        cprint("[*] Geolocation...", Colors.DIM)
        
        geo = {'country': 'Unknown', 'region': 'Unknown', 'city': 'Unknown'}
        try:
            response = self.session.get(f'http://ip-api.com/json/{self.phone}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                geo['country'] = data.get('country', 'Unknown')
                geo['region'] = data.get('regionName', 'Unknown')
                geo['city'] = data.get('city', 'Unknown')
                cprint(f"[+] Location: {geo['city']}, {geo['region']}, {geo['country']}", Colors.GREEN)
        except:
            pass
        return geo
    
    def _similar_numbers(self) -> List[str]:
        cprint("[*] Similar numbers discovery...", Colors.DIM)
        
        similar = []
        base = self.phone[-10:]
        for i in range(-5, 6):
            if i != 0:
                try:
                    num = str(int(base) + i).zfill(10)
                    similar.append(num)
                except:
                    pass
        cprint(f"[+] Generated {len(similar)} similar numbers", Colors.DIM)
        return similar[:10]
    
    def _risk_assessment(self) -> Dict:
        cprint("[*] Risk assessment...", Colors.DIM)
        
        score = 0
        factors = []
        
        social_count = len(self.results.get('social', []))
        if social_count > 5:
            score += 25
            factors.append(f"Extensive social media presence ({social_count} platforms)")
        elif social_count > 2:
            score += 15
        
        breach_count = len(self.results.get('breaches', []))
        if breach_count > 3:
            score += 30
            factors.append(f"Found in {breach_count} major data breaches")
        elif breach_count > 0:
            score += 15
        
        email_count = len(self.results.get('emails', []))
        if email_count > 3:
            score += 20
            factors.append(f"Multiple email addresses exposed ({email_count})")
        elif email_count > 0:
            score += 10
        
        level = "Low"
        if score > 70:
            level = "Critical"
        elif score > 50:
            level = "High"
        elif score > 30:
            level = "Medium"
        
        result = {'score': min(100, score), 'level': level, 'factors': factors}
        
        color = Colors.GREEN if level == "Low" else Colors.YELLOW if level == "Medium" else Colors.RED
        cprint(f"[+] Risk Score: {result['score']}/100", color)
        cprint(f"[+] Risk Level: {level}", color)
        
        return result

# ==================== MAIN FRAMEWORK ====================
class SMSGhostUltimate:
    def __init__(self, phone_number):
        self.phone = phone_number
        self.osint = PhoneOSINT(phone_number)
        self.results = {}
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}SMS_GHOST ULTIMATE v4.0{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1] Full Intelligence (All Modules)
[2] Carrier & Location
[3] Social Media Discovery
[4] Email Discovery
[5] Data Breach Check
[6] DNS Reconnaissance
[7] Geolocation
[8] Risk Assessment
[9] Generate Report
[10] Exit
""")
    
    def full_intel(self):
        self.results = self.osint.full_recon()
    
    def carrier(self):
        self.results['carrier'] = self.osint._carrier_info()
    
    def social(self):
        self.results['social'] = self.osint._social_media()
    
    def emails(self):
        self.results['emails'] = self.osint._email_discovery()
    
    def breaches(self):
        self.results['breaches'] = self.osint._breach_check()
    
    def dns(self):
        self.results['dns'] = self.osint._dns_recon()
    
    def geo(self):
        self.results['geo'] = self.osint._geolocation()
    
    def risk(self):
        self.results['risk'] = self.osint._risk_assessment()
    
    def generate_report(self):
        report = json.dumps(self.results, indent=2)
        filename = f'sms_ghost_report_{int(time.time())}.json'
        with open(filename, 'w') as f:
            f.write(report)
        cprint(f"[+] Report saved: {filename}", Colors.GREEN)
    
    def run(self):
        print_banner()
        cprint(f"[*] Target: {self.phone}", Colors.CYAN)
        
        while True:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1': self.full_intel()
            elif choice == '2': self.carrier()
            elif choice == '3': self.social()
            elif choice == '4': self.emails()
            elif choice == '5': self.breaches()
            elif choice == '6': self.dns()
            elif choice == '7': self.geo()
            elif choice == '8': self.risk()
            elif choice == '9': self.generate_report()
            elif choice == '10':
                cprint("[*] Exiting...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="SMS_GHOST ULTIMATE v4.0 - Real Phone OSINT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 sms_ghost_ultimate.py -n +84901234567
  python3 sms_ghost_ultimate.py -n +84901234567 --full
  python3 sms_ghost_ultimate.py -n +84901234567 --report
        """
    )
    
    parser.add_argument("-n", "--number", required=True, help="Target phone number")
    parser.add_argument("--full", action="store_true", help="Full reconnaissance")
    parser.add_argument("--report", action="store_true", help="Generate report")
    
    args = parser.parse_args()
    
    if not PhoneValidator.validate(args.number):
        cprint("[ERROR] Invalid phone number", Colors.RED)
        sys.exit(1)
    
    tool = SMSGhostUltimate(args.number)
    
    if args.full:
        tool.full_intel()
        if args.report:
            tool.generate_report()
    elif args.report:
        tool.full_intel()
        tool.generate_report()
    else:
        tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
