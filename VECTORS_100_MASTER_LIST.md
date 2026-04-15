# 📜 AUTOMATION PENTEST SYSTEM: 100 VECTORS MASTER LIST

Tài liệu này là danh sách đầy đủ 100 Vector kiểm thử tiêu chuẩn của hệ thống **APS**, được phân loại thành 10 Tầng Chiến Lược. Đây là "Nguồn sự thật" (Source of Truth) cho mọi quy trình audit và báo cáo chuyên nghiệp.

---

## 🏛️ Tầng 1: Binary Hardening (STT 1-10)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **ASLR Audit** | Ngẫu nhiên hóa địa chỉ bộ nhớ | winchecksec | Kiểm tra DllCharacteristics flags |
| 2 | **DEP/NX Audit** | Chống thực thi trên ngăn xếp | DIE-cli | Xác thực NX_COMPAT bit |
| 3 | **Intel CET Check** | Bảo vệ Stack phần cứng | Intel Inspector | Kiểm tra CET compatibility metadata |
| 4 | **CFG Validation** | Bảo vệ luồng gọi hàm gián tiếp | dumpbin | Phân tích bitmap Forwarding |
| 5 | **SafeSEH Audit** | Bảo vệ Exception Handler | PE-bear | Kiểm tra bảng SEH được tin cậy |
| 6 | **Stack Cookie (GS)** | Chống tràn bộ đệm ngăn xếp | x64dbg | Phân tích Security Cookie tại hàm |
| 7 | **High Entropy ASLR** | ASLR độ phân giải cao | PESecurity | Kiểm tra High entropy flag |
| 8 | **PIE / DYN Base** | Độc lập vị trí thực thi | pefile | Xác định Relocation table integrity |
| 9 | **RFG Check** | Return Flow Guard | MSVC Audit | Kiểm tra RFG instrumentation |
| 10 | **Control Flow Integrity**| Bảo vệ tính toàn vẹn luồng | Clang-CFI | Phân tích CFI metadata |

## 📜 Tầng 2: Authenticode & Metadata (STT 11-20)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 11 | **Digital Signature** | Xác thực nguồn gốc binary | Sigcheck | Kiểm tra Certificate chain trust |
| 12 | **PDB Symbol Leak** | Thu thập thông tin phát triển | dumpbin /pdb | Trích xuất đường dẫn build PDB |
| 13 | **CLR Metadata Scan** | Kiểm tra .NET internals | dnSpy | Phân tích CLR Header & Manifest |
| 14 | **PE Header Anomaly** | Phát hiện cấu trúc file lạ | PE-bear | So sánh Header thực tế vs Chuẩn |
| 15 | **Section Alignment** | Phát hiện chèn mã thủ công | pefile | Kiểm tra chênh lệch Padding/Alignment |
| 16 | **Debug Dir Scan** | Dấu vết từ quá trình debug | CFF Explorer | Phân tích IMAGE_DEBUG_DIRECTORY |
| 17 | **Export Table Audit** | Kiểm tra các hàm được công khai | Dependency Walker | Phân tích EAT tìm các hàm nhạy cảm |
| 18 | **Rich Header Scan** | Fingerprinting compiler | DIE | Phân tích MSVC Rich Header metadata |
| 19 | **Manifest Signature** | Xác thực file khai báo XML | XMLSign | Kiểm tra chữ ký trong Manifest.xml |
| 20 | **Revocation Check** | Kiểm tra chứng chỉ bị thu hồi | certutil | Phân tích CRL/OCSP status |

