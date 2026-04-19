import os
import json
import urllib.request
from colorama import Fore, Style

class AIAnalyzer:
    def __init__(self, report_data, api_key=""):
        self.report_data = report_data
        # Ưu tiên lấy api_key từ tham số, nếu không có lấy từ biến môi trường
        self.api_key = api_key if api_key else os.environ.get("GROQ_API_KEY")

    def run(self):
        print(f"\n{Fore.BLUE}[+] PHASE 4: AI/LLM REVERSING ANALYSIS (Vector 20){Style.RESET_ALL}")
        if not self.api_key:
            print(f" {Fore.YELLOW}[!] Bỏ qua Phân tích AI vì không tìm thấy Groq API Key.{Style.RESET_ALL}")
            print(f" {Fore.LIGHTBLACK_EX}[INFO] Hãy thiết lập `export GROQ_API_KEY=gsk_...` hoặc nhập vào giao diện web.{Style.RESET_ALL}")
            return [{
                "id": "AI-INFO",
                "name": "AI Analysis Skipped",
                "severity": "INFO",
                "details": "Hãy cung cấp Groq API Key (gsk_...) để AI chạy đọc hiểu Report."
            }]

        print(f" {Fore.GREEN}[-] Đang gửi dữ liệu thô lên Máy chủ LLM để dịch ngược logic...{Style.RESET_ALL}")
        
        prompt = (
            "Bạn là một 'Lead Red Team Operator' chuyên gia về Windows PE Internals. "
            "Nhiệm vụ của bạn là phân tích dữ liệu Pentest dưới đây để thiết lập một 'Kill Chain' (Chuỗi hạ gục) hoàn chỉnh. "
            "Hãy xâu chuỗi các điểm yếu rời rạc (như Missing ASLR + Sensitive APIs + Writable Directory) thành một kịch bản xâm nhập chiếm quyền SYSTEM.\n\n"
            "Yêu cầu:\n"
            "1. XÁC ĐỊNH MỤC TIÊU ƯU TIÊN (High-Value Target Identification).\n"
            "2. THIẾT LẬP CHUỖI TẤN CÔNG (Exploit Chain: Recon -> Access -> Persistence -> LPE).\n"
            "3. ĐỀ XUẤT CÁC KỸ THUẬT BYPASS (EDR/AV Evasion like Indirect Syscalls, DLL Proxying).\n"
            "4. ĐÁNH GIÁ TỔNG QUAN VỀ KHẢ NĂNG BỊ 'PWNED' CỦA ỨNG DỤNG.\n\n"
            "KẾT QUẢ PENTEST RAW:\n"
            f"{json.dumps(self.report_data)[:4000]}"
        )

        data = json.dumps({
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }).encode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
                ai_response = result['choices'][0]['message']['content']
                print(f" {Fore.GREEN}[OK] Groq AI Đã Trả Lời: {ai_response[:100]}...{Style.RESET_ALL}")
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
