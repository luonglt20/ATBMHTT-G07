import os
import subprocess
import json
import time
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS
from modules.engine import APSEngine

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

engine = APSEngine()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
PAYLOAD_DIR = os.path.join(BASE_DIR, "Payload")

# Ensure dirs exist
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(PAYLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.json
    path = data.get('path')
    ai = data.get('ai', False)
    pwn = data.get('pwn', False)
    groq_key = data.get('groqKey', '')
    
    if not path or not os.path.exists(path):
        return jsonify({"error": "Đường dẫn không tồn tại"}), 400

    def generate():
        try:
            # 1. Tìm danh sách mục tiêu
            if os.path.isdir(path):
                targets = []
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(('.exe', '.dll', '.sys')):
                            targets.append(os.path.join(root, file))
            else:
                targets = [path]
            
            total = len(targets)
            yield f"data: {json.dumps({'event': 'start', 'total': total})}\n\n"
            
            for i, target in enumerate(targets):
                yield f"data: {json.dumps({'event': 'file_start', 'target': os.path.basename(target), 'index': i+1})}\n\n"
                
                # Thực hiện quét file này
                try:
                    res = engine.scan_file(target, output_dir=REPORT_DIR, ai_analyze=ai, pwn=pwn, groq_key=groq_key)
                    yield f"data: {json.dumps({'event': 'file_result', 'result': res, 'index': i+1})}\n\n"
                except Exception as file_err:
                    yield f"data: {json.dumps({'event': 'file_error', 'target': target, 'error': str(file_err)})}\n\n"
                
                # Nghỉ một chút để frontend kịp xử lý (optional)
                time.sleep(0.1)
                
            yield f"data: {json.dumps({'event': 'finish'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'event': 'error', 'error': str(e)})}\n\n"

    response = Response(stream_with_context(generate()), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    response.headers['Connection'] = 'keep-alive'
    return response

@app.route('/api/reports')
def list_reports():
    files = []
    if os.path.exists(REPORT_DIR):
        for f in os.listdir(REPORT_DIR):
            if f.endswith('.md'):
                stats = os.stat(os.path.join(REPORT_DIR, f))
                files.append({
                    "name": f,
                    "time": stats.st_mtime,
                    "size": stats.st_size
                })
    return jsonify(sorted(files, key=lambda x: x['time'], reverse=True))

@app.route('/api/payloads')
def list_payloads():
    payload_tree = []
    if os.path.exists(PAYLOAD_DIR):
        for target_folder in os.listdir(PAYLOAD_DIR):
            folder_path = os.path.join(PAYLOAD_DIR, target_folder)
            if os.path.isdir(folder_path):
                files = os.listdir(folder_path)
                payload_tree.append({
                    "target": target_folder,
                    "files": files
                })
    return jsonify(payload_tree)
    
@app.route('/api/browse-native', methods=['GET'])
def browse_native():
    mode = request.args.get('mode', 'folder')
    try:
        # Lệnh AppleScript trực tiếp, an toàn hơn và luôn hiện lên trên cùng
        if mode == 'file':
            ascript = 'choose file with prompt "Chọn tệp mục tiêu Pentest"'
        else:
            ascript = 'choose folder with prompt "Chọn thư mục mục tiêu Pentest"'
            
        # Sử dụng lệnh lồng nhau để đảm bảo hộp thoại được kích hoạt ngay lập tức
        cmd = f"osascript -e 'tell application \"Finder\"' -e 'activate' -e 'POSIX path of ({ascript})' -e 'end tell'"
        
        # Thêm timeout 60 giây để tránh treo hệ thống nếu người dùng không tương tác
        result = subprocess.check_output(cmd, shell=True, text=True, timeout=60).strip()
        return jsonify({"path": result if result else None})
    except subprocess.TimeoutExpired:
        log("  [!] Hộp thoại chọn file bị quá hạn (Timeout).", Fore.YELLOW)
        return jsonify({"path": None, "error": "Quá thời gian chọn file"})
    except subprocess.CalledProcessError:
        # Người dùng nhấn Cancel
        return jsonify({"path": None})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reports/<path:filename>')
def serve_report(filename):
    return send_from_directory(REPORT_DIR, filename)

if __name__ == '__main__':
    print(f"[*] APS Dashboard starting on http://localhost:5050")
    app.run(host='0.0.0.0', port=5050, debug=True)
