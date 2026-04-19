# 🛡️ AUTOMATION PENTEST SYSTEM (APS)

Chào mừng bạn đến với **AUTOMATION PENTEST SYSTEM** - Giải pháp đánh giá an ninh chuyên sâu và tự động hóa quy trình Pentest cho các ứng dụng Thick Client (môi trường Windows PE).

## 🌟 Tổng quan Hệ thống
AUTOMATION PENTEST SYSTEM là một framework mạnh mẽ được thiết kế để hỗ trợ các chuyên gia an ninh mạng trong việc phân tích tệp tin thực thi mà không cần can thiệp thủ công quá nhiều. Hệ thống tập trung vào việc phát hiện các lỗ hổng từ mức bit-level đến các lỗi logic nghiệp vụ phức tạp thông qua mô hình **10 Tầng Tác Chiến (The 100 Vectors Standard)**.

## 🚀 Tính năng Cốt lõi
*   **Deep Static Analysis**: Kiểm tra toàn diện các cơ chế bảo vệ (ASLR, DEP, CET, CFG).
*   **API Behavioral Audit**: Phân tích bảng Import để dự đoán hành vi nhạy cảm của ứng dụng.
*   **Privilege Escalation Detection**: Tìm kiếm các kịch bản leo thang đặc quyền thông qua Manifest và DLL Hijacking.
*   **Secrets & Forensic Scavenging**: Tự động khai quật các thông tin nhạy cảm bị rò rỉ trong file cấu hình và cơ sở dữ liệu.
*   **AI-Enhanced Reporting**: Tích hợp trí tuệ nhân tạo để thẩm định rủi ro và đưa ra khuyến nghị khắc phục chuẩn chuyên gia.
*   **Portable Auto-Compile (Zig Engine)**: Tự động biên dịch mã nguồn C thành file thực thi (.dll/.exe) ngay lập tức với công nghệ Tự cài đặt trình biên dịch Portable.
*   **Just-In-Time Weaponization**: Cơ chế "Gác cổng" thông minh, chỉ sinh Payload và thư mục khi phát hiện lỗ hổng thực tế, giữ sạch không gian dự án.
*   **Ghost-Protocol Tier-3 (No-IAT)**: Công nghệ tàng hình cao cấp, xóa bỏ mọi dấu vết hàm hệ thống (IAT) bằng kỹ thuật PEB Walking và API Hashing, giúp vượt qua các trình diệt virus (AV/EDR) hiện đại nhất.

## 🛠️ Hướng dẫn Sử dụng (Nhanh)
Để vận hành hệ thống, quý khách vui lòng sử dụng lệnh sau trong terminal:

```bash
# Quét một file mục tiêu đơn lẻ
python3 main.py -t <path_to_pe_file>

# Quét hàng loạt trong một thư mục và kích hoạt AI thẩm định
python3 main.py -t <directory_path> --ai-analyze

# Quét và tự động sinh mã khai thác mẫu (PoC)
python3 main.py -t <path_to_pe_file> --pwn
```

---

# 🚀 TÀI LIỆU KỸ THUẬT TỔNG HỢP (ULTIMATE DOCUMENTATION)

Đây là nguồn tài liệu duy nhất chứa đựng tất cả kiến thức từ lý thuyết, kỹ thuật cho đến vận hành thực chiến của hệ thống **APS (Professional Edition)**.

