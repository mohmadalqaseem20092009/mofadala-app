import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# قاعدة بيانات المفاضلة الشاملة المبنية على ملفك الرسمي
DATA = [
    # 1. السنة التحضيرية للكليات الطبية
    {"faculty": "السنة التحضيرية", "university": "جميع الجامعات الحكومية", "type": "مفاضلة عامة", "min_score": 94.5, "conditions": "فرز طبي لاحقاً"},
    {"faculty": "السنة التحضيرية", "university": "جميع الجامعات الحكومية", "type": "مفاضلة التعليم الموازي", "min_score": 92.0, "conditions": "فرز طبي لاحقاً"},
    {"faculty": "السنة التحضيرية (المحافظات الشرقية)", "university": "دير الزور - الحسكة - الرقة", "type": "مفاضلة عامة", "min_score": 90.0, "conditions": "أبناء المحافظات الشرقية حصراً"},
    {"faculty": "السنة التحضيرية (المحافظات الشرقية)", "university": "دير الزور - الحسكة - الرقة", "type": "مفاضلة التعليم الموازي", "min_score": 85.0, "conditions": "أبناء المحافظات الشرقية حصراً"},

    # 2. الهندسات الحاسوبية والمعلوماتية والذكاء الاصطناعي
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 85.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "مفاضلة التعليم الموازي", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حلب", "type": "مفاضلة عامة", "min_score": 84.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حلب", "type": "مفاضلة التعليم الموازي", "min_score": 79.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة عامة", "min_score": 84.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة التعليم الموازي", "min_score": 79.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة البعث (حمص)", "type": "مفاضلة عامة", "min_score": 84.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حماة", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},

    # 3. الهندسات الطبية والميكانيكية والمعمارية والمدنية
    {"faculty": "الهندسة الطبية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الطبية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط النجاح في مسابقة العمارة الوزارية"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة حلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط النجاح في مسابقة العمارة الوزارية"},
    {"faculty": "الهندسة المدنية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المدنية", "university": "جامعة حلب", "type": "مفاضلة عامة", "min_score": 78.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الإلكترونيات والاتصالات", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الحواسيب والأتمتة", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "لا يوجد"},

    # 4. كليات العلوم الصحية والتمريض والطب البيطري والزراعة
    {"faculty": "الطب البيطري", "university": "جامعة حماة / إدلب / درعا", "type": "مفاضلة عامة", "min_score": 65.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الزراعية", "university": "دمشق / حلب / اللاذقية / حمص", "type": "مفاضلة عامة", "min_score": 70.0, "conditions": "لا يوجد"},
    {"faculty": "العلوم الصحية (التخدير)", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "تخصص دكتور التخدير محمد القاسم الفخم"},
    {"faculty": "العلوم الصحية (التحليل المخبري)", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط فحص اللياقة"},
    {"faculty": "التمريض", "university": "حلب / اللاذقية / حماة / حمص", "type": "مفاضلة عامة", "min_score": 65.0, "conditions": "شرط المقابلة الشخصية وجنسية سورية"},

    # 5. الكليات النظرية والمعاهد التقنية والصحية
    {"faculty": "كلية الاقتصاد", "university": "دمشق / حلب / اللاذقية / طرطوس", "type": "مفاضلة عامة", "min_score": 68.0, "conditions": "لا يوجد"},
    {"faculty": "كلية الحقوق", "university": "دمشق / حلب / إدلب / اللاذقية", "type": "مفاضلة عامة", "min_score": 55.0, "conditions": "لا يوجد"},
    {"faculty": "المعهد التقاني الطبي", "university": "دمشق / حلب / اللاذقية / حمص", "type": "مفاضلة عامة", "min_score": 65.0, "conditions": "مفاضلة معاهد علمية"},
    {"faculty": "المعهد التقاني الصحي", "university": "دمشق / حلب / طرطوس / الحسكة", "type": "مفاضلة عامة", "min_score": 60.0, "conditions": "مستقبل مهني ممتاز"},
    {"faculty": "المعهد التقاني للحاسوب", "university": "جميع المحافظات", "type": "مفاضلة عامة", "min_score": 60.0, "conditions": "شرط حيازة 60% في مادة الرياضيات"}
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
