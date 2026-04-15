import argparse
import sys
import time
import os
import subprocess

def auto_install_requirements():
    try:
        import colorama
        import pefile
    except ImportError:
        print("[!] Phát hiện khởi chạy lần đầu! Đang tải thư viện PE-Core...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("[+] Sẵn sàng.\n")
        except Exception as e:
            print(f"[!] Lỗi: {e}.")
            sys.exit(1)

auto_install_requirements()

from colorama import init, Fore, Style
from modules.binary_protections import BinaryProtectionScanner
from modules.api_scanner import APIScanner
from modules.dll_hijack import DLLHijackingScanner
from modules.windows_manifest import WindowsServicesManifestScanner
from modules.packer_detector import PackerDetector
from modules.crypto_scanner import CryptoScanner
from modules.local_storage import LocalStorageScanner
from modules.ad_scanner import ADScanner
from modules.driver_scanner import DriverScanner
from modules.reporter import ReportGenerator
from modules.ai_analyzer import AIAnalyzer
from modules.weaponizer import Weaponizer

init(autoreset=True)

def print_banner():
    banner = f"""
 {Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
 ║                                                              ║
 ║                 {Fore.WHITE}AUTOMATION PENTEST SYSTEM{Fore.CYAN}                    ║
 ║                  Ultimate Security Scanner                   ║
 ║                  {Fore.YELLOW}PROFESSIONAL EDITION{Fore.CYAN}                        ║
 ║                                                              ║
 ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def is_pe_file(path):
    try:
        with open(path, 'rb') as f:
            return f.read(2) == b'MZ'
    except: return False

def scan_single_file(target_path, args):
    if not is_pe_file(target_path):
        print(f"{Fore.RED}[!] Unsupported Format: {target_path}{Style.RESET_ALL}")
        return None

    print(f"\n{Fore.YELLOW}============================================================{Style.RESET_ALL}")
    print(f"{Fore.WHITE}[*] STARTING AUTOMATION PENTEST AUDIT: {target_path}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}============================================================{Style.RESET_ALL}")

    report_gen = ReportGenerator(target_path, args.output)

    # --- TẦNG 1 & 2: MITIGATIONS & AUTHENTICODE ---
    print(f"\n{Fore.GREEN}[+] TẦNG 1-2: BINARY HARDENING & CODE SIGNING{Style.RESET_ALL}")
    bp_scanner = BinaryProtectionScanner(target_path)
    report_gen.add_section("Tầng 1-2: Mitigations & Authenticode", bp_scanner.scan())

    # --- TẦNG 3: API ANOMALY ---
    print(f"\n{Fore.GREEN}[+] TẦNG 3: API ANOMALY & IAT AUDIT{Style.RESET_ALL}")
    api_scanner = APIScanner(target_path)
    report_gen.add_section("Tầng 3: API Anomaly & IAT Audit", api_scanner.scan())

    # --- TẦNG 4: DLL HIJACKING ---
    print(f"\n{Fore.GREEN}[+] TẦNG 4: DLL HIJACKING & SIDE-LOADING{Style.RESET_ALL}")
    hijack_scanner = DLLHijackingScanner(target_path)
    report_gen.add_section("Tầng 4: DLL Hijacking & Side-loading", hijack_scanner.scan())

    # --- TẦNG 5: RESOURCE & MANIFEST ---
    print(f"\n{Fore.GREEN}[+] TẦNG 5: RESOURCE & MANIFEST (LPE){Style.RESET_ALL}")
    manifest_scanner = WindowsServicesManifestScanner(target_path)
    report_gen.add_section("Tầng 5: Resource & Manifest (LPE)", manifest_scanner.scan())

    # --- TẦNG 6: PACKER & ANTI-RE ---
    print(f"\n{Fore.GREEN}[+] TẦNG 6: PACKER, ENTROPY & ANTI-RE{Style.RESET_ALL}")
    packer_scanner = PackerDetector(target_path)
    report_gen.add_section("Tầng 6: Packer, Entropy & Anti-RE", packer_scanner.scan())

    # --- TẦNG 7: SECRETS & CRYPTO ---
    print(f"\n{Fore.GREEN}[+] TẦNG 7: HARDCODED SECRETS & CRYPTO Indicators{Style.RESET_ALL}")
    crypto_scanner = CryptoScanner(target_path)
    report_gen.add_section("Tầng 7: Hardcoded Secrets & Crypto", crypto_scanner.scan())

    # --- TẦNG 8: LOCAL STORAGE ---
    print(f"\n{Fore.GREEN}[+] TẦNG 8: LOCAL STORAGE & DATA PRIVACY{Style.RESET_ALL}")
    scan_dir = os.path.dirname(os.path.abspath(target_path)) if os.path.isfile(target_path) else target_path
    storage_scanner = LocalStorageScanner(scan_dir)
    report_gen.add_section("Tầng 8: Local Storage & Data Privacy", storage_scanner.scan())

    # --- TẦNG 9: ECOSYSTEM (AD & DRIVER) ---
    print(f"\n{Fore.GREEN}[+] TẦNG 9: WINDOWS ECOSYSTEM (AD & KERNEL){Style.RESET_ALL}")
    ad_scanner = ADScanner(target_path)
    report_gen.add_section("Tầng 9: Windows Ecosystem (AD & Kernel)", ad_scanner.scan())
    
    driver_scanner = DriverScanner(target_path)
    report_gen.add_section("Tầng 9 (Secondary): Driver Analysis", driver_scanner.scan())

    # --- TẦNG 10: AI & WEAPONIZATION ---
    if args.ai_analyze:
        print(f"\n{Fore.GREEN}[+] TẦNG 10: AI BEHAVIORAL ANALYSIS & PWN{Style.RESET_ALL}")
        ai_analyzer = AIAnalyzer(report_gen.results)
        report_gen.add_section("Tầng 10: AI Behavioral Summary", ai_analyzer.run())

    if args.pwn:
        weaponizer = Weaponizer(target_path, report_gen.results)
        weaponizer.run([])

    # --- FINAL: REPORTING ---
    print("\n" + "-"*60)
    print(f"{Fore.WHITE}[*] GENERATING 100-VECTOR MISSION REPORT...{Style.RESET_ALL}")
    report_path = report_gen.generate()
    print(f"{Fore.GREEN}[+] COMPLETED. REPORT: {report_path}{Style.RESET_ALL}")
    return report_path

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="AUTOMATION PENTEST SYSTEM: The 100 Vectors Standard")
    parser.add_argument("-t", "--target", required=True, help="Path to PE file or directory")
    parser.add_argument("-o", "--output", default="reports", help="Output directory")
    parser.add_argument("--ai-analyze", action="store_true", help="AI Behavioral Predictions")
    parser.add_argument("--pwn", action="store_true", help="Weaponization Vectors")
    
    args = parser.parse_args()
    
    target_path = args.target
    if not os.path.exists(target_path):
        print(f"{Fore.RED}[!] Target '{target_path}' not found!{Style.RESET_ALL}")
        sys.exit(1)

    targets = [os.path.join(root, file) for root, _, files in os.walk(target_path) for file in files if file.lower().endswith(('.exe', '.dll', '.sys'))] if os.path.isdir(target_path) else [target_path]

    for t_path in targets:
        try:
            scan_single_file(t_path, args)
        except Exception as e:
            print(f"{Fore.RED}[!] Error in '{t_path}': {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