## 📑 MỤC LỤC
1.  [**Giới thiệu & Triết lý thiết kế**](#1-giới-thiệu--triết-lý-thiết-kế)
2.  [**Cơ sở Lý thuyết Khoa học**](#2-cơ-sở-lý-thuyết-khoa-học)
3.  [**Hướng dẫn Vận hành Chuyên sâu (CLI & Web Dashboard)**](#3-hướng-dẫn-vận-hành-chuyên-sâu-cli--web-dashboard)
4.  [**Chi tiết 100 Vectors & 10 Tầng Tác chiến**](#4-chi-tiết-100-vectors--10-tầng-tác-chiến)
5.  [**Quy trình Phân loại Rủi ro & Xác thực (Blueprint)**](#5-quy-trình-phân-loại-rủi-ro--xác-thực-blueprint)
6.  [**Cẩm nang Pentest & Reverse Engineering**](#6-cẩm-nang-pentest--reverse-engineering)
7.  [**Hướng dẫn Khai thác & Sử dụng Payload (PoC)**](#7-hướng-dẫn-khai-thác--sử-dụng-payload-poc)
8.  [**Danh mục 100 Payloads (Payload Master List)**](#8-danh-mục-100-payloads-payload-master-list)

---

## 1. Giới thiệu & Triết lý thiết kế
Hãy tưởng tượng phần mềm giống như một ngôi nhà. APS là một **"Đội kiểm định nhà thông minh"**. 
- Nó không cần đập phá nhà (không chạy file mã độc thật).
- Nó chỉ cần đứng ngoài, soi đèn pin vào cửa sổ, kiểm tra ổ khóa, xem tường có nứt không (**Tĩnh học - Static Analysis**).
- Cuối cùng, nó sẽ nói cho bạn biết: "Chỗ này trộm có thể lẻn vào được đấy!" và đưa cho bạn bằng chứng (Payload).

> [!TIP]
> APS bảo vệ hệ thống của bạn bằng cách chỉ ra lỗ hổng trước khi hacker tìm thấy chúng.

---

## 2. Cơ sở Lý thuyết Khoa học
Hệ thống dựa trên 7 trụ cột lý thuyết cốt lõi:

| STT | Tên Cơ sở Lý thuyết | Ứng dụng trong Project (APS) |
| :--- | :--- | :--- |
| **1** | **Cấu trúc PE (Portable Executable)** | Phân tích Headers, Sections, IAT/EAT của EXE/DLL/SYS. |
| **2** | **Memory Management** | Phát hiện lỗ hổng DLL Hijacking, Privilege Escalation. |
| **3** | **Shannon Entropy** | Nhận diện mã nguồn bị nén (Packer) hoặc mã hóa (Crypter). |
| **4** | **Static Program Analysis** | Thẩm định thuộc tính phần mềm mà không cần thực thi mã. |
| **5** | **Cryptography & PKI** | Giải mã mật khẩu nhúng, xác thực chữ ký Authenticode. |
| **6** | **Attack Surface Modeling** | Dựa trên MITRE ATT&CK để phân loại hành vi tấn công. |
| **7** | **AI & Transformers** | Dự đoán rủi ro thông minh & Tự động sinh mã khai thác mẫu. |

---

## 3. Hướng dẫn Vận hành Chuyên sâu (CLI & Web Dashboard)

### 🖥️ A. Giao diện Dòng lệnh (CLI)
Dành cho các chuyên gia cần xử lý hàng loạt:
```bash
python3 main.py -t <đường_dẫn_file_hoặc_thư_mục> --pwn --ai-analyze
```
- `-t`: File/Thư mục cần quét.
- `--pwn`: Kích hoạt sinh mã khai thác PoC.
- `--ai-analyze`: Kích hoạt phân tích hành vi bằng AI.

### 🌐 B. Giao diện Web Dashboard (MỚI)
Dành cho trải nghiệm trực quan và thực chiến:
1.  Chạy lệnh: `python3 server.py`
2.  Truy cập: **`http://localhost:5050`** trên trình duyệt.
- Giao diện **Glassmorphism** chuyên nghiệp.
- Hiển thị tiến trình qua **10 Tầng Tác chiến**.
- Quản lý kho **Weapons Repository** trực tiếp trên Dashboard.
- **AI Groq Integration**: Hỗ trợ nhập API Key trực tiếp trên giao diện để kích hoạt bộ não Llama 3 (70B) phân tích thực chiến.

---

## 4. Chi tiết 100 Vectors & 10 Tầng Tác chiến

Dưới đây là danh sách toàn diện 100 Vector kiểm thử tiêu chuẩn của hệ thống APS, được đồng bộ với Engine Ghost-Protocol v3.

### 🏛️ Tầng 1: Binary Hardening (STT 1-10)
| STT | Tên Vector | Mục tiêu kiểm thử | Công cụ | Kỹ thuật Tác chiến (Mới nhất) |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **ASLR Audit** | Ngẫu nhiên hóa địa chỉ | winchecksec | Kiểm tra các cờ DllCharacteristics. |
| 2 | **DEP/NX Audit** | Chống thực thi ngăn xếp | DIE-cli | Xác thực bit NX_COMPAT. |
| 3 | **Intel CET Check** | Bảo vệ Stack phần cứng | Intel Inspector | Kiểm tra metadata tương thích CET. |
| 4 | **CFG Validation** | Bảo vệ luồng gọi hàm | dumpbin | Phân tích bitmap Forwarding. |
| 5 | **SafeSEH Audit** | Bảo vệ Exception Handler | PE-bear | Kiểm tra bảng SEH được tin cậy. |
| 6 | **Stack Cookie (GS)** | Chống tràn bộ đệm | x64dbg | Phân tích Security Cookie tại các hàm. |
| 7 | **High Entropy ASLR** | ASLR độ phân giải cao | PESecurity | Kiểm tra cờ High entropy (64-bit). |
| 8 | **PIE / DYN Base** | Độc lập vị trí thực thi | pefile | Xác định tính toàn vẹn bảng Relocation. |
| 9 | **RFG Check** | Return Flow Guard | MSVC Audit | Kiểm tra instrumentation của RFG. |
| 10 | **UI Shatter (UP)** | Tấn công giao diện | APS Custom | **Tiêm tin nhắn xuyên phiên làm việc.** |

### 📜 Tầng 2: Authenticode & Metadata (STT 11-20)
| STT | Tên Vector | Mục tiêu kiểm thử | Công cụ | Kỹ thuật Tác chiến |
| :--- | :--- | :--- | :--- | :--- |
| 11 | **Digital Signature** | Xác thực nguồn gốc | Sigcheck | Kiểm tra chuỗi tin cậy Certificate. |
| 12 | **Race Condition** | Lỗi tranh chấp (UP) | APS Custom | **Kiểm định bản sao Handle/TOCTOU.** |
| 13 | **CLR Metadata Scan** | Kiểm tra nội hàm .NET | dnSpy | Phân tích CLR Header & Manifest. |
| 14 | **PE Header Anomaly** | Cấu trúc file bất thường | PE-bear | So sánh Header thực tế vs chuẩn PE. |
| 15 | **Section Alignment** | Chèn mã thủ công | pefile | Kiểm tra chênh lệch Padding/Alignment. |
| 16 | **Debug Dir Scan** | Dấu vết gỡ lỗi | CFF Explorer | Phân tích IMAGE_DEBUG_DIRECTORY. |
| 17 | **Symbolic Aid (UP)** | Dấu vết lập trình | Microsoft PDB | **Tự động khai thác cấu trúc file PDB.** |
| 18 | **Rich Header Scan** | Nhận diện trình biên dịch | DIE | Phân tích metadata MSVC Rich Header. |
| 19 | **Manifest Signature** | Xác thực XML | XMLSign | Kiểm tra chữ ký trong Manifest.xml. |
| 20 | **Revocation Check** | Chứng chỉ bị thu hồi | certutil | Phân tích trạng thái CRL/OCSP. |

### 💉 Tầng 3: API Anomaly & IAT Audit (STT 21-30)
| STT | Tên Vector | Mục tiêu kiểm thử | Công cụ | Kỹ thuật Tác chiến (Mới nhất) |
| :--- | :--- | :--- | :--- | :--- |
| 21 | **Process Injection** | Tiêm mã độc | APIScanner | Quét các hàm OpenProcess/WriteProcessMemory. |
| 22 | **Anti-Debug API** | Chống phân tích | ScyllaHide | Tìm IsDebuggerPresent/NtGlobalFlag. |
| 23 | **Anti-VM Detection** | Né tránh máy ảo | APS Custom | Quét các hàm truy vấn ID phần cứng. |
| 24 | **Native Syscall** | Vượt mặt EDR/AV (UP) | **Halo's Gate** | **Trích xuất SSN trực tiếp từ ntdll.** |
| 25 | **SMC PoC (UP)** | Mã tự thay đổi | APS Custom | **Giải mã mã nguồn trong thời gian chạy.** |
| 26 | **Reflective Stub** | Nạp mã từ bộ nhớ | x64dbg | Phân tích cấu trúc reflective loader. |
| 27 | **Network Capability** | Kết nối Internet | APIScanner | Quét InternetOpen/WSAStartup. |
| 28 | **IAT Loader Audit** | Nạp hàm ẩn danh | APS Custom | Phân tích nạp hàm qua tên băm (Hashing). |
| 29 | **File Sys Tampering** | Thao tác tệp hệ thống | APS Custom | Quét CreateFileW/ReplaceFile. |
| 30 | **Thread Management** | Quản lý luồng nhạy cảm | APS Custom | Quét CreateRemoteThread/QueueUserAPC. |

### 🏗️ Tầng 4: DLL Hijacking & Side-loading (STT 31-40)
| STT | Tên Vector | Mục tiêu kiểm thử | Công cụ | Kỹ thuật Tác chiến (Mới nhất) |
| :--- | :--- | :--- | :--- | :--- |
| 31 | **Search Order Audit** | Thứ tự nạp thư viện | ProcMon | Tìm DLL nạp sai vị trí ưu tiên. |
| 32 | **Phantom DLL (UP)** | DLL bị thiếu hoàn toàn | Dependencies | **Khai thác DLL không có Export.** |
| 33 | **DLL Proxying** | Chiếm quyền qua Proxy | Weaponizer | Tạo Proxy DLL giữ nguyên hàm gốc. |
| 34 | **Delay Load Hijack**| Lỗi nạp DLL trễ | Dumpbin | Phân tích bảng Delay Import. |
| 35 | **SafeSearch Exploit**| Vượt Safe Search Order | APS Custom | Khai thác cơ chế nạp không an toàn. |
| 36 | **Env Path Injection**| Shadowing biến %PATH% | ProcMon | Kiểm tra độ ưu tiên biến môi trường. |
| 37 | **Manifest Hijack** | Chèn DLL qua Manifest | XML Editor | Sửa đổi dependency trong XML. |
| 38 | **Com Hijacking** | Chèn DLL qua COM | OleViewDotNet | Phân tích InprocServer32 Registry. |
| 39 | **AppInit_DLLs** | Tự động load qua Reg | Autoruns | Kiểm tra AppInit_DLLs hooks. |
| 40 | **Shim Hijacking** | Khai thác App Shims | CompAdmin | Phân tích cơ sở dữ liệu .sdb. |

### 🎭 Tầng 5: Resource & Manifest Audit (STT 41-50)
| STT | Tên Vector | Mục tiêu kiểm thử | Công cụ | Kỹ thuật Tác chiến |
| :--- | :--- | :--- | :--- | :--- |
| 41 | **UAC Level Check** | Đặc quyền yêu cầu | Sigcheck | Phân tích mức `requestedExecutionLevel`. |
| 42 | **UIAccess Bypass** | Quyền tương tác UI | APS Custom | Quét cờ `uiAccess` nâng cao. |
| 43 | **Auto-Elevate** | Tự leo thang quyền | APS Custom | Quét cờ `autoElevate` trong Manifest. |
| 44 | **Overlay Deep Scan**| Shellcode đính kèm | binwalk | Phân tích dữ liệu dư thừa cuối file. |
| 45 | **Icon Spoofing** | Giả mạo biểu tượng | APS Custom | So sánh mã băm MD5 của Icon. |
| 46 | **Resource Dump** | Trích xuất tài nguyên | ResHacker | Tìm kiếm thông tin nhạy cảm trong Resource. |
| 47 | **Version Anomaly** | Sai lệch thông tin file | CFF Explorer | So sánh FileInfo vs Header thực tế. |
| 48 | **XML Schema Val** | Lỗi cấu trúc Manifest | XMLSpy | Phân tích định dạng XML rò rỉ thông tin. |
| 49 | **Manifest Sign Val**| Chữ ký cho XML | certutil | Xác thực Authenticode cho Manifest. |
| 50 | **OS Compatibility** | Tương thích Windows | APS Custom | Phân tích SupportedOS GUIDs. |

### 🌀 Tầng 6: Packer, Entropy & Anti-RE (STT 51-60)
| STT | Tên Vector | Mục tiêu kiểm thử | Công cụ | Kỹ thuật Tác chiến (Mới nhất) |
| :--- | :--- | :--- | :--- | :--- |
| 51 | **Entropy (UP)** | Độ hỗn loạn dữ liệu | Shannon Engine | **Phân tích entropy đa tầng.** |
| 52 | **Packer Signature** | Nhận diện bộ nén | DIE | So sánh bytecode với database Packer. |
| 53 | **TLS Callback Scan**| Mã chạy trước hàm Main | x64dbg | Phân tích thư mục TLS trong Header. |
| 54 | **OEP Obfuscation** | Làm nhiễu điểm vào | PE-bear | Kiểm tra lệnh JMP/PUSH lạ tại EP. |
| 55 | **Anti-Dump Logic** | Chống trích xuất RAM | APS Custom | Tìm kỹ thuật xóa Header khi thực thi. |
| 56 | **Heaven's Gate(UP)**| Thoát x86 sang x64 | **Mode Switching** | **Kỹ thuật chuyển đổi kiến trúc ngầm.** |
| 57 | **Sandbox Gate(UP)**| Né tránh môi trường ảo | APS Custom | **Kiểm tra hành vi người dùng thực.** |
| 58 | **RDTSC Check (UP)**| Phân tích thời gian | APS Custom | **Phân tích độ trễ phần cứng.** |
| 59 | **String Encrypt** | Chuỗi bị mã hóa | APS Custom | Tìm thuật toán giải mã chuỗi (XOR/AES). |
| 60 | **Junk Code Check** | Phát hiện mã rác | APS Custom | Phân tích tỷ lệ tập lệnh vô nghĩa. |

### 🗝️ Tầng 7: Hardcoded Secrets & Crypto (STT 61-70)
| STT | Tên Vector | Mục tiêu kiểm thử | Công cụ | Kỹ thuật Tác chiến |
| :--- | :--- | :--- | :--- | :--- |
| 61 | **AWS Access Key** | Rò rỉ Cloud AWS | CryptoScanner | Quét mẫu AKIA[0-9A-Z]{16}. |
| 62 | **Google API Key** | Rò rỉ khóa Google | CryptoScanner | Quét mẫu AIza[0-9A-Za-z-_]{35}. |
| 63 | **RSA Private Key** | Rò rỉ khóa bí mật | CryptoScanner | Tìm chuỗi BEGIN RSA PRIVATE KEY. |
| 64 | **Hardcoded Pass** | Mật khẩu ghi cứng | CryptoScanner | Khai thác regex (pass\|pwd). |
| 65 | **Weak Hash Usage** | Thuật toán băm yếu | APS Custom | Tìm hằng số MD5/SHA1 nhúng trong mã. |
| 66 | **Custom Crypto** | Thuật toán tự chế | APS Custom | Phân tích hằng số toán học bất thường. |
| 67 | **Hardcoded IVs** | Vectơ khởi tạo tĩnh | APS Custom | Tìm hằng số tĩnh truyền vào hàm AES. |
| 68 | **Cert Embedding** | Nhúng chứng chỉ thô | APS Custom | Tìm chuỗi định dạng X.509. |
| 69 | **OAuth Tokens** | Rò rỉ token truy cập | CryptoScanner | Quét các mẫu JWT/OAuth Bearer. |
| 70 | **Firebase URL** | Rò rỉ cơ sở dữ liệu | CryptoScanner | Tìm địa chỉ *.firebaseio.com. |

### 📂 Tầng 8: Local Storage & Data Privacy (STT 71-80)
| STT | Tên Vector | Mục tiêu kiểm thử | Công cụ | Kỹ thuật Tác chiến |
| :--- | :--- | :--- | :--- | :--- |
| 71 | **SQLite Table Scan**| Thu thập bảng nhạy cảm| LocalStorage | Trích xuất schema từ file SQLite. |
| 72 | **JSON Config Audit**| Phân tích tệp JSON | APS Custom | Quét bí mật trong appsettings.json. |
| 73 | **XML Config Audit** | Phân tích tệp XML | APS Custom | Quét thông tin đăng nhập trong XML. |
| 74 | **Registry Key Audit**| Kiểm tra thanh ghi | APS Custom | Phân tích các khóa `Software\<App>`. |
| 75 | **Env Variable Leak**| Tìm bí mật trong .env | APS Custom | Quét các tệp ẩn chứa biến môi trường. |
| 76 | **Log File Audit** | Nhạy cảm trong tệp Nhật ký | APS Custom | Quét từ khóa 'password' trong .log. |
| 77 | **Temp File Audit** | Dữ liệu rác nhạy cảm | APS Custom | Kiểm tra các định danh trong %TEMP%. |
| 78 | **Browser Cache** | Rò rỉ qua WebView | APS Custom | Phân tích bộ nhớ Chromium cục bộ. |
| 79 | **Installer Script**| Lỗi từ bộ cài đặt | APS Custom | Phân tích script trong MSI/InnoSetup. |
| 80 | **Ransom Sim** | Giả lập mã hóa tệp | Weaponizer | **Thực thi PoC mã hóa kiểm soát.** |

### 🏰 Tầng 9: Windows Ecosystem Audit (STT 81-90)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 81 | APS-VEC-081 | `.ps1` (Giải mã) | **Giải mã cpassword GPP**. | Chạy Script PowerShell (Bypass) | Hiện mật khẩu AD dạng thô |
| 82 | APS-VEC-082 | `.txt` (Báo cáo) | Lỗi ủy quyền tên miền AD. | Đọc báo cáo lỗ hổng Domain | Chỉ ra tài khoản có quyền Delegated |
| 83 | APS-VEC-083 | `.txt` (Báo cáo) | Thu thập tài khoản dịch vụ SPN. | Đọc bảng danh sách SPN | Dữ liệu sẵn sàng cho Kerberoasting |
| 84 | APS-VEC-084 | `.c` (Trình điều khiển)| **Fuzzing Driver IOCTL**. | Biên dịch (.c) & Chạy file | Driver crash hoặc rò rỉ mem kernel |
| 85 | APS-VEC-085 | `.c` (COM) | Chiếm quyền giao diện COM. | Biên dịch (.c) & Chạy file | Thực thi mã qua COM hijacking |
| 86 | APS-VEC-086 | `.ps1` (Script) | Sửa đổi ACLs dịch vụ Windows. | Chạy Script PowerShell (Bypass) | Dịch vụ đích bị thay đổi quyền |
| 87 | APS-VEC-087 | `.c` (Pipe) | Khai thác Pipe nội bộ. | Biên dịch (.c) & Chạy file | Giao tiếp chéo tiến trình thành công |
| 88 | APS-VEC-088 | `.mof` / `.ps1` | Duy trì quyền qua WMI Event. | Chạy script đăng ký WMI | Mã độc tự chạy lại sau khi reboot |
| 89 | APS-VEC-089 | `.ps1` (Script) | Tự động leo thang qua Token. | Chạy Script PowerShell (Admin) | Chiếm quyền SYSTEM thông qua Token |
| 90 | APS-VEC-090 | `.c` (RPC) | Mô phỏng lỗ hổng điểm cuối RPC. | Biên dịch (.c) & Chạy file | RPC server thực thi lệnh trái phép |

### 🤖 Tầng 10: AI Intelligence & Weaponizer (STT 91-100)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 91 | APS-VEC-091 | `.json` / `.txt`| Chấm điểm rủi ro & đánh giá AI. | Đọc báo cáo xếp hạng rủi ro | Chỉ ra độ nguy hiểm của mục tiêu |
| 92 | APS-VEC-092 | `.c` (Mã nguồn) | **PoC đa khai thác Tier-3**. | Biên dịch (.c) & Chạy file | Khai thác đa tầng, tàng hình tuyệt đối |
| 93 | APS-VEC-093 | `.json` / `.txt`| Dự đoán AI về luồng hành vi độc. | Đọc phân tích đường đi của mã | Nhận diện chuỗi tấn công tiềm năng |
| 94 | APS-VEC-094 | `.txt` (Báo cáo) | Lỗi logic nghiệp vụ từ AI. | Đọc báo cáo lỗi nghiệp vụ | Chỉ ra lỗ hổng logic không mã hóa |
| 95 | APS-VEC-095 | `.json` / `.txt`| Nhận diện hành vi bất thường. | So sánh Log vs AI Baseline | Phát hiện sự lệch chuẩn an ninh |
| 96 | APS-VEC-096 | `.txt` (Báo cáo) | Phân tích độ ổn định mã khai thác. | Đọc bảng đánh giá độ tin cậy | Đảm bảo PoC không gây treo hệ thống |
| 97 | APS-VEC-097 | `.c` (Khai thác) | Bytecode tối ưu hóa kèm mã nhiễu. | Biên dịch (.c) & Chạy file | Binary vượt qua mọi mô hình Static AI |
| 98 | APS-VEC-098 | `.ps1` (Nạp mã) | **Dropper Tier-3 & Bypass AMSI**. | Chạy PS script (Vùng nhớ RAM) | Fileless thực thi, không tì vết |
| 99 | APS-VEC-099 | `.ps1` (Dọn dẹp) | Xóa dấu vết & nhật ký Log. | Chạy Script dọn dẹp sau tấn công | Xóa sạch dấu vết trong Event Viewer |
| 100| APS-VEC-100 | `.md` (Cảnh báo) | **Đối soát lỗ hổng CVE chi tiết**. | Đọc cảnh báo CVE Mapping | Kết nối trực tiếp với CVE-202X-... |

---

## 5. Quy trình Phân loại Rủi ro & Xác thực (Blueprint)
APS sử dụng mô hình **Liên kết Chiến lược (Strategic Correlation)**:
- **Xác thực Liên kết (Correlation Validation)**: Nếu Tầng 1 (ASLR TẮT) + Tầng 3 (Process Injection API), rủi ro được nâng lên mức **NGHIÊM TRỌNG (CRITICAL)**.
- **Trí tuệ Nhân tạo (AI Contextual Intel)**: AI đóng vai trò "Chiến lược gia" để liên kết các điểm yếu thành một chuỗi tấn công (Attack Chain) hoàn chỉnh.
- **Các mức độ Tin cậy**:
    - **XÁC THỰC CAO (HIGH/VERIFIED)**: Lỗ hổng đã được máy quét xác nhận thực tế.
    - **CẢNH BÁO (WARY)**: Cần chuyên gia kiểm tra lại logic nghiệp vụ.

---

## 6. Cẩm nang Pentest & Reverse Engineering

| Tầng tác chiến | Công cụ khuyên dùng | Kỹ thuật Khai thác |
| :--- | :--- | :--- |
| **Bảo vệ Binary** | `winchecksec`, `x64dbg` | Xây dựng chuỗi ROP bypass DEP/NX. |
| **DLL Hijacking** | `ProcMon`, `Dependencies` | Tìm "Ghost DLL" để chèn mã độc vào. |
| **IAT Audit** | `ScyllaHide`, `Ghidra` | Vượt qua Unhooking & API Hashing. |
| **Hệ sinh thái AD**| `BloodHound`, `certutil` | Leo thang qua GPP Password & Kerberoasting. |

---

## 7. Hướng dẫn Khai thác & Sử dụng Payload (PoC)

### 📊 Bảng tóm tắt phương thức triển khai Payload
| Loại Payload | Định dạng | Công cụ thực hiện | Kết quả Proof-of-Concept (PoC) |
| :--- | :--- | :--- | :--- |
| **Mã nguồn C** | `.c` | `x86_64-w64-mingw32-gcc` | Biên dịch thành `.dll` hoặc `.exe` để chạy. |
| **Script PowerShell**| `.ps1` | Windows PowerShell (Admin) | Thực thi bypass AMSI, nạp mã ngầm trong RAM. |
| **Cấu hình Registry**| `.reg` | `regedit.exe` | Tạo khóa duy trì quyền truy cập (Persistence). |
| **Ứng dụng XML** | `.xml` / `.manifest` | Trình soạn thảo XML | Ghi đè cấu hình nạp thư viện (Side-loading). |
| **Dữ liệu thô** | `.bin` / `.sdb` | `dd` / `sdbinst.exe` | Tiêm nội dung hoặc cài đặt Shims hệ thống. |

### 📁 Cách thực hiện Demo (Proof of Concept)
1. **Biên dịch**: Dùng `mingw-w64` để biên dịch file `.c` thành `.dll`. 
   - Lệnh mẫu: `x86_64-w64-mingw32-gcc -shared -o evil.dll evil.c`
2. **Triển khai**: Copy file `.dll` vào thư mục của ứng dụng thực tế.
3. **Kích hoạt**: Chạy ứng dụng. Nếu xuất hiện Popup "APS PoC" hoặc Calculator, lỗ hổng đã được xác nhận.

> [!TIP]
> **TÍNH NĂNG MỚI (AUTO-COMPILE)**: Bạn không cần phải tự biên dịch thủ công nữa! Engine Weaponizer v2.5 sẽ tự động dò tìm trình biên dịch (GCC/MinGW/Zig) và build file `.dll` cho bạn ngay sau khi quét xong. 

> [!IMPORTANT]
> **GHOST-PROTOCOL TIER-3 (ADVANCED STEALTH)**: Từ phiên bản v2.6, toàn bộ Payload C/DLL sẽ được bảo vệ bởi cơ chế **No-IAT**. File thực thi sẽ không chứa bất kỳ tên hàm Windows nào (như `system` hay `MessageBox`). Mọi liên kết sẽ được thực hiện động trong RAM lúc chạy thông qua thuật toán băm (API Hashing), mang lại tỷ lệ vượt qua AV cực cao.

---

## 8. Danh mục 100 Payloads (Payload Master List)

### 🏛️ Tầng 1: Bảo vệ Binary (STT 1-10)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | APS-VEC-001 | `.c` (Mã nguồn) | Demo khả năng rò rỉ địa chỉ ASLR. | Biên dịch (.c) & Chạy file | Hiện Popup địa chỉ nhớ rò rỉ |
| 2 | APS-VEC-002 | `.c` (Mã nguồn) | Demo xây dựng chuỗi ROP vượt DEP. | Biên dịch (.c) & Chạy file | Thực thi mã trong vùng non-exec |
| 3 | APS-VEC-003 | `.c` (Mã nguồn) | Kiểm tra bảo vệ ngăn xếp CET. | Biên dịch (.c) & Chạy file | Báo cáo vi phạm Shadow Stack |
| 4 | APS-VEC-004 | `.c` (Mã nguồn) | Thử nghiệm vượt Control Flow Guard. | Biên dịch (.c) & Chạy file | Gọi hàm ngoài danh sách CFG |
| 5 | APS-VEC-005 | `.c` (Mã nguồn) | Giả lập ghi đè trình xử lý SEH. | Biên dịch (.c) & Chạy file | Chiếm quyền điều khiển qua SEH |
| 6 | APS-VEC-006 | `.c` (Mã nguồn) | Thử nghiệm hỏng Stack GS Cookie. | Biên dịch (.c) & Chạy file | Báo cáo lỗi gác cổng Stack |
| 7 | APS-VEC-007 | `.c` (Mã nguồn) | Kiểm tra độ mạnh High Entropy ASLR. | Biên dịch (.c) & Chạy file | Phân tích phân bổ bộ nhớ 64-bit |
| 8 | APS-VEC-008 | `.c` (Mã nguồn) | Thẩm định tính độc lập vị trí nạp. | Biên dịch (.c) & Chạy file | Báo cáo tính toàn vẹn bản Reloc |
| 9 | APS-VEC-009 | `.c` (Mã nguồn) | Kiểm tra bảo vệ Return Flow Guard. | Biên dịch (.c) & Chạy file | Xác nhận RFG instrumentation |
| 10 | APS-VEC-010 | `.c` (Khai thác) | **UI Shatter**: Tiêm tin nhắn chéo. | Biên dịch (.c) & Chạy file | Tin nhắn xuất hiện cửa sổ khác |

### 📜 Tầng 2: Authenticode & Metadata (STT 11-20)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 11 | APS-VEC-011 | `.c` (Mã nguồn) | Demo giả mạo chữ ký Authenticode. | Biên dịch (.c) & Chạy file | OS báo tệp đã "được ký số" giả |
| 12 | APS-VEC-012 | `.c` (Khai thác) | **Khai thác lỗi tranh chấp TOCTOU**. | Biên dịch (.c) & Chạy file | Đổi nội dung tệp khi đang quét |
| 13 | APS-VEC-013 | `.c` / `.txt` | Sơ đồ rò rỉ Metadata .NET CLR. | Đọc file báo cáo sinh ra | Danh sách hàm/lớp rò rỉ |
| 14 | APS-VEC-014 | `.c` / `.txt` | Chỉ số cấu trúc PE Header lạ. | Đọc file báo cáo sinh ra | Bản đồ cấu trúc Header lỗi |
| 15 | APS-VEC-015 | `.c` / `.txt` | PoC hiệu chỉnh sai lệch Sections. | Biên dịch (.c) & Chạy file | Load sections vào vùng bất thường |
| 16 | APS-VEC-016 | `.c` / `.txt` | Rò rỉ thông tin từ thư mục Debug. | Đọc file báo cáo sinh ra | Đường dẫn PDB rò rỉ bí mật |
| 17 | APS-VEC-017 | `.txt` (Báo cáo) | **Symbolic Aid**: Khai thác tệp PDB. | Đọc file báo cáo sinh ra | Cấu trúc dữ liệu nội bộ bị lộ |
| 18 | APS-VEC-018 | `.txt` (Báo cáo) | Sơ đồ định danh qua Rich Header. | Đọc file báo cáo sinh ra | Nhận diện phiên bản compiler |
| 19 | APS-VEC-019 | `.xml` (Cấu hình) | Thử nghiệm thay đổi chữ ký Manifest. | Import file XML vào App | Token bảo mật bị ghi đè |
| 20 | APS-VEC-020 | `.txt` (Báo cáo) | Báo cáo trạng thái thu hồi chứng chỉ. | Đọc file báo cáo sinh ra | Danh sách CRL bị thu hồi |

### 💉 Tầng 3: API Anomaly & IAT Audit (STT 21-30)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 21 | APS-VEC-021 | `.c` (Khai thác) | Trình tiêm luồng Remote Thread. | Biên dịch (.c) & Chạy file | Mã độc tiêm sang process khác |
| 22 | APS-VEC-022 | `.c` (Ẩn mình) | Vượt qua các cơ chế gỡ lỗi. | Biên dịch (.c) & Chạy file | Debugger không bắt được tiến trình |
| 23 | APS-VEC-023 | `.c` (Né tránh) | Vượt qua môi trường máy ảo. | Biên dịch (.c) & Chạy file | Chạy bình thường trên VM |
| 24 | APS-VEC-024 | `.c` (Syscall) | **System Call trực tiếp (Halo's Gate)**. | Biên dịch (.c) & Chạy file | Vượt qua EDR Monitoring |
| 25 | APS-VEC-025 | `.c` (SMC) | **Giải mã mã nguồn khi đang chạy**. | Biên dịch (.c) & Chạy file | Mã tự giải mã thực thi Popup |
| 26 | APS-VEC-026 | `.c` (Nạp mã) | Khung nạp DLL trực tiếp từ RAM. | Biên dịch (.c) & Chạy file | DLL thực thi không qua disk |
| 27 | APS-VEC-027 | `.c` (Mạng) | Giả lập kết nối C2 qua mạng. | Biên dịch (.c) & Chạy file | Hiện log kết nối server kiểm thử |
| 28 | APS-VEC-028 | `.c` (IAT) | Làm nhiễu IAT bằng băm DJB2. | Biên dịch (.c) & Chạy file | IAT bị mã hóa, né tránh tĩnh |
| 29 | APS-VEC-029 | `.ps1` (Script) | Script thao tác quyền hệ thống tệp. | Chạy PowerShell (Bypass) | File hệ thống bị chiếm quyền |
| 30 | APS-VEC-030 | `.c` (Luồng) | Trình tiêm luồng ẩn qua ntdll. | Biên dịch (.c) & Chạy file | Tiêm mã không tạo luồng lộ liễu |

### 🏗️ Tầng 4: DLL Hijacking & Side-loading (STT 31-40)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 31 | APS-VEC-031 | `.c` (DLL) | DLL nạp vào thư mục ứng dụng. | Copy DLL vào folder App đích | Ứng dụng nạp DLL PoC |
| 32 | APS-VEC-032 | `.c` (DLL) | **Phantom DLL Hijacker**. | Copy DLL vào folder App đích | Bypass export checks |
| 33 | APS-VEC-033 | `.bat` / `.c` | Trình tạo Proxy DLL & Triển khai. | Chạy file .bat để tự cấu hình | Tự động chiếm quyền DLL gốc |
| 34 | APS-VEC-034 | `.c` (DLL) | Đoạn mã nạp DLL trễ. | Chạy App và đợi sự kiện nạp | DLL PoC chạy sau khi App nạp trễ |
| 35 | APS-VEC-035 | `.c` (Syscall) | Vượt cơ chế Safe Search Order. | Copy DLL vào vị trí nạp ưu tiên | Bypass Windows Search order |
| 36 | APS-VEC-036 | `.ps1` (Script) | Chiếm quyền qua biến %PATH%. | Chạy script sửa đổi Path | App chạy mã từ thư mục bị Shadow |
| 37 | APS-VEC-037 | `.xml` (Cấu hình) | XML Manifest độc hại cho Sxs. | Thay thế file .manifest của App | App nạp DLL từ đường dẫn giả |
| 38 | APS-VEC-038 | `.reg` / `.c` | Chiếm quyền COM qua Registry. | Import file .reg & Chạy App | App gọi COM rước mã độc vào |
| 39 | APS-VEC-039 | `.reg` (Cấu hình) | Duy trì quyền qua AppInit_DLLs. | Import file .reg | Mã độc tực động nạp vào mọi App |
| 40 | APS-VEC-040 | `.sdb` (DB) | Database vượt cơ chế App Shim. | Cài đặt SDB qua sdbinst | Mã độc chạy qua cơ chế tương thích |

### 🎭 Tầng 5: Resource & Manifest Audit (STT 41-50)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 41 | APS-VEC-041 | `.reg` / `.c` | PoC giả mạo UAC & Auto-elevate. | Import file .reg & Chạy App | App tự leo thang không hỏi UAC |
| 42 | APS-VEC-042 | `.manifest` | XML cấu hình yêu cầu UIAccess. | Thay thế .manifest của App | App chiếm quyền tương tác UI cao |
| 43 | APS-VEC-043 | `.reg` (Cấu hình) | Sửa Registry tin cậy cho Auto-Elevate. | Import file .reg | Vượt mặt cơ chế tin cậy nhị phân |
| 44 | APS-VEC-044 | `.bin` (Mã máy) | Shellcode trích xuất từ Overlay. | Chạy tệp nạp Shellcode | Shellcode thực thi (Hiện Calc/Popup) |
| 45 | APS-VEC-045 | `.ico` / `.txt` | Báo cáo giả mạo biểu tượng & binary. | Đọc báo cáo định danh Icon | Nhận diện kỹ thuật ngụy trang |
| 46 | APS-VEC-046 | `.c` (Trích xuất) | Kết xuất dữ liệu từ Resource section. | Biên dịch (.c) & Chạy file | Toàn bộ ảnh/config nhúng bị dump |
| 47 | APS-VEC-047 | `.txt` / `.json`| Chỉ số sai lệch thông tin phiên bản. | Đọc bảng so sánh Metadata | Phát hiện giả mạo thông tin tệp |
| 48 | APS-VEC-048 | `.xml` / `.txt`| Báo cáo lỗ hổng lược đồ XML. | Đọc phân tích cấu trúc XML | Chỉ ra điểm rò rỉ trong Manifest |
| 49 | APS-VEC-049 | `.txt` (Báo cáo) | Thất bại xác thực chữ ký Manifest. | Đọc nhật ký kiểm định chữ ký | Xác nhận Manifest không toàn vẹn |
| 50 | APS-VEC-050 | `.json` / `.txt`| Sơ đồ sai lệch tương thích hệ điều hành. | Đọc bản đồ GUID tương thích | Nhận diện mục tiêu OS bị giả mạo |

### 🌀 Tầng 6: Packer, Entropy & Anti-RE (STT 51-60)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 51 | APS-VEC-051 | `.c` (Bọc mã) | Trình bọc làm mờ độ hỗn loạn. | Biên dịch (.c) & Chạy file | Entropy file giảm, né tránh AI |
| 52 | APS-VEC-052 | `.c` (Bọc mã) | Ngụy trang chữ ký các bộ nén. | Biên dịch (.c) & Chạy file | Scanner nhận diện thành App sạch |
| 53 | APS-VEC-053 | `.c` (Né tránh) | Thực thi qua cơ chế TLS Callback. | Biên dịch (.c) & Chạy file | Mã độc chạy trước cả Entry Point |
| 54 | APS-VEC-054 | `.c` (Né tránh) | Nhiễu OEP & trình chạy JMP stub. | Biên dịch (.c) & Chạy file | Unpacker/Decompiler bị treo |
| 55 | APS-VEC-055 | `.c` (Né tránh) | PoC xóa Header chống trích xuất RAM. | Biên dịch (.c) & Chạy file | RAM dump không tìm thấy PE header |
| 56 | APS-VEC-056 | `.c` (Chuyển chế độ) | **Heaven's Gate (x86 sang x64)**. | Biên dịch (.c) & Chạy file | Né tránh x86 Debugger thành công |
| 57 | APS-VEC-057 | `.c` (Né tránh) | Cổng né Sandbox (chuột/uptime). | Biên dịch (.c) & Chạy file | Ngừng chạy nếu phát hiện Sandbox |
| 58 | APS-VEC-058 | `.c` (Thời gian) | **Phân tích độ trễ qua lệnh RDTSC**. | Biên dịch (.c) & Chạy file | Phát hiện bị gỡ lỗi qua timing |
| 59 | APS-VEC-059 | `.c` (Né tránh) | Logic mã hóa/giải mã chuỗi RAM. | Biên dịch (.c) & Chạy file | Strings không bị lộ khi quét tĩnh |
| 60 | APS-VEC-060 | `.c` (Né tránh) | Trình tạo mã rác làm nhiễu tập lệnh. | Biên dịch (.c) & Chạy file | Signatures tĩnh bị thay đổi liên tục |

### 🗝️ Tầng 7: Hardcoded Secrets & Crypto (STT 61-70)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 61 | APS-VEC-061 | `.json` / `.txt`| **Secret Harvester: AWS Access Keys**. | Đọc file báo cáo .json | Hiện AKIA... rò rỉ của mục tiêu |
| 62 | APS-VEC-062 | `.json` / `.txt`| Secret Harvester: Google API Keys. | Đọc file báo cáo .json | Hiện AIza... rò rỉ của mục tiêu |
| 63 | APS-VEC-063 | `.key` / `.txt` | **Trích xuất khóa riêng RSA**. | Mở file .key được dump | Toàn bộ Private Key bị lộ thô |
| 64 | APS-VEC-064 | `.json` / `.txt`| Mật khẩu và thông tin đăng nhập cứng. | Đọc file .txt | Danh sách Pass/User thô rò rỉ |
| 65 | APS-VEC-065 | `.txt` (Báo cáo) | Phân tích sử dụng băm yếu (MD5). | Đọc nhật ký kiểm tra Crypto | Chỉ ra hàm dùng MD5 không an toàn |
| 66 | APS-VEC-066 | `.c` (Mã nguồn) | Triển khai thuật toán mã hóa tự chế. | Biên dịch (.c) & Chạy file | Demo phá vỡ giải thuật tự chế |
| 67 | APS-VEC-067 | `.c` (Mã nguồn) | PoC rò rỉ IV của thuật toán AES. | Biên dịch (.c) & Chạy file | Giải mã tệp tin nhờ IV bị lộ |
| 68 | APS-VEC-068 | `.crt` / `.txt` | Trích xuất chứng chỉ số nhúng thô. | Mở tệp .crt được trích xuất | Chứng chỉ số của App bị dump |
| 69 | APS-VEC-069 | `.txt` (Báo cáo) | Thu thập các Token OAuth/JWT. | Đọc báo cáo trích xuất Token | Hiện Token có thể dùng Hijack |
| 70 | APS-VEC-070 | `.txt` (Báo cáo) | Danh sách rò rỉ Firebase DB URL. | Đọc tệp .txt | Hiện URL Firebase không bảo mật |

### 📂 Tầng 8: Local Storage & Data Privacy (STT 71-80)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 71 | APS-VEC-071 | `.sqlite` / `.txt`| **Trích xuất bảng dữ liệu SQLite App**. | Dùng công cụ đọc DB mở file | Toàn diện database cục bộ bị lộ |
| 72 | APS-VEC-072 | `.json` / `.txt`| Kết xuất tệp JSON cấu hình nhạy cảm. | Đọc tệp .json được dump | Lộ thông tin kết nối/environment |
| 73 | APS-VEC-073 | `.xml` / `.txt` | Rò rỉ credential trong tệp XML. | Đọc tệp .xml được dump | Lộ User/Pass trong file config |
| 74 | APS-VEC-074 | `.reg` / `.txt` | Thu thập bí mật từ Registry. | Mở file .reg hoặc .txt | Toàn bộ secrets trong Registry lộ |
| 75 | APS-VEC-075 | `.txt` (Báo cáo) | Rò rỉ qua biến môi trường. | Đọc tệp log rò rỉ ENV | Hiện giá trị các biến .env |
| 76 | APS-VEC-076 | `.log` / `.txt` | Dữ liệu nhạy cảm rò rỉ trong Nhật ký. | Quét tìm Keyword trong Log | Hiện các dòng Log chứa mật khẩu |
| 77 | APS-VEC-077 | `.txt` (Báo cáo) | Bí mật tàn dư trong %TEMP%. | Truy cập tệp trong thư mục Temp | Lấy được tệp cấu hình tạm rò rỉ |
| 78 | APS-VEC-078 | `.db` / `.json` | **Trích xuất Lịch sử & Cookies**. | Chạy script trích xuất Dump | Hiện lịch sử web & token đăng nhập |
| 79 | APS-VEC-079 | `.txt` (Báo cáo) | Lỗ hổng kịch bản trình cài đặt. | Đọc phân tích Installer script | Chỉ ra lỗi ghi đè tệp/leo thang |
| 80 | APS-VEC-080 | `.ps1` (Mô phỏng) | **Mô phỏng mã hóa Ransomware**. | Chạy Script PowerShell (Bypass) | Thử nghiệm mã hóa tệp (An toàn) |

### 🏰 Tầng 9: Windows Ecosystem Audit (STT 81-90)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 81 | APS-VEC-081 | `.ps1` (Giải mã) | **Giải mã cpassword GPP**. | Chạy Script PowerShell (Bypass) | Hiện mật khẩu AD dạng thô |
| 82 | APS-VEC-082 | `.txt` (Báo cáo) | Lỗi ủy quyền tên miền AD. | Đọc báo cáo lỗ hổng Domain | Chỉ ra tài khoản có quyền Delegated |
| 83 | APS-VEC-083 | `.txt` (Báo cáo) | Thu thập tài khoản dịch vụ SPN. | Đọc bảng danh sách SPN | Dữ liệu sẵn sàng cho Kerberoasting |
| 84 | APS-VEC-084 | `.c` (Trình điều khiển)| **Fuzzing Driver IOCTL**. | Biên dịch (.c) & Chạy file | Driver crash hoặc rò rỉ mem kernel |
| 85 | APS-VEC-085 | `.c` (COM) | Chiếm quyền giao diện COM. | Biên dịch (.c) & Chạy file | Thực thi mã qua COM hijacking |
| 86 | APS-VEC-086 | `.ps1` (Script) | Sửa đổi ACLs dịch vụ Windows. | Chạy Script PowerShell (Bypass) | Dịch vụ đích bị thay đổi quyền |
| 87 | APS-VEC-087 | `.c` (Pipe) | Khai thác Pipe nội bộ. | Biên dịch (.c) & Chạy file | Giao tiếp chéo tiến trình thành công |
| 88 | APS-VEC-088 | `.mof` / `.ps1` | Duy trì quyền qua WMI Event. | Chạy script đăng ký WMI | Mã độc tự chạy lại sau khi reboot |
| 89 | APS-VEC-089 | `.ps1` (Script) | Tự động leo thang qua Token. | Chạy Script PowerShell (Admin) | Chiếm quyền SYSTEM thông qua Token |
| 90 | APS-VEC-090 | `.c` (RPC) | Mô phỏng lỗ hổng điểm cuối RPC. | Biên dịch (.c) & Chạy file | RPC server thực thi lệnh trái phép |

### 🤖 Tầng 10: AI Intelligence & Weaponizer (STT 91-100)
| STT | Vector ID | Kiểu File | Hành vi Payload | **Cách thực hiện** | **Kỳ vọng** |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 91 | APS-VEC-091 | `.json` / `.txt`| Chấm điểm rủi ro & đánh giá AI. | Đọc báo cáo xếp hạng rủi ro | Chỉ ra độ nguy hiểm của mục tiêu |
| 92 | APS-VEC-092 | `.c` (Mã nguồn) | **PoC đa khai thác Tier-3**. | Biên dịch (.c) & Chạy file | Khai thác đa tầng, tàng hình tuyệt đối |
| 93 | APS-VEC-093 | `.json` / `.txt`| Dự đoán AI về luồng hành vi độc. | Đọc phân tích đường đi của mã | Nhận diện chuỗi tấn công tiềm năng |
| 94 | APS-VEC-094 | `.txt` (Báo cáo) | Lỗi logic nghiệp vụ từ AI. | Đọc báo cáo lỗi nghiệp vụ | Chỉ ra lỗ hổng logic không mã hóa |
| 95 | APS-VEC-095 | `.json` / `.txt`| Nhận diện hành vi bất thường. | So sánh Log vs AI Baseline | Phát hiện sự lệch chuẩn an ninh |
| 96 | APS-VEC-096 | `.txt` (Báo cáo) | Phân tích độ ổn định mã khai thác. | Đọc bảng đánh giá độ tin cậy | Đảm bảo PoC không gây treo hệ thống |
| 97 | APS-VEC-097 | `.c` (Khai thác) | Bytecode tối ưu hóa kèm mã nhiễu. | Biên dịch (.c) & Chạy file | Binary vượt qua mọi mô hình Static AI |
| 98 | APS-VEC-098 | `.ps1` (Nạp mã) | **Dropper Tier-3 & Bypass AMSI**. | Chạy PS script (Vùng nhớ RAM) | Fileless thực thi, không tì vết |
| 99 | APS-VEC-099 | `.ps1` (Dọn dẹp) | Xóa dấu vết & nhật ký Log. | Chạy Script dọn dẹp sau tấn công | Xóa sạch dấu vết trong Event Viewer |
| 100| APS-VEC-100 | `.md` (Cảnh báo) | **Đối soát lỗ hổng CVE chi tiết**. | Đọc cảnh báo CVE Mapping | Kết nối trực tiếp với CVE-202X-... |

---

### 🚀 Ghost-Protocol Tier-3 Payload Features
Mọi Payload `.c` sinh ra cho các Vector trọng yếu đều được tích hợp gói **Ghost-Protocol Tier-3** với các tính năng:
- **XOR Stack Strings**: Không chứa chuỗi ký tự thô nào trong mã nguồn.
- **PEB Module Walk**: Tự tìm hàm hệ thống trong bộ nhớ, không cần bảng nạp (IAT).
- **Direct Syscall (Halo's Gate)**: Thực thi trực tiếp qua System Call để tàng hình trước EDR.
- **RtlQueueWorkItem**: Chạy mã trong Thread Pool thay vì tạo luồng mới (Anti-monitoring).

---
*Chúc quý khách có một chiến dịch Pentest thành công và an toàn!*
*Tài liệu được cập nhật ngày: 19/04/2026 - Đội ngũ phát triển APS.*
