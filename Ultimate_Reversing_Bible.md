# 📖 AUTOMATION PENTEST SYSTEM: THE ULTIMATE REVERSING & EXPLOITATION BIBLE 📖

Tài liệu này là "Bản đồ tác chiến" (War Map) cho chuyên gia Pentest. Nó đồng bộ 100 Vector tấn công vào **10 Tầng Chiến Lược** của hệ thống AUTOMATION PENTEST SYSTEM (APS), đi kèm các công cụ tiêu chuẩn ngành và kỹ thuật khai thác thực tế.

---

## 🏛️ Tầng 1: Binary Hardening (Phòng thủ Nhị phân)
*Mục tiêu: Đánh giá khả năng chống khai thác mức thấp của tệp thực thi.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **ASLR (Randomization)** | winchecksec | `binary_protections.py` | Rò rỉ địa chỉ qua lỗi Memory Leak -> Tính Base Address -> Bypass. |
| 2 | **DEP/NX (Non-Exec)** | DIE-cli | `binary_protections.py` | Xây dựng chuỗi ROP (Return Oriented Programming) để thực thi shellcode. |
| 3 | **Intel CET (Hardware)** | Intel Inspector | `binary_protections.py` | Shadow Stack protection. Yêu cầu kỹ thuật JOP/COP bypass cao cấp. |
| 4 | **Control Flow Guard** | `dumpbin /loadconfig` | `binary_protections.py` | Khai thác các lần gọi hàm gián tiếp không nằm trong bitmap bảo vệ. |
| 5 | **SafeSEH / SEHOP** | CFF Explorer | `binary_protections.py` | Ghi đè cấu trúc Exception Handler để chiếm quyền điều khiển luồng. |

---

## 📜 Tầng 2: Authenticode & Metadata (Nhận diện & Xác thực)
*Mục tiêu: Xác minh nguồn gốc và tính toàn vẹn của ứng dụng.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 11 | **Digital Signature** | Sigcheck | `binary_protections.py` | Spoofing certificate hoặc khai thác lỗi trong quá trình verify chữ ký. |
| 12 | **PDB Symbol Paths** | `dumpbin /pdb` | `binary_protections.py` | Thu thập thông tin về cấu trúc thư mục phát triển và tên hàm nội bộ. |
| 13 | **CLR Metadata (.NET)** | dnSpy | `main.py` | Decompile ngược về C# để tìm kiếm logic bypass trong các hàm Native. |

---

## 💉 Tầng 3: API Anomaly & IAT Audit (Bất thường Hệ thống)
*Mục tiêu: Phát hiện hành vi mã độc và các phương thức tiêm kích.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 21 | **Process Injection** | x64dbg | `api_scanner.py` | Theo dõi `VirtualAllocEx` + `WriteProcessMemory` để tìm code injection. |
| 22 | **Anti-Debug APIs** | ScyllaHide | `api_scanner.py` | Bypass `IsDebuggerPresent` để phân tích ứng dụng trong môi trường debug. |
| 23 | **Reg Tampering** | ProcMon | `api_scanner.py` | Phát hiện các API can thiệp vào Registry để thiết lập Persistence. |

---

## 🏗️ Tầng 4: DLL Hijacking & Side-loading (Leo thang đặc quyền)
*Mục tiêu: Chiếm quyền điều khiển luồng nạp thư viện của Windows.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 31 | **Weak Search Order** | ProcMon | `dll_hijack.py` | Chèn DLL trùng tên vào thư mục ứng dụng để được load trước DLL hệ thống. |
| 32 | **Ghost DLL Loading** | Dependencies | `dll_hijack.py` | Tìm kiếm các DLL bị thiếu (Missing) mà ứng dụng vẫn cố gắng nạp. |

---

## 🎭 Tầng 5: Resource & Manifest (Quyền hạn & Tài nguyên)
*Mục tiêu: Đánh giá đặc quyền UAC và các tài nguyên đính kèm.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 41 | **UAC Auto-Elevate** | Sigcheck | `windows_manifest.py` | Tìm các binary được tin tưởng bởi OS để thực hiện UAC Bypass. |
| 42 | **Resource Carving** | Resource Hacker | `windows_manifest.py` | Trích xuất các tệp tin cấu hình nhạy cảm được nhúng trong Resource Section. |

---

## 🌀 Tầng 6: Packer, Entropy & Anti-RE (Chống đảo ngược)
*Mục tiêu: Vượt qua các lớp vỏ bọc và cơ chế bảo vệ mã nguồn.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 51 | **High Entropy Sec** | DIE | `packer_detector.py` | Nhận diện dữ liệu bị nén/mã hóa. Thường chứa payload thật của malware. |
| 52 | **Known Packer Sign** | PEid | `packer_detector.py` | Tự động unpacking các lớp vỏ phổ thông như UPX, ASPack. |

---

## 🗝️ Tầng 7: Hardcoded Secrets & Crypto (Rò rỉ Thông tin)
*Mục tiêu: Khai thác các dữ liệu nhạy cảm bị ghi cứng trong mã.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 61 | **API Key Mining** | TruffleHog | `crypto_scanner.py` | Thu hoạch AWS, Google API keys để tấn công vào hạ tầng Cloud. |
| 62 | **Weak Crypto Const** | Signsrch | `crypto_scanner.py` | Nhận diện các hằng số mã hóa yếu (MD5, SHA1) để thực hiện tấn công va chạm. |

---

## 📂 Tầng 8: Local Storage & Data Privacy (Pháp y Dữ liệu)
*Mục tiêu: Chiếm đoạt dữ liệu người dùng được lưu trữ cục bộ.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 71 | **SQLite DB Audit** | DB Browser | `local_storage.py` | Trích xuất bảng `Users`, `Sessions` để chiếm quyền tài khoản. |
| 72 | **Config File Leak** | Notepad++ | `local_storage.py` | Tìm kiếm mật khẩu Cleartext trong các file `.env`, `.xml`, `.json`. |

---

## 🏰 Tầng 9: Windows Ecosystem (AD & Kernel)
*Mục tiêu: Tấn công leo thang vào hạ tầng Domain và Nhân hệ điều hành.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 81 | **GPP Password Leak** | SYSVOL Crawler | `ad_scanner.py` | Giải mã mật khẩu Admin từ file `Groups.xml` trong Active Directory. |
| 82 | **IOCTL Fuzzing** | IrpTracker | `driver_scanner.py` | Gửi gói tin rác vào Driver để gây sập hệ thống hoặc chiếm quyền Kernel. |

---

## 🤖 Tầng 10: AI Intelligence & Weaponizer (Trí tuệ Nhân tạo)
*Mục tiêu: Thẩm định nâng cao và tự động hóa mã khai thác.*

| STT | Vector | Công cụ Pro | Module APS | Kỹ thuật Khai thác |
| :--- | :--- | :--- | :--- | :--- |
| 91 | **AI Risk Scoring** | Gemini 1.5 Pro | `ai_analyzer.py` | Sử dụng LLM để dự đoán các lỗi logic nghiệp vụ mà tool tĩnh không thấy. |
| 92 | **Auto PoC Gen** | Metasploit | `weaponizer.py` | Tự động sinh mã khai thác (Exploit) dựa trên các lỗ hổng đã xác thực. |

---
*Tài liệu này được bảo mật và biên soạn bởi Đội ngũ AUTOMATION PENTEST SYSTEM.*
