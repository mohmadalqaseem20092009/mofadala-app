import os
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd # ستحتاج لإضافة pandas في ملف requirements.txt

app = Flask(__name__)

# قاعدة البيانات المحدثة لتشمل التخصصات والجامعات الأساسية
DATA = [
    {"faculty": "السنة التحضيرية للكليات الطبية", "university": "جميع الجامعات الحكومية", "type": "عام", "min_score": 94.5},
    {"faculty": "السنة التحضيرية للكليات الطبية", "university": "جميع الجامعات الحكومية", "type": "موازي", "min_score": 92.0},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "عام", "min_score": 85.0},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "موازي", "min_score": 80.0},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حلب", "type": "عام", "min_score": 84.0},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حلب", "type": "موازي", "min_score": 79.0},
    {"faculty": "الهندسة الطبية", "university": "جامعة دمشق", "type": "عام", "min_score": 80.0},
    {"faculty": "الهندسة الطبية", "university": "جامعة دمشق", "type": "موازي", "min_score": 77.0},
    {"faculty": "الهندسة المعمارية", "university": "جامعة دمشق", "type": "عام", "min_score": 75.0},
    {"faculty": "الهندسة المعمارية", "university": "جامعة دمشق", "type": "موازي", "min_score": 72.0},
    {"faculty": "الهندسة المدنية", "university": "جامعة إدلب", "type": "عام", "min_score": 72.0},
    {"faculty": "الهندسة المدنية", "university": "جامعة حلب", "type": "موازي", "min_score": 67.0},
    {"faculty": "الهندسة المدنية", "university": "جامعة إدلب", "type": "موازي", "min_score": 65.0},
    {"faculty": "كلية الاقتصاد", "university": "جامعة دمشق", "type": "عام", "min_score": 68.0},
    {"faculty": "كلية الحقوق", "university": "جامعة دمشق", "type": "عام", "min_score": 55.0}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_faculty():
    user_score = request.args.get('score', type=float)
    selected_type = request.args.get('type', type=str, default='all')
    accepted_branches = []
    
    for branch in DATA:
        if user_score is not None and user_score < branch['min_score']:
            continue
        if selected_type and selected_type != 'all':
            if selected_type != branch['type']:
                continue
        accepted_branches.append(branch)
        
    accepted_branches = sorted(accepted_branches, key=lambda x: x['min_score'], reverse=True)
    return jsonify({"status": "success", "data": accepted_branches})

@app.route('/api/submit_wishes', methods=['POST'])
def submit_wishes():
    post_data = request.get_json() or {}
    wishes_list = post_data.get('wishes', [])
    
    file_name = "student_wishes.xlsx"
    
    try:
        # بناء جدول البيانات لتصديره إلى ملف إكسل نظيف ومحترف
        rows = []
        for index, wish in enumerate(wishes_list):
            rows.append({
                "ترتيب الرغبة": index + 1,
                "الكلية / المعهد": wish.get('faculty', ''),
                "الجامعة": wish.get('university', ''),
                "نوع القبول": wish.get('type', '')
            })
        
        df = pd.DataFrame(rows)
        df.to_excel(file_name, index=False)
        
        return jsonify({"status": "success", "file_created": file_name})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"<h3>File not found!</h3>", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
