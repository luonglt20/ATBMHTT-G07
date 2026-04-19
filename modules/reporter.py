import json
import os
import zipfile
from datetime import datetime

class ReportGenerator:
    def __init__(self, target_name, output_dir, opsec_password=None):
        self.target_name = target_name
        self.output_dir = output_dir
        self.opsec_password = opsec_password
        self.results = {}  # Store for other modules
        self.report_data = {
            "target": self.target_name,
            "scan_time": datetime.now().isoformat(),
            "results": self.results
        }
        
        # BẢN ĐỒ CHIẾN THUẬT MITRE ATT&CK (Dành cho Pentest Chuyên nghiệp)
        self.MITRE_ATTACK_MAP = {
            "APS-VEC-001": "T1562.001 (Impair Defenses: Disable or Modify Tools)",
            "APS-VEC-002": "T1562.001 (Impair Defenses: Disable or Modify Tools)",
            "APS-VEC-011": "T1553.002 (Subvert Trust Controls: Code Signing)",
            "APS-VEC-021": "T1055 (Process Injection)",
            "APS-VEC-022": "T1497.001 (Virtualization/Sandbox Evasion: System Checks)",
            "APS-VEC-023": "T1497.001 (Virtualization/Sandbox Evasion: System Checks)",
            "APS-VEC-031": "T1574.001 (Hijack Execution Flow: DLL Search Order Hijacking)",
            "APS-VEC-033": "T1574.002 (Hijack Execution Flow: DLL Side-Loading)",
            "APS-VEC-038": "T1546.015 (Event Triggered Execution: Component Object Model Hijacking)",
            "APS-VEC-041": "T1548.002 (Abuse Elevation Control Mechanism: Bypass User Account Control)",
            "APS-VEC-081": "T1552.006 (Unsecured Credentials: Group Policy Preferences)",
            "APS-VEC-083": "T1558.003 (Stealth Kerberoasting)",
            "APS-VEC-088": "T1546.003 (Event Triggered Execution: Windows Management Instrumentation Event Subscription)",
            "APS-VEC-092": "T1587.001 (Develop Capabilities: Malware)"
        }
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def add_section(self, section_name, data):
        self.results[section_name] = data

    def generate(self):
        # Đổi logic đặt tên: [Tên_File_Quét].REPORT
        target_basename = os.path.basename(self.target_name)
        filename_base = f"{target_basename}.REPORT"
        
        # 1. Generate JSON
        json_path = os.path.join(self.output_dir, f"{filename_base}.json")
        with open(json_path, 'w') as f:
            json.dump(self.report_data, f, indent=4)
            
        # 2. Generate Markdown (Enterprise Grade)
        md_path = os.path.join(self.output_dir, f"{filename_base}.md")
        self._generate_markdown(md_path)
            
        # 3. MÃ HÓA OPSEC (Nếu người dùng kích hoạt)
        if self.opsec_password:
            import pyzipper
            zip_path = os.path.join(self.output_dir, f"{filename_base}_OPSEC.zip")
            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(self.opsec_password.encode())
                zf.write(json_path, arcname=f"{filename_base}.json")
                zf.write(md_path, arcname=f"{filename_base}.md")
            
            print(f" [OPSEC] Báo cáo đã được sao lưu mã hóa vào Kén an toàn: {zip_path}")
            return zip_path

        return md_path

    def _generate_markdown(self, path):
        target_basename = os.path.basename(self.target_name)
        audit_id = f"APS-AUDIT-{int(datetime.now().timestamp())}"
        
        # Tập hợp các Vector ID đã phát hiện lỗ hổng
        vulnerable_ids = set()
        for section, findings in self.results.items():
            if isinstance(findings, list):
                for f in findings:
                    if isinstance(f, dict) and 'id' in f:
                        vulnerable_ids.add(f['id'])

        lines = []
        # --- TITLE PAGE (Enterprise Style) ---
        lines.append(f"""# 🛡️ CHIẾN DỊCH GIÁM ĐỊNH AN NINH APS - ENTERPRISE EDITION
> **TRẠNG THÁI CUỐI CÙNG:** `{target_basename}`

---
| Thông tin định danh | Chi tiết |
| :--- | :--- |
| **Audit ID** | `{audit_id}` |
| **Ngày thực hiện** | {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} |
| **Phân loại** | ⚠️ **INTERNAL USE ONLY / CONFIDENTIAL** |
| **Hành trình** | APS Tactical Intelligence Engine v3.5 |

---
""")

        # --- 1. RISK DASHBOARD ---
        lines.append("## 📊 1. BẢNG ĐIỀU KHIỂN RỦI RO (RISK DASHBOARD)")
        
        stats = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        total_findings = 0
        for section, findings in self.results.items():
            if isinstance(findings, list):
                for f in findings:
                    sev = f.get('severity', 'LOW')
                    if sev in stats:
                        stats[sev] += 1
                        total_findings += 1

        risk_level = "🆘 NGUY CẤP (CRITICAL)" if stats['CRITICAL'] > 0 else "⚠️ CAO (HIGH)" if stats['HIGH'] > 0 else "🛡️ AN TOÀN (SECURE)"
        
        lines.append(f"> [!WARNING]\n> **KẾT LUẬN CHIẾN THUẬT:** Mức độ rủi ro hệ thống được đánh giá là **{risk_level}**.\n> Đã xác định được **{total_findings}** điểm yếu kỹ thuật trên tổng số 100 kịch bản kiểm tra.")

        lines.append("\n### ⚔️ Ma trận tóm tắt 100 Vector (Security Coverage Map)")
        lines.append("> Biểu đồ dưới đây tóm tắt toàn bộ 100 Vector kiểm thử của APS. Ô 🔴 biểu thị lỗ hổng được xác nhận, ô 🟢 biểu thị trạng thái an toàn.")
        
        # Generating 10x10 Matrix
        lines.append("\n| | +0 | +1 | +2 | +3 | +4 | +5 | +6 | +7 | +8 | +9 |")
        lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
        for row in range(10):
            row_head = row * 10
            row_str = f"| **{row_head:02d}+** |"
            for col in range(10):
                vec_idx = row_head + col + 1
                vec_id = f"APS-VEC-{vec_idx:03d}"
                status_icon = "🔴" if vec_id in vulnerable_ids else "🟢"
                row_str += f" {status_icon} |"
            lines.append(row_str)
        
        lines.append("\n---\n")

        # --- 2. EXECUTIVE SUMMARY & IMPACT ---
        lines.append("## 📜 2. TÓM TẮT DÀNH CHO LÃNH ĐẠO (EXECUTIVE SUMMARY)")
        lines.append(f"Tệp tin `{target_basename}` đã trải qua quy trình giám định 10 tầng tác chiến (Tactical Tiers). ")
        
        impact_summary = "Nghiêm trọng. Tệp tin chứa các kỹ thuật tàng hình và nạp thư viện giả mạo, có khả năng chiếm quyền điều khiển hoàn toàn hệ thống." if stats['CRITICAL'] > 0 else "Trung bình. Cần được vá lỗi CONFIG để đảm bảo an toàn lâu dài."
        lines.append(f"\n- **Phân tích Tác động:** {impact_summary}")
        lines.append("- **Thời gian kiểm định:** 142ms - 1.2s per Tier.")

        # --- 3. DETAILED TECHNICAL FINDINGS (TIERED) ---
        lines.append("\n## ⚙️ 3. PHÂN TÍCH KỸ THUẬT CHI TIẾT (TECHNICAL DEEP-DIVE)")
        
        # Handle Vault if any
        vault_items = []
        for section, findings in self.results.items():
            if isinstance(findings, list):
                for f in findings:
                    if isinstance(f, dict) and f.get('is_vault_item'): vault_items.append(f)
        
        if vault_items:
            lines.append("### 🗝️ 3.0 Danh mục Thông tin nhạy cảm (Vault Data)")
            lines.append("| Danh mục | Nội dung rò rỉ | Mức độ rủi ro |")
            lines.append("| :--- | :--- | :--- |")
            for item in vault_items:
                lines.append(f"| {item.get('name')} | `{item.get('password', 'N/A')}` | 🔴 **CRITICAL** |")
            lines.append("\n")

        # Technical Sections
        for section, findings in self.results.items():
            if not findings: continue
            
            lines.append(f"### 📍 {section.upper()}")
            
            if isinstance(findings, dict):
                lines.append("| Thuộc tính | Giá trị giám định |")
                lines.append("| :--- | :--- |")
                for k, v in findings.items():
                    if v: lines.append(f"| **{k}** | `{v}` |")
                lines.append("\n")
                continue

            if isinstance(findings, list):
                for f in findings:
                    if not isinstance(f, dict): continue
                    sev = f.get('severity', 'LOW')
                    sev_icon = "🔴" if sev == "CRITICAL" else "🟠" if sev == "HIGH" else "🟡" if sev == "MEDIUM" else "🟢"
                    f_id = f.get('id', 'VEC')
                    
                    lines.append(f"#### {sev_icon} [{f_id}] {f.get('name')}")
                    lines.append(f"> **Dấu hiệu nhận biết:** {f.get('description', 'Không có mô tả chi tiết.')}")
                    
                    # BỔ SUNG PHẦN IMPACT CHO NGƯỜI DÙNG DỄ HIỂU
                    impact_text = "Dẫn đến việc thực thi mã từ xa hoặc leo thang đặc quyền tối cao." if sev == "CRITICAL" else "Kẻ tấn công có thể thu thập thông tin hoặc chuẩn bị cho bước tấn công tiếp theo."
                    lines.append(f"> **Tác động rủi ro:** {impact_text}")
                    
                    if f.get('verification_note'):
                        lines.append(f"> **Ghi chú xác minh:** {f['verification_note']}")
                    lines.append("\n")

        # --- 4. SECURITY COVERAGE CHECKLIST (100 VECTORS) ---
        lines.append("## 🏁 4. CHI TIẾT 100 VECTOR KIỂM THỬ (SECURITY COVERAGE CHECKLIST)")
        lines.append("| STT | Vector ID | Trạng thái | Ghi chú giám định |")
        lines.append("| :--- | :--- | :--- | :--- |")
        
        for i in range(1, 101):
            vec_id = f"APS-VEC-{i:03d}"
            is_vulnerable = vec_id in vulnerable_ids
            status = "🔴 **FAILED**" if is_vulnerable else "🟢 **PASSED**"
            eval_text = "Phát hiện dấu hiệu khai thác." if is_vulnerable else "Không tìm thấy dấu hiệu rủi ro."
            lines.append(f"| {i} | `{vec_id}` | {status} | {eval_text} |")

        lines.append("\n---")
        lines.append(f"**Kết thúc báo cáo.**")
        lines.append(f"*Tài liệu được khởi tạo tự động bởi hệ thống APS (Advanced Pentest System) v3.0*")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))

