import os
import sqlite3
import re
from colorama import Fore, Style

class LocalStorageScanner:
    """
    Quét khu vực lưu trữ của ứng dụng/Thư mục mục tiêu:
    - File cấu hình chứa mật khẩu nhạy cảm.
    - File SQLite DB chứa dữ liệu người dùng.
    - Quyền truy cập thư mục (ACLs).
    """
    def __init__(self, target_dir=None):
        self.target_dir = target_dir
        if not self.target_dir or not os.path.isdir(self.target_dir):
            self.target_dir = os.path.dirname(os.path.abspath(__file__)) if not target_dir else target_dir
        self.findings = []
        
    def scan(self):
        print(f"  {Fore.CYAN}[-]{Style.RESET_ALL} Quét Local Storage tại '{self.target_dir}'...")
        
        self.check_directory_permissions(self.target_dir)
        self.scan_sensitive_files(self.target_dir)
        
        return self.findings

    def check_directory_permissions(self, directory_path):
        is_writable = False
        try:
            test_file = os.path.join(directory_path, ".tcptf_write_test")
            with open(test_file, 'w') as f:
                f.write('pwn')
            os.remove(test_file)
            is_writable = True
        except (IOError, OSError):
            is_writable = False

        if is_writable:
            self.findings.append({
                "id": "FS-ACL-LPE",
                "name": "Writable Target Directory (LPE Risk)",
                "severity": "HIGH",
                "privilege": "Standard User",
                "description": f"Thư mục '{directory_path}' cho phép người dùng hiện tại ghi file. Có rủi ro DLL/Binary Hijacking."
            })

    def scan_sensitive_files(self, base_dir):
        patterns = {
            "Config & Env Files": r".*\.(ini|config|json|xml|yaml|yml|env)$",
            "Local Database": r".*\.(db|sqlite|sqlite3)$",
            "Sensitive Files": r".*(id_rsa|credentials|secrets.*)$"
        }
        
        found_files = []
        # Chỉ quét trong thư mục mục tiêu (Black-box Scope)
        for root, dirs, files in os.walk(base_dir):
            if any(x in root for x in ['.git', 'node_modules']): continue
            for file in files:
                file_path = os.path.join(root, file)
                for cat, pat in patterns.items():
                    if re.match(pat, file.lower()):
                        found_files.append((cat, file_path))

        for category, path in found_files:
            if "Database" in category:
                self._analyze_sqlite(path)
            else:
                 self._scan_file_content(path, category)

    def _analyze_sqlite(self, db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            sensitive_tables = [t[0] for t in tables if any(k in t[0].lower() for k in ['user', 'pass', 'auth', 'token', 'cred'])]
            
            if sensitive_tables:
                self.findings.append({
                    "id": "FS-DB-001",
                    "name": "Sensitive Local SQLite Database",
                    "severity": "HIGH",
                    "details": f"Database tại '{db_path}' chứa các bảng nhạy cảm: {sensitive_tables}."
                })
        except: pass

    def _scan_file_content(self, filepath, category):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Simple Password Pattern Hunt
            cred_match = re.search(r"(?i)(password|passwd|pwd|secret|key)\s*[:=]\s*['\"]?([^'\"\n\s]{4,})['\"]?", content)
            if cred_match:
                self.findings.append({
                    "id": "FS-SEC-002",
                    "name": f"Cleartext Credential in {category}",
                    "severity": "HIGH",
                    "username": "System/File",
                    "password": cred_match.group(2),
                    "details": f"File '{filepath}' chứa thông tin xác thực ghi rõ bài văn bản (Cleartext).",
                    "is_vault_item": True
                })
        except: pass
