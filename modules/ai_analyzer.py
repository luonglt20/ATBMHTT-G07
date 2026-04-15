import os
import json
import urllib.request
from colorama import Fore, Style

class AIAnalyzer:
    def __init__(self, report_data):
        self.report_data = report_data
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def run(self):
        print(f"\n{Fore.BLUE}[+] PHASE 4: AI/LLM REVERSING ANALYSIS (Vector 20){Style.RESET_ALL}")
        if not self.api_key:
            print(f" {Fore.YELLOW}[!] Bỏ qua Phân tích AI vì không tìm thấy biến môi trường OPENAI_API_KEY.{Style.RESET_ALL}")
            print(f" {Fore.LIGHTBLACK_EX}[INFO] Hãy thiết lập `export OPENAI_API_KEY=sk-...` để AI tự động đọc hiểu Report.{Style.RESET_ALL}")
            return [{
                "id": "AI-INFO",
                "name": "AI Analysis Skipped",
                "severity": "INFO",
                "details": "Hãy thiết lập `export OPENAI_API_KEY=sk-...` để AI tự động đọc hiểu Report."
            }]

        print(f" {Fore.GREEN}[-] Đang gửi dữ liệu thô lên Máy chủ LLM để dịch ngược logic...{Style.RESET_ALL}")
        
        prompt = (
            "Bạn là một 'Lead Exploit Strategist' chuyên gia về Windows PE Internals. "
            "Nhiệm vụ của bạn là phân tích dữ liệu Pentest dưới đây để tìm ra 'Chuỗi tấn công' (Attack Chains) khả thi nhất. "
            "Hãy kết nối các lỗ hổng rời rạc (ví dụ: Thiếu ASLR/DEP + Dangerous APIs + DLL Hijacking) thành một kịch bản xâm nhập hoàn chỉnh.\n\n"
            "Yêu cầu:\n"
            "1. Xác định rủi ro kinh doanh cốt lõi (Core Business Risk).\n"
            "2. Phân tích sự kết hợp giữa các tầng (Layer Correlation).\n"
            "3. Gợi ý kỹ thuật khai thác nâng cao (angr, Frida, WinDbg script).\n"
            "4. Đưa ra khuyến nghị khắc phục theo thứ tự ưu tiên chiến lược.\n\n"
            "KẾT QUẢ PENTEST RAW:\n"
            f"{json.dumps(self.report_data)[:4000]}"
        )

        data = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }).encode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                ai_response = result['choices'][0]['message']['content']
                print(f" {Fore.GREEN}[OK] AI Đã Trả Lời: {ai_response[:100]}...{Style.RESET_ALL}")
                return [{
                    "id": "AI-SUMMARY",
                    "name": "AI Executive Summary",
                    "severity": "INFO",
                    "details": ai_response
                }]
        except Exception as e:
            print(f" {Fore.RED}[!] Lỗi khi gọi AI API: {e}{Style.RESET_ALL}")
            return [{
                "id": "AI-ERROR",
                "name": "AI Analysis Error",
                "severity": "MEDIUM",
                "details": f"Lỗi khi gọi AI API: {str(e)}"
            }]
