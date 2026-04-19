import os
import pefile
from colorama import Fore, Style

# Import all scanner modules
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
from modules.exploit_verifier import ExploitVerifier
from modules.yara_scanner import YaraScanner

class APSEngine:
    """
    Core engine for APS scanning. 
    Decoupled from CLI for integration with Web UI.
    """
    
    def __init__(self):
        pass

    def is_pe_file(self, path):
        try:
            with open(path, 'rb') as f:
                return f.read(2) == b'MZ'
        except: return False

    def scan_file(self, target_path, output_dir="reports", ai_analyze=False, pwn=False, live_logger=None):
        """
        Scans a single file and returns the full result dictionary.
        live_logger: a function(string) to stream logs to UI
        """
        def log(msg, color=Fore.WHITE):
            formatted = f"{color}{msg}{Style.RESET_ALL}"
            if live_logger:
                live_logger(msg) # Raw msg for UI
            print(formatted)

        if not self.is_pe_file(target_path):
            log(f"[!] Unsupported Format: {target_path}", Fore.RED)
            return {"error": "Unsupported file format"}

        log(f"[*] STARTING AUDIT: {os.path.basename(target_path)}", Fore.CYAN)
        report_gen = ReportGenerator(target_path, output_dir)

        # 1. PE Metadata
        pe_metadata = {}
        try:
            pe = pefile.PE(target_path)
            pe_metadata = {
                "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
                "image_base": hex(pe.OPTIONAL_HEADER.ImageBase),
                "subsystem": pefile.SUBSYSTEM_TYPE.get(pe.OPTIONAL_HEADER.Subsystem, "Unknown"),
                "sections": []
            }
            for section in pe.sections:
                name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
                pe_metadata["sections"].append({
                    "name": name,
                    "entropy": round(section.get_entropy(), 2)
                })
            report_gen.add_section("PE Technical Forensics", pe_metadata)
        except: pass

        # 2. Yara
        log("[+] Layer 0: YARA Engine...")
        yara_scanner = YaraScanner(target_path)
        yara_findings = yara_scanner.scan()
        if yara_findings: report_gen.add_section("YARA Signature Analysis", yara_findings)

        # 3. Binary Protections
        log("[+] Layer 1-2: Binary Hardening...")
        bp_scanner = BinaryProtectionScanner(target_path)
        report_gen.add_section("Tầng 1-2: Mitigations & Authenticode", bp_scanner.scan())

        # 4. API Anomaly
        log("[+] Layer 3: IAT Anomaly...")
        api_scanner = APIScanner(target_path)
        report_gen.add_section("Tầng 3: API Anomaly & IAT Audit", api_scanner.scan())

        # 5. DLL Hijacking
        log("[+] Layer 4: DLL Hijacking...")
        hijack_scanner = DLLHijackingScanner(target_path)
        report_gen.add_section("Tầng 4: DLL Hijacking & Side-loading", hijack_scanner.scan())

        # 6. Resource/Manifest
        log("[+] Layer 5: Resource & Manifest...")
        manifest_scanner = WindowsServicesManifestScanner(target_path)
        report_gen.add_section("Tầng 5: Resource & Manifest (LPE)", manifest_scanner.scan())

        # 7. Packer
        log("[+] Layer 6: Packer/Entropy...")
        packer_scanner = PackerDetector(target_path)
        report_gen.add_section("Tầng 6: Packer, Entropy & Anti-RE", packer_scanner.scan())

        # 8. Crypto
        log("[+] Layer 7: Crypto Indicators...")
        crypto_scanner = CryptoScanner(target_path)
        report_gen.add_section("Tầng 7: Hardcoded Secrets & Crypto", crypto_scanner.scan())

        # 9. Local Storage
        log("[+] Layer 8: Local Storage...")
        scan_dir = os.path.dirname(os.path.abspath(target_path))
        storage_scanner = LocalStorageScanner(scan_dir)
        report_gen.add_section("Tầng 8: Local Storage & Data Privacy", storage_scanner.scan())

        # 10. Ecosystem
        log("[+] Layer 9: Ecosystem Audit...")
        ad_scanner = ADScanner(target_path)
        report_gen.add_section("Tầng 9: Windows Ecosystem (AD & Kernel)", ad_scanner.scan())
        
        driver_scanner = DriverScanner(target_path)
        report_gen.add_section("Tầng 9 (Secondary): Driver Analysis", driver_scanner.scan())

        # 11. Verification & Weaponization
        verification_results = []
        if ai_analyze or pwn:
            all_findings = []
            for section in report_gen.results.values():
                if isinstance(section, list): all_findings.extend(section)
            
            verifier = ExploitVerifier(target_path, all_findings)
            verification_results = verifier.run()
            report_gen.add_section("Exploit Verification (AEVF)", verification_results)

        if ai_analyze:
            log("[+] Layer 10: AI Behavior...")
            ai_analyzer = AIAnalyzer(report_gen.results)
            report_gen.add_section("Tầng 10: AI Behavioral Summary", ai_analyzer.run())

        if pwn:
            log("[!!] WEAPONIZING...")
            weaponizer = Weaponizer(target_path, report_gen.results)
            weaponizer.run(verification_results)

        # Generate report
        report_path = report_gen.generate()
        log(f"[+] Final Report Generated: {report_path}", Fore.GREEN)

        return {
            "target": target_path,
            "results": report_gen.results,
            "report_path": report_path,
            "pe_metadata": pe_metadata
        }