## 💉 Tầng 3: API Anomaly & IAT Audit (STT 21-30)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 21 | **Process Injection** | Phát hiện kỹ thuật tiêm mã | APIScanner | Quét OpenProcess/WriteProcessMemory |
| 22 | **Anti-Debug API** | Phát hiện chống phân tích | ScyllaHide | Tìm IsDebuggerPresent/NtGlobalFlag |
| 23 | **Anti-VM Detection** | Phát hiện né tránh máy ảo | APS Custom | Quét các hàm truy vấn MAC/CPU ID |
| 24 | **Kernel Interaction**| Giao tiếp thiết bị hệ thống | IrpTracker | Phân tích mã điều khiển IOCTL |
| 25 | **Service Controller** | Thao tác dịch vụ Windows | APIScanner | Quét OpenSCManager/CreateService |
| 26 | **Privilege Escalation**| Tăng quyền hạn luồng | APS Custom | Tìm OpenProcessToken/AdjustPrivileges |
| 27 | **Network Capability** | Khả năng kết nối Internet | APIScanner | Quét InternetOpen/WSAStartup |
| 28 | **Cryptography Usage** | Sử dụng hàm băm/mã hóa | APS Custom | Tìm CryptAcquireContext/BCryptOpen |
| 29 | **File Sys Tampering** | Thao tác tệp tin hệ thống | APS Custom | Quét CreateFileW/ReplaceFile |
| 30 | **Thread Management** | Quản lý đa luồng nhạy cảm | APS Custom | Quét CreateRemoteThread/QueueUserAPC |

## 🏗️ Tầng 4: DLL Hijacking & Side-loading (STT 31-40)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 31 | **Search Order Audit** | Khai thác thứ tự nạp DLL | ProcMon | Tìm DLL nạp từ thư mục ứng dụng |
| 32 | **Missing DLL Audit** | Khai thác các DLL bị thiếu | Dependencies | Tìm thư viện App cố nạp nhưng k thấy |
| 33 | **DLL Proxying** | Chiếm quyền qua Library Proxy | DLLHijackingScanner | Phân tích IAT tìm DLL có thể thay thế |
| 34 | **KnownDlls Bypass** | Vượt qua danh sách DLL an toàn | APS Custom | Kiểm tra các kỹ thuật link redirection |
| 35 | **Sxs Override Audit** | Khai thác Side-by-Side manifest | APS Custom | Phân tích .local file redirection |
| 36 | **Env Path Injection** | Leo thang qua biến môi trường | ProcMon | Kiểm tra %PATH% shadowing |
| 37 | **Manifest Hijack** | Chèn DLL qua manifest nạp | XML Editor | Sửa đổi dependency trong Manifest |
| 38 | **Com Hijacking** | Chèn DLL qua COM server | OleViewDotNet | Phân tích InprocServer32 Registry |
| 39 | **AppInit_DLLs Check** | Tự động load DLL qua registry | Autoruns | Kiểm tra AppInit_DLLs hooks |
| 40 | **Shim Hijacking** | Khai thác Application Shims | Compatibility Admin | Phân tích .sdb database hooks |

## 🎭 Tầng 5: Resource & Manifest Audit (STT 41-50)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 41 | **UAC Level Check** | Đặc quyền yêu cầu của App | Sigcheck | Phân tích `requestedExecutionLevel` |
| 42 | **Auto-Elevate Check** | Khả năng bỏ qua xác nhận Admin | APS Custom | Quét `autoElevate` flag trong XML |
| 43 | **Res Encryption** | Mã hóa tài nguyên ứng dụng | Resource Hacker | Phân tích tính Entropy của Resource |
| 44 | **Overlay Deep Scan** | Tìm shellcode đính kèm file | binwalk | Phân tích dữ liệu dư thừa cuối file |
| 45 | **Icon Spoofing** | Phát hiện app giả mạo icon | APS Custom | So sánh Icon MD5 hash |
| 46 | **String Table Audit** | Tìm thông rò rỉ trong Resource | Resource Hacker | Quét chuỗi nhạy cảm trong String Table |
| 47 | **Version Info Audit** | Kiểm tra khớp thông tin phiên bản | CFF Explorer | So sánh FileInfo vs Header |
| 48 | **XML Schema Val** | Kiểm tra lỗi cấu trúc Manifest | XMLSpy | Phân tích định dạng XML rò rỉ |
| 49 | **Manifest Sign Val** | Chữ ký số cho file khai báo | certutil | Xác thực Authenticode cho Manifest |
| 50 | **Compatibility Audit**| Khả năng tương thích OS | APS Custom | Phân tích SupportedOS GUIDs |

