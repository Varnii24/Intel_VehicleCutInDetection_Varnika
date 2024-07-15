# backend/app.py
from flask import Flask, request, jsonify, send_from_directory
from detect import run_detection
from estimate_depth import run_depth_estimation
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'filepath': filepath})
    return jsonify({'error': 'File upload failed'})

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    image_path = data['image_path']
    detections = run_detection(image_path)
    return jsonify(detections)

@app.route('/estimate_depth', methods=['POST'])
def estimate_depth():
    data = request.get_json()
    image_path = data['image_path']
    depth_map = run_depth_estimation(image_path)
    return jsonify({'depth_map': depth_map})

if __name__ == '__main__':
    app.run(debug=True)
 