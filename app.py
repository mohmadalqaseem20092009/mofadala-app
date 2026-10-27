import os
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# قاعدة بيانات المفاضلة الشاملة المبنية على ملفك الرسمي (22 صفحة)
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
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة البعث (حمص) - برمجيات", "type": "مفاضلة عامة", "min_score": 84.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة البعث (حمص) - شبكات", "type": "مفاضلة عامة", "min_score": 84.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة البعث (حمص) - ذكاء اصطناعي", "type": "مفاضلة عامة", "min_score": 84.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حماة", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},

    # 3. الهندسات الطبية والميكانيكية والمعمارية والمدنية
    {"faculty": "الهندسة الطبية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الطبية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط النجاح في مسابقة العمارة الوزارية"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة حلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط النجاح في مسابقة العمارة الوزارية"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط النجاح في مسابقة العمارة الوزارية"},
    {"faculty": "الهندسة المدنية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المدنية", "university": "جامعة حلب", "type": "مفاضلة عامة", "min_score": 78.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المدنية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة عامة", "min_score": 78.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المدنية", "university": "جامعة البعث (حمص)", "type": "مفاضلة عامة", "min_score": 78.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الإلكترونيات والاتصالات", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الحواسيب والأتمتة", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الميكاترونيك", "university": "جامعة حلب / اللاذقية / حمص", "type": "مفاضلة عامة", "min_score": 72.0, "conditions": "لا يوجد"},

    # 4. كليات العلوم الصحية والتمريض والطب البيطري والزراعة
    {"faculty": "الطب البيطري", "university": "جامعة حماة / إدلب / درعا", "type": "مفاضلة عامة", "min_score": 65.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الزراعية", "university": "دمشق / حلب / اللاذقية / حمص", "type": "مفاضلة عامة", "min_score": 70.0, "conditions": "لا يوجد"},
    {"faculty": "العلوم الصحية (التخدير)", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "تخصص دكتور التخدير محمد القاسم الفخم"},
    {"faculty": "العلوم الصحية (التحليل المخبري)", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط فحص اللياقة"},
    {"faculty": "العلوم الصحية (علاج وظيفي وسمعيات)", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "خاضع للاختبار الطبي"},
    {"faculty": "التمريض", "university": "حلب / اللاذقية / حماة / حمص", "type": "مفاضلة عامة", "min_score": 65.0, "conditions": "شرط المقابلة الشخصية وجنسية سورية"},

    # 5. الكليات النظرية والمعاهد التقنية والصحية الملتزمة
    {"faculty": "كلية الاقتصاد", "university": "دمشق / حلب / اللاذقية / طرطوس", "type": "مفاضلة عامة", "min_score": 68.0, "conditions": "لا يوجد"},
    {"faculty": "كلية الحقوق", "university": "دمشق / حلب / إدلب / اللاذقية / حمص", "type": "مفاضلة عامة", "min_score": 55.0, "conditions": "لا يوجد"},
    {"faculty": "كلية الإعلام", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 65.0, "conditions": "حيازة 80% في مادة اللغة العربية أو الأجنبية"},
    {"faculty": "كلية الشريعة", "university": "دمشق / حلب / اللاذقية / حمص", "type": "مفاضلة عامة", "min_score": 55.0, "conditions": "حيازة 60% في التربية الدينية واللغة العربية"},
    {"faculty": "المعهد التقاني الطبي (تخدير / مخابر / أشعة)", "university": "دمشق / حلب / اللاذقية / حمص", "type": "مفاضلة عامة", "min_score": 65.0, "conditions": "مفاضلة معاهد علمية"},
    {"faculty": "المعهد التقاني الصحي (صيدلة / تخدير / بصريات)", "university": "دمشق / حلب / طرطوس / الحسكة", "type": "مفاضلة عامة", "min_score": 60.0, "conditions": "مستقبل مهني ممتاز"},
    {"faculty": "المعهد التقاني للحاسوب", "university": "دمشق / حلب / اللاذقية / حمص / إدلب", "type": "مفاضلة عامة", "min_score": 60.0, "conditions": "شرط حيازة 60% في مادة الرياضيات"},
    {"faculty": "المعهد التقاني للنفط والغاز (ملتزم - ذكور)", "university": "حمص / دير الزور / طرطوس / الحسكة", "type": "مفاضلة عامة", "min_score": 60.0, "conditions": "توظيف مباشر بعد التخرج للذكور مواليد 2003 فما فوق"}
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
            # فلترة الرغبات بناءً على مجموع الطالب ونوع المفاضلة المختارة
            if user_score >= branch['min_score']:
                if selected_type == 'كل الأنواع' or branch['type'] == selected_type:
                    accepted_branches.append(branch)
                    
        # ترتيب الكليات المتاحة من الأعلى معدلاً إلى الأدنى لتظهر بشكل احترافي
        accepted_branches = sorted(accepted_branches, key=lambda x: x['min_score'], reverse=True)
        return jsonify({'status': 'success', 'data': accepted_branches})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