## 🌀 Tầng 6: Packer, Entropy & Anti-RE (STT 51-60)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 51 | **Entropy Analysis** | Đo độ hỗn loạn dữ liệu | Shannon Engine | Tính toán entropy từng section |
| 52 | **Packer Signature** | Nhận diện chữ kỹ các bộ nén | DIE | So sánh bytecode vs DB Packer |
| 53 | **TLS Callback Scan** | Phát hiện code chạy trước Main | x64dbg | Phân tích TLS directory entries |
| 54 | **OEP Obfuscation** | Phát hiện Entry Point bị đổi | PE-bear | Kiểm tra JMP/PUSH tại Entry Point |
| 55 | **Anti-Dump Logic** | Chống dump bộ nhớ RAM | APS Custom | Tìm kỹ thuật Header Erasing |
| 56 | **Anti-Patching** | Chống sửa đổi mã nguồn | APS Custom | Quét mã tự kiểm tra Integrity |
| 57 | **Code Virtualization**| Phát hiện mã bị ảo hóa | APS Custom | Tìm máy ảo trung gian xử lý opcode |
| 58 | **Flow Flattening** | Phát hiện làm phẳng luồng điều khiển | Ghidra | Phân tích cấu trúc Switch/Case khổng lồ |
| 59 | **String Encrypt** | Phát hiện chuỗi đã được mã hóa | APS Custom | Tìm hàm xor/decryption logic |
| 60 | **Junk Code Check** | Phát hiện mã rác | APS Custom | Phân tích tỷ lệ Opcode thực thi |

## 🗝️ Tầng 7: Hardcoded Secrets & Crypto (STT 61-70)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 61 | **AWS Access Key** | Rò rỉ thông tin AWS Cloud | CryptoScanner | Quét pattern AKIA[0-9A-Z]{16} |
| 62 | **Google API Key** | Rò rỉ khóa dịch vụ Google | CryptoScanner | Quét AIza[0-9A-Za-z-_]{35} |
| 63 | **RSA Private Key** | Rò rỉ khóa mật mã riêng tư | CryptoScanner | Tìm chuỗi BEGIN RSA PRIVATE KEY |
| 64 | **Hardcoded Pass** | Mật khẩu ghi cứng trong mã | CryptoScanner | Regex mining logic (pass|pwd|secret) |
| 65 | **Weak Hash Usage** | Sử dụng thuật toán băm yếu | APS Custom | Tìm hằng số MD5/SHA1 constants |
| 66 | **Custom Crypto** | Phát hiện thuật toán tự chế | APS Custom | Phân tích hằng số toán học lạ |
| 67 | **Hardcoded IVs** | Dùng Vectơ khởi tạo cố định | APS Custom | Tìm hằng số truyền vào hàm AES/DES |
| 68 | **Cert Embedding** | Nhúng chứng chỉ thô trong file | APS Custom | Tìm chuỗi X.509 certificate headers |
| 69 | **OAuth Tokens** | Rò rỉ token xác thực | CryptoScanner | Quét JWT/OAuth Bearer patterns |
| 70 | **Firebase URL** | Rò rỉ URL cơ sở dữ liệu cloud | CryptoScanner | Tìm pattern *.firebaseio.com |

