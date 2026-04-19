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
                for root_dir, _, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(('.exe', '.dll', '.sys')):
                            targets.append(os.path.join(root_dir, file))
            else:
                targets = [path]
            
            total = len(targets)
            yield f"data: {json.dumps({'status': 'start', 'total': total})}\n\n"
            
            from modules.weaponizer import Weaponizer
            
            for i, target in enumerate(targets):
                rel_path = os.path.relpath(target, path) if os.path.isdir(path) else os.path.basename(target)
                yield f"data: {json.dumps({'status': 'scanning', 'file': rel_path, 'current': i+1})}\n\n"
                
                # Scan
                report = engine.scan_file(target)
                
                # AI Analysis
                if ai and groq_key:
                    yield f"data: {json.dumps({'status': 'ai_analyzing', 'file': rel_path})}\n\n"
                    # Giả lập AI call hoặc tích hợp thực tế ở đây
                
                # Weaponize
                if pwn:
                    yield f"data: {json.dumps({'status': 'weaponizing', 'file': rel_path})}\n\n"
                    wpp = Weaponizer(target, report)
                    # Chạy quy trình pwn mặc định nếu cần
                
                yield f"data: {json.dumps({'status': 'done', 'file': rel_path, 'report': report})}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/api/reports', methods=['GET'])
def get_reports():
    reports = []
    for f in os.listdir(REPORT_DIR):
        if f.endswith('.md'):
            reports.append(f)
    return jsonify(reports)

@app.route('/api/payloads', methods=['GET'])
def get_payloads():
    payloads = []
    if os.path.exists(PAYLOAD_DIR):
        for root_dir, dirs, files in os.walk(PAYLOAD_DIR):
            for file in files:
                payloads.append(os.path.relpath(os.path.join(root_dir, file), PAYLOAD_DIR))
    return jsonify(payloads)

@app.route('/api/browse-native', methods=['GET'])
def browse_native():
    mode = request.args.get('mode', 'folder')
    try:
        # Lệnh AppleScript trực tiếp thông qua Finder
        if mode == 'file':
            ascript = 'choose file with prompt "Chọn tệp mục tiêu Pentest"'
        else:
            ascript = 'choose folder with prompt "Chọn thư mục mục tiêu Pentest"'
            
        cmd = f"osascript -e 'tell application \"Finder\"' -e 'activate' -e 'POSIX path of ({ascript})' -e 'end tell'"
        
        # Timeout 60 giây
        result = subprocess.check_output(cmd, shell=True, text=True, timeout=60).strip()
        return jsonify({"path": result if result else None})
    except subprocess.TimeoutExpired:
        return jsonify({"path": None, "error": "Quá thời gian chọn file"}), 408
    except subprocess.CalledProcessError:
        return jsonify({"path": None})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reports/<path:filename>')
def serve_report(filename):
    return send_from_directory(REPORT_DIR, filename)

if __name__ == '__main__':
    print(f"[*] APS Dashboard starting on http://localhost:5050")
    app.run(host='0.0.0.0', port=5050, debug=True)
