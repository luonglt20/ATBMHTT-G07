# 🛠️ AUTOMATION PENTEST SYSTEM - TECHNICAL SPECIFICATIONS

Hệ thống này được thiết kế để cung cấp quy trình đánh giá an ninh tự động chuyên sâu cho các tệp tin thực thi (PE Files). Dưới đây là bảng mô tả chi tiết 10 Tầng Tác Chiến với 100 Vector kiểm thử tiêu chuẩn.

## 📊 Bảng Danh mục 100 Vectors (10 Tầng Chiến Lược)

| Tầng (Layer) | Tên Vector | Mục đích | Tools sử dụng | Models / Logic | Kỹ thuật Pentest |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1: Hardening** | Mitigations Audit | Kiểm tra cơ chế bảo vệ mã nguồn | `pefile`, `BinaryProtectionScanner` | Heuristic Analysis | Phân tích DLL Characteristics (ASLR, DEP, CFG, CET) |
| **2: Authenticode** | Digital Signature | Xác thực tính toàn vẹn và nguồn gốc | `pefile`, `Win32 Trust API` | Certificate Chain Validation | Phân tích Security Directory & Root CA trust |
| **3: API Anomaly** | IAT Behavioral Audit | Phát hiện hành vi mã độc/tiêm kích | `APIScanner` | Behavioral Mapping | Phân tích bảng Import (IAT) tìm các API nhạy cảm |
| **4: Persistence** | DLL Hijacking | Phát hiện lỗ hổng leo thang đặc quyền | `DLLHijackingScanner` | Path Search Order Logic | Phân tích IAT & Directory ACLs để tìm điểm chèn DLL |
| **5: Privileges** | UAC & Manifest | Kiểm tra quyền hạn thực thi ứng dụng | `WindowsServicesManifestScanner` | XML Security Schema | Phân tích Manifest XML tìm quyền `requireAdministrator` |
| **6: Anti-Forensic** | Entropy & Packers | Phát hiện che giấu mã và nén dữ liệu | `PackerDetector` | Shannon Entropy Calculation | Đo độ hỗn loạn dữ liệu và nhận diện chữ ký Packer (UPX, VMP) |
| **7: Info Leak** | Hardcoded Secrets | Tìm rò rỉ API Keys, Passwords, Credentials | `CryptoScanner` | Regex Mining & String Analysis | Quét các chuỗi nhạy cảm (Pattern matching) công khai |
| **8: Data Privacy** | Local Storage / DB | Đánh giá an toàn dữ liệu người dùng | `LocalStorageScanner` | SQLite/Config Audit Engine | Phân tích các file DB, JSON, XML tại thư mục cài đặt |
| **9: Ecosystem** | AD & Kernel Audit | Tấn công hạ tầng Domain & Hệ thống | `ADScanner`, `DriverScanner` | Active Directory Intelligence | Kiểm tra AD Delegation & Lỗ hổng tương tác Kernel Driver |
| **10: AI Insight** | AEVF & Weaponizer | Thẩm định rủi ro và tự động hóa PoC | `AIAnalyzer`, `Weaponizer` | Gemini 1.5 Pro / GPT-4 | Phân tích tổng hợp AI & Sinh mã khai thác mẫu (PoC) |

## 📐 Danh mục Chi tiết 100 Vectors
Để xem danh sách đầy đủ và chi tiết kỹ thuật của toàn bộ 100 Vector kiểm thử, quý khách vui lòng truy cập:
👉 **[DANH SÁCH CHI TIẾT 100 VECTORS (VECTORS_100_MASTER_LIST.md)](VECTORS_100_MASTER_LIST.md)**

## ⚙️ Nguyên lý Vận hành
Hệ thống sử dụng phương pháp **Static Bit-level Analysis** kết hợp với **Contextual Intelligence** để đưa ra các nhận định chính xác mà không cần thực thi mã độc trong môi trường thật (Black-box approach).

---
*Tài liệu này thuộc về AUTOMATION PENTEST SYSTEM - Professional Edition*