## 📂 Tầng 8: Local Storage & Data Privacy (STT 71-80)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 71 | **SQLite Table Scan** | Phân tích bảng nhạy cảm DB | LocalStorageScanner | Phân tích schema SQLite tìm 'users' |
| 72 | **JSON Config Audit** | Tìm khóa trong file JSON | APS Custom | Quét khóa nhạy cảm trong appsettings |
| 73 | **XML Config Audit** | Tìm khóa trong file XML | APS Custom | Quét credential trong web.config |
| 74 | **Registry Key Audit**| Kiểm tra dữ liệu trong Registry | APS Custom | Phân tích `Software\<AppName>` keys |
| 75 | **Env Variable Leak**| Tìm bí mật trong file .env | APS Custom | Quét file ẩn .env trong thư mục App |
| 76 | **Log File Audit** | Tìm thông nhạy cảm trong Log | APS Custom | Quét file .log tìm 'password' |
| 77 | **Temp File Audit** | Tìm dữ liệu rác nhạy cảm | APS Custom | Kiểm tra %TEMP% app identifiers |
| 78 | **Browser Cache** | Dữ liệu rò rỉ qua WebView | APS Custom | Phân tích Local Storage của Chromium |
| 79 | **Installer Script**| Lỗi bảo mật từ bộ cài | APS Custom | Phân tích MSI/InnoSetup scripts |
| 80 | **Crash Dump Audit** | Dữ liệu nhạy cảm trong dump | APS Custom | Phân tích file .dmp rò rỉ RAM |

## 🏰 Tầng 9: Windows Ecosystem Audit (STT 81-90)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 81 | **GPP Password** | Rò rỉ mật khẩu AD | ADScanner | Giải mã cpassword từ Groups.xml |
| 82 | **AD Delegation** | Lỗi ủy quyền domain nhạy cảm | ADScanner | Kiểm tra Unconstrained Delegation |
| 83 | **Kerberoasting Cx** | Phân tích SPN service accounts | ADScanner | Thu thập SPNs cho brute-force offline |
| 84 | **Driver IOCTL** | Lỗi giao tiếp kernel driver | DriverScanner | Phân tích mã điều khiển thiết bị |
| 85 | **Filter Driver** | Phát hiện driver lọc traffic | APS Custom | Kiểm tra các driver nạp theo App |
| 86 | **Service Security** | Quyền hạn dịch vụ Windows | APS Custom | Phân tích ACLs của Windows Service |
| 87 | **Scheduled Tasks** | Khai thác tác vụ lập lịch | APS Custom | Kiểm tra các task tự động chạy app |
| 88 | **WMI Persistence** | Chạy app ngầm qua WMI | APS Custom | Phân tích WMI Event Consumers |
| 89 | **COM Reg Audit** | Lỗi đăng ký đối tượng COM | APS Custom | Kiểm tra InprocServer32 permissions |
| 90 | **RPC Interfaces** | Khai thác giao tiếp RPC nội bộ | APS Custom | Phân tích các endpoint RPC của App |

## 🤖 Tầng 10: AI Intelligence & Weaponizer (STT 91-100)
| STT | Vector Name | Objective | Tools | Pentest Technique |
| :--- | :--- | :--- | :--- | :--- |
| 91 | **AI Risk Scoring** | Chấm điểm rủi ro tổng thể | AIAnalyzer | LLM-based behavioral scoring |
| 92 | **PoC Generation** | Tự động sinh mã khai thác | Weaponizer | Template-based exploit generator |
| 93 | **Behavior Predict** | Dự đoán luồng thực thi xấu | AIAnalyzer | Pattern matching logic flows |
| 94 | **Logic Flaw Audit** | Tìm lỗi nghiệp vụ qua AI | AIAnalyzer | Phân tích Semantic logic errors |
| 95 | **Anomaly Detection**| Phát hiện mẫu tấn công lạ | AIAnalyzer | So sánh hành vi vs Baseline an toàn |
| 96 | **Exploit Stability**| Đo độ ổn định của mã độc | Weaponizer | Phân tích độ tin cậy của payload |
| 97 | **Payload Crafting** | Tối ưu hóa mã payload | Weaponizer | Đa dạng hóa bytecode chống AV |
| 98 | **Delivery Method** | Kỹ thuật vận chuyển app | APS Custom | Phân tích vector Phishing/Dropper |
| 99 | **Clean-up Logic** | Dọn dẹp dấu vết sau tấn công | Weaponizer | Tự động sinh script xóa log |
| 100 | **Mission Report** | Xuất báo cáo chiến lược | ReportGenerator | Tổng hợp 100 vectors chuẩn Pro |

---
*Tài liệu này được bảo mật và biên soạn bởi Đội ngũ AUTOMATION PENTEST SYSTEM.*
