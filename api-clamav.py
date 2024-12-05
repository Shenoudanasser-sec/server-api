from flask import Flask, request, jsonify
import pyclamd
import os

app = Flask(__name__)

# إنشاء كائن ClamAV
clamav = pyclamd.ClamdAgnostic()

@app.route('/scan', methods=['POST'])
def scan_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    # فحص الملف باستخدام ClamAV
    result = clamav.scan_file(file_path)
    
    if result:
        return jsonify({"status": "infected", "virus": result[1]}), 200
    else:
        return jsonify({"status": "clean"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
