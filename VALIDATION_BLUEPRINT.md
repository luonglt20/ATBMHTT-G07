# 🎯 APS VALIDATION BLUEPRINT: Quyết định Độ chính xác & Ngữ cảnh

Tài liệu này giải thích quy trình tư duy và xác thực của hệ thống **AUTOMATION PENTEST SYSTEM (APS)** để đảm bảo mọi phát hiện rủi ro đều **chính xác về kỹ thuật** và **phù hợp về ngữ cảnh**.

## 1. Cơ chế Triage 10 Tầng (10-Layer Strategic Triage)
APS không đánh giá các lỗ hổng một cách rời rạc. Hệ thống sử dụng mô hình **Strategic Correlation** ở Layer 10:

*   **Xác thực Tương quan (Correlation Validation)**: Nếu Layer 1 phát hiện thiếu ASLR và Layer 3 phát hiện `VirtualAllocEx`, APS sẽ nâng mức độ rủi ro từ MED sang **CRITICAL**. Bởi vì việc thiếu cơ chế bảo vệ bộ nhớ khiến các API nhạy cảm trở nên cực kỳ nguy hiểm.
*   **Xác thực Nạp nạp (Reachability Analysis)**: Engine `AEVF Verifier` sẽ nạp file PE vào bộ nhớ đệm để kiểm tra bảng nạp (IAT). Một API được coi là rủi ro chỉ khi ứng dụng thực sự có lệnh gọi nạp API đó từ hệ điều hành.

## 2. Thẩm định AI theo Ngữ cảnh (Contextual AI Intel)
Mỗi báo cáo được xử lý bởi **Lead Exploit Strategist AI**, thực hiện các bước:
1.  **Attack Chain Synthesis**: AI sẽ đóng vai trò hacker chuyên nghiệp để liên kết các điểm yếu lại thành một kịch bản xâm nhập thực tế.
2.  **Business Risk Logic**: AI đánh giá xem rủi ro đó có ảnh hưởng đến nghiệp vụ hay không (ví dụ: rò rỉ Key ở ứng dụng tài chính quan trọng hơn nhiều so với ứng dụng tiện ích offline).
3.  **Remediation Prioritization**: Các khuyến nghị được sắp xếp theo mức độ ưu tiên từ "Vá ngay lập tức" đến "Cần theo dõi".

## 3. Loại bỏ Cảnh báo giả (False Positive Mitigation)
Hệ thống sử dụng các bộ lọc chuyên biệt để giảm thiểu nhiễu:
*   **Thư viện hệ thống**: APS tự động loại trừ các binary chuẩn của Windows khỏi quá trình báo cáo lỗi để tập trung vào mã nguồn của ứng dụng khách (Custom Code).
*   **Logic Reachability**: Nếu một đoạn mã nguy hiểm tồn tại nhưng không cách nào thực thi được (Dead Code), APS sẽ hạ cấp ưu tiên của lỗ hổng đó.

## 4. Cách sếp kiểm chứng (User Triage)
Dựa vào cột **Confidence** trong báo cáo:
*   **HIGH/VERIFIED**: Lỗ hổng đã được máy quét xác nhận sự tồn tại thực tế trong code. Sếp nên tập trung xử lý ngay.
*   **WARY/MEDIUM**: Có dấu hiệu rủi ro nhưng cần chuyên gia manual check thêm về logic nghiệp vụ.

---
*Mục tiêu của APS không phải là đưa ra nhiều lỗi nhất, mà là đưa ra những lỗi 'đắt' nhất.*
*Đội ngũ APS - Precision Security Engineering.*
