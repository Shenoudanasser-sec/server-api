from flask import Flask, request, jsonify
import pyclamd
import os

app = Flask(__name__)

# إنشاء كائن ClamAV
clamav = pyclamd.ClamdAgnostic()

@app.route('/scan', methods=['POST'])
def scan_file():
    # التأكد من أن الملف تم إرساله في الطلب
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    # فحص الملف باستخدام ClamAV
    try:
        result = clamav.scan_file(file_path)
        
        # التأكد من أن النتيجة ليست None
        if result:
            # تحقق من أن النتيجة عبارة عن tuple أو list وأنها تحتوي على أكثر من عنصر
            if isinstance(result, tuple) and len(result) > 1:
                return jsonify({"status": "infected", "virus": result[1]}), 200
            elif isinstance(result, dict):
                # في حال كانت النتيجة قاموسًا يحتوي على معلومات الفيروس
                return jsonify({"status": "infected", "virus": result.get('virus', 'Unknown virus')}), 200
            else:
                return jsonify({"status": "clean"}), 200
        else:
            # إذا كانت النتيجة None، فهذا يعني أن الملف نظيف
            return jsonify({"status": "clean"}), 200
    except Exception as e:
        # في حال حدوث أي خطأ أثناء فحص الملف
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
