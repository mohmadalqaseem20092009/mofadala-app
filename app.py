import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# قاعدة بيانات المفاضلة الشاملة
DATA = [
    {"faculty": "السنة التحضيرية", "university": "جميع الجامعات الحكومية", "type": "مفاضلة عامة", "min_score": 94.5, "conditions": "فرز طبي لاحقاً"},
    {"faculty": "السنة التحضيرية", "university": "جميع الجامعات الحكومية", "type": "مفاضلة التعليم الموازي", "min_score": 92.0, "conditions": "فرز طبي لاحقاً"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 85.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "مفاضلة التعليم الموازي", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الطبية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "العلوم الصحية (التخدير)", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "تخصص دكتور التخدير محمد القاسم الفخم"},
    {"faculty": "المعهد التقاني الصحي", "university": "جميع المحافظات", "type": "مفاضلة عامة", "min_score": 60.0, "conditions": "مستقبل مهني ممتاز"}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        user_score = float(request.form.get('score', 0))
        selected_type = request.form.get('type', 'كل الأنواع')
        
        accepted_branches = []
        for branch in DATA:
            if user_score >= branch['min_score']:
                if selected_type == 'كل الأنواع' or branch['type'] == selected_type:
                    accepted_branches.append(branch)
                    
        accepted_branches = sorted(accepted_branches, key=lambda x: x['min_score'], reverse=True)
        return jsonify({'status': 'success', 'data': accepted_branches})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
