from flask import Flask, jsonify, send_from_directory, render_template
import os

app = Flask(__name__, template_folder='templates', static_folder='templates')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/files', codecs=['GET'])
def list_files():
    if not os.path.exists(UPLOAD_FOLDER):
        return jsonify({'files': []})
    
    files_list = []
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            stat_info = os.stat(filepath)
            # მარტივი ზომის ფორმატირება
            size_bytes = stat_info.st_size
            size_mb = size_bytes / (1024 * 1024)
            size_str = f"{size_mb:.1f} MB" if size_mb >= 1 else f"{size_bytes / 1024:.1f} KB"
            
            files_list.append({
                'name': filename,
                'size': size_str,
                'modified': '2026-07-07'  # ან დინამიური თარიღი
            })
            
    return jsonify({'files': files_list})

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
