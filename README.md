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

## 🛠️ Hướng dẫn Sử dụng
Để vận hành hệ thống, quý khách vui lòng sử dụng lệnh sau trong terminal:

```bash
# Quét một file mục tiêu đơn lẻ
python3 main.py -t <path_to_pe_file>

# Quét hàng loạt trong một thư mục và kích hoạt AI thẩm định
python3 main.py -t <directory_path> --ai-analyze

# Quét và tự động sinh mã khai thác mẫu (PoC)
python3 main.py -t <path_to_pe_file> --pwn
```

## 📖 Tài liệu Kỹ thuật
Để tìm hiểu sâu hơn về 100 Vector kiểm thử và các kỹ thuật Pentest được áp dụng, quý khách vui lòng tham khảo:
👉 **[Tài liệu Kỹ thuật Hệ thống (TECH_SPECS.md)](TECH_SPECS.md)**

---
*Chúc quý khách có một chiến dịch Pentest thành công và an toàn!*
*Đội ngũ phát triển AUTOMATION PENTEST SYSTEM.*
