import os
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# قاعدة البيانات الشاملة والموسعة لملف المفاضلة والفرز الرسمي
DATA = [
    {"faculty": "السنة التحضيرية للكليات الطبية", "university": "جميع الجامعات الحكومية", "type": "مفاضلة عامة", "min_score": 94.5, "conditions": "فرز لاحق (طب بشري، أسنان، صيدلة)"},
    {"faculty": "السنة التحضيرية للكليات الطبية", "university": "جميع الجامعات الحكومية", "type": "مفاضلة التعليم الموازي", "min_score": 92.0, "conditions": "فرز لاحق (طب بشري، أسنان، صيدلة)"},
    {"faculty": "السنة التحضيرية (المحافظات الشرقية)", "university": "دير الزور - الحسكة - الرقة", "type": "مفاضلة عامة", "min_score": 90.0, "conditions": "أبناء المحافظات الشرقية حصراً"},
    {"faculty": "السنة التحضيرية (المحافظات الشرقية)", "university": "دير الزور - الحسكة - الرقة", "type": "مفاضلة التعليم الموازي", "min_score": 85.0, "conditions": "أبناء المحافظات الشرقية حصراً"},
    {"faculty": "كلية الصيدلة", "university": "الجامعات الخاصة (سيرفر افتراضي)", "type": "مفاضلة عامة", "min_score": 88.0, "conditions": "حسب الطاقة الاستيعابية للجامعة"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 85.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "مفاضلة التعليم الموازي", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حلب", "type": "مفاضلة عامة", "min_score": 84.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حلب", "type": "مفاضلة التعليم الموازي", "min_score": 79.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة عامة", "min_score": 84.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة التعليم الموازي", "min_score": 79.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية (برمجيات - شبكات - ذكاء اصطناعي)", "university": "جامعة البعث (حمص)", "type": "مفاضلة عامة", "min_score": 84.0, "conditions": "فرز داخلي بالكلية"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة البعث (حمص)", "type": "مفاضلة التعليم الموازي", "min_score": 78.5, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حماة", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة حماة", "type": "مفاضلة التعليم الموازي", "min_score": 76.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المعلوماتية", "university": "جامعة إدلب", "type": "مفاضلة التعليم الموازي", "min_score": 75.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الطبية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الطبية", "university": "جامعة دمشق", "type": "مفاضلة التعليم الموازي", "min_score": 77.0, "conditions": "متاحة لمجموعك موازي!"},
    {"faculty": "الهندسة الطبية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الطبية", "university": "جامعة تشرين (اللاذقية)", "type": "مفاضلة التعليم الموازي", "min_score": 76.5, "conditions": "متاحة لمجموعك موازي!"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط النجاح في مسابقة العمارة الوزارية"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة دمشق", "type": "مفاضلة التعليم الموازي", "min_score": 72.0, "conditions": "شرط مسابقة العمارة الوزارية"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة حلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط النجاح في مسابقة العمارة الوزارية"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة حلب", "type": "مفاضلة التعليم الموازي", "min_score": 71.5, "conditions": "شرط مسابقة العمارة"},
    {"faculty": "الهندسة المعمارية", "university": "جامعة تشرين / البعث", "type": "مفاضلة عامة", "min_score": 74.5, "conditions": "شرط النجاح في مسابقة العمارة الوزارية"},
    {"faculty": "الهندسة المدنية", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المدنية", "university": "جامعة دمشق", "type": "مفاضلة التعليم الموازي", "min_score": 74.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المدنية", "university": "جامعة حلب / البعث / تشرين", "type": "مفاضلة عامة", "min_score": 78.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة المدنية", "university": "جامعة حلب / البعث / تشرين", "type": "مفاضلة التعليم الموازي", "min_score": 72.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الإلكترونيات والاتصالات", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الإلكترونيات والاتصالات", "university": "جامعة دمشق", "type": "مفاضلة التعليم الموازي", "min_score": 74.5, "conditions": "لا يوجد"},
    {"faculty": "هندسة الحواسيب والأتمتة", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الحواسيب والأتمتة", "university": "جامعة دمشق", "type": "مفاضلة التعليم الموازي", "min_score": 71.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الميكاترونيك", "university": "جامعة حلب / اللاذقية / حمص", "type": "مفاضلة عامة", "min_score": 72.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الميكاترونيك", "university": "جامعة حلب / اللاذقية / حمص", "type": "مفاضلة التعليم الموازي", "min_score": 68.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الهمك (ميكانيك عام / كهرباء)", "university": "جميع الجامعات الحكومية", "type": "مفاضلة عامة", "min_score": 68.0, "conditions": "لا يوجد"},
    {"faculty": "هندسة الهمك (ميكانيك عام / كهرباء)", "university": "جميع الجامعات الحكومية", "type": "مفاضلة التعليم الموازي", "min_score": 64.0, "conditions": "لا يوجد"},
    {"faculty": "العلوم الصحية (التخدير)", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "تخصص دكتور التخدير محمد القاسم الفخم"},
    {"faculty": "العلوم الصحية (التحليل المخبري)", "university": "جامعة إدلب", "type": "مفاضلة عامة", "min_score": 75.0, "conditions": "شرط فحص اللياقة الطبي بالكلية"},
    {"faculty": "العلوم الصحية (علاج وظيفي وسمعيات)", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 80.0, "conditions": "خاضع للاختبار الطبي والنفسي الدراسي"},
    {"faculty": "التمريض", "university": "حلب / اللاذقية / حماة / حمص", "type": "مفاضلة عامة", "min_score": 65.0, "conditions": "شرط المقابلة الشخصية والجنسية العربية السورية"},
    {"faculty": "التمريض", "university": "جامعة دمشق", "type": "مفاضلة عامة", "min_score": 67.0, "conditions": "شرط المقابلة الشخصية"},
    {"faculty": "الطب البيطري", "university": "جامعة حماة / إدلب / درعا", "type": "مفاضلة عامة", "min_score": 65.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الزراعية", "university": "دمشق / حلب / اللاذقية / حمص / طرطوس", "type": "مفاضلة عامة", "min_score": 70.0, "conditions": "لا يوجد"},
    {"faculty": "الهندسة الزراعية", "university": "جميع الجامعات الحكومية", "type": "مفاضلة التعليم الموازي", "min_score": 65.0, "conditions": "لا يوجد"},
    {"faculty": "كلية الاقتصاد", "university": "دمشق / حلب / اللاذقية / حمص", "type": "مفاضلة عامة", "min_score": 68.0, "conditions": "لا يوجد"},
    {"faculty": "كلية الاقتصاد", "university": "دمشق / حلب / اللاذقية / حمص", "type": "مفاضلة التعليم الموازي", "min_score": 62.0, "conditions": "لا يوجد"},
    {"faculty": "كلية الحقوق", "university": "دمشق / حلب / إدلب / اللاذقية", "type": "مفاضلة عامة", "min_score": 55.0, "conditions": "لا يوجد"},
    {"faculty": "كلية الحقوق", "university": "دمشق / حلب / إدلب / اللاذقية", "type": "مفاضلة التعليم الموازي", "min_score": 52.0, "conditions": "لا يوجد"},
    {"faculty": "كلية العلوم (رياضيات / فيزياء / كيمياء)", "university": "جميع الجامعات الحكومية", "type": "مفاضلة عامة", "min_score": 58.0, "conditions": "لا يوجد"},
    {"faculty": "كلية التربية (معلم صف)", "university": "جميع المحافظات السورية", "type": "مفاضلة عامة", "min_score": 62.0, "conditions": "فرز مباشر كمعلم مدرسة ابتدائية لاحقاً"},
    {"faculty": "كلية التربية (معلم صف)", "university": "جميع المحافظات السورية", "type": "مفاضلة التعليم الموازي", "min_score": 58.0, "conditions": "لا يوجد"}
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
            if selected_type == 'موازي' and 'موازي' not in branch['type']:
                continue
            if selected_type == 'عام' and 'عام' not in branch['type']:
                continue
        accepted_branches.append(branch)
        
    accepted_branches = sorted(accepted_branches, key=lambda x: x['min_score'], reverse=True)
    return jsonify({"status": "success", "data": accepted_branches})

@app.route('/api/submit_wishes', methods=['POST'])
def submit_wishes():
    post_data = request.get_json() or {}
    student_name = post_data.get('student_name', 'طالب مجهول')
    wishes_list = post_data.get('wishes', [])
    
    excel_data = []
    for index, wish in enumerate(wishes_list):
        excel_data.append({
            "رقم الرغبة": index + 1,
            "اسم الطالب": student_name,
            "الكلية / المعهد": wish.get('faculty', ''),
            "الجامعة": wish.get('university', ''),
            "نوع القبول": wish.get('type', '')
        })
    
    if excel_data:
