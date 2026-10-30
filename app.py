import os
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# قاعدة البيانات المدمجة السريعة المحدثة لتطابق الاختيارات
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
    {"faculty": "الهندسة المدنية", "university": "جامعة دمشق", "type": "عام", "min_score": 80.0},
    {"faculty": "الهندسة المدنية", "university": "جامعة دمشق", "type": "موازي", "min_score": 74.0},
    {"faculty": "هندسة الميكاترونيك", "university": "جامعة حلب", "type": "عام", "min_score": 72.0},
    {"faculty": "هندسة الميكاترونيك", "university": "جامعة حلب", "type": "موازي", "min_score": 68.0},
    {"faculty": "هندسة الهمك (ميكانيك عام / كهرباء)", "university": "جميع الجامعات الحكومية", "type": "عام", "min_score": 68.0},
    {"faculty": "هندسة الهمك (ميكانيك عام / كهرباء)", "university": "جميع الجامعات الحكومية", "type": "موازي", "min_score": 64.0},
    {"faculty": "كلية الاقتصاد", "university": "جامعة دمشق", "type": "عام", "min_score": 68.0},
    {"faculty": "كلية الحقوق", "university": "جامعة دمشق", "type": "عام", "min_score": 55.0}
]

@app.route('/')
def home():
    # إرسال واجهة الـ HTML مباشرة من السيرفر لضمان كسر التجميد والتعليق
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>مفاضلة القبول الجامعي</title>
        <style>
            body { background-color: #121212; color: #e0e0e0; font-family: system-ui, sans-serif; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: start; min-height: 100vh; }
            .container { width: 100%; max-width: 500px; background-color: #1e1e1e; border: 1px solid #2d2d2d; border-radius: 12px; padding: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.4); box-sizing: border-box; }
            .header { text-align: center; position: relative; margin-bottom: 24px; }
            .theme-toggle-btn { position: absolute; left: 0; top: 0; background-color: rgba(245, 158, 11, 0.1); color: #f59e0b; font-size: 11px; padding: 5px 12px; border-radius: 20px; border: 1px solid rgba(245, 158, 11, 0.2); cursor: pointer; font-weight: bold; }
            .header h1 { color: #10b981; font-size: 20px; margin: 0; }
            .header p { color: #888; font-size: 13px; margin: 4px 0 0 0; }
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 8px; font-size: 14px; font-weight: bold; text-align: right; }
            .form-group input, .form-group select { width: 100%; box-sizing: border-box; background-color: #121212; border: 1px solid #2d2d2d; border-radius: 8px; padding: 12px; color: #ffffff; font-size: 16px; text-align: center; outline: none; }
            .analyze-btn { width: 100%; background-color: #059669; color: white; border: none; padding: 12px; border-radius: 8px; font-size: 15px; font-weight: bold; cursor: pointer; margin-bottom: 20px; }
            .wishes-container { border: 1px dashed #0284c7; background-color: rgba(2, 132, 199, 0.05); border-radius: 8px; padding: 16px; margin-bottom: 20px; }
            .wishes-header { color: #38bdf8; font-size: 13px; font-weight: bold; margin-bottom: 12px; text-align: right; }
            .wish-row { background-color: #121212; padding: 12px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; margin-bottom: 12px; border: 1px solid #2d2d2d; }
            .delete-btn { background-color: #dc2626; color: white; border: none; padding: 4px 10px; border-radius: 4px; font-size: 11px; cursor: pointer; }
            .submit-btn { width: 100%; background-color: #059669; color: white; border: none; padding: 12px; border-radius: 8px; font-size: 15px; font-weight: bold; cursor: pointer; }
            .available-title { font-size: 14px; color: #888; margin: 20px 0 10px 0; text-align: right; }
            .branch-list { max-height: 260px; overflow-y: auto; }
            .branch-item { background-color: #121212; border: 1px solid #2d2d2d; border-radius: 8px; padding: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 13px; }
            .branch-details { text-align: right; }
            .branch-name { font-weight: bold; color: #ffffff; }
            .branch-sub { color: #888; font-size: 11px; margin-top: 2px; }
            .branch-left { display: flex; align-items: center; gap: 12px; }
            .min-score { color: #10b981; font-weight: bold; }
            .add-btn { background-color: #2563eb; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 12px; cursor: pointer; }
            .hidden { display: none !important; }
            .download-btn { display: inline-block; background-color: #0284c7; color: white; padding: 10px 16px; border-radius: 6px; text-decoration: none; font-size: 13px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container" id="mainContainer">
            <div class="header">
                <button onclick="toggleTheme()" id="themeBtn" class="theme-toggle-btn">☀️ مشرق</button>
                <h1>مفاضلة القبول الجامعي</h1>
                <p>المهندس محمد القاسم</p>
            </div>
            <div class="form-group">
                <label>أدخل مجموعك المئوي (%):</label>
                <input type="text" id="studentScore" value="86">
            </div>
            <div class="form-group">
                <label>نوع المفاضلة:</label>
                <select id="competitionType">
                    <option value="all">كل المفاضلات</option>
                    <option value="عام" selected>مفاضلة عامة</option>
                    <option value="موازي">مفاضلة التعليم الموازي</option>
                </select>
            </div>
            <button onclick="searchBranches()" class="analyze-btn">✨ تحليل درجاتي وعرض الأفرع</button>
            <div id="wishesBox" class="wishes-container hidden">
                <div class="wishes-header">📋 رغباتك المختارة:</div>
                <div id="selectedWishesList"></div>
                <button onclick="submitWishes()" class="submit-btn">تثبيت</button>
                <div id="downloadArea" class="hidden" style="text-align: center;"></div>
            </div>
            <div class="available-title">الأفرع المتاحة لمجموعك:</div>
            <div id="availableBranches" class="branch-list"></div>
        </div>
        <script>
            let selectedWishes = [];
            let isLight = false;

            function toggleTheme() {
                isLight = !isLight;
                const btn = document.getElementById('themeBtn');
                const container = document.getElementById('mainContainer');
                if (isLight) {
                    document.body.style.backgroundColor = '#f3f4f6';
                    document.body.style.color = '#1f2937';
                    container.style.backgroundColor = '#ffffff';
                    container.style.borderColor = '#e5e7eb';
                    btn.innerHTML = '🌙 مظلم';
                } else {
                    document.body.style.backgroundColor = '#121212';
                    document.body.style.color = '#e0e0e0';
                    container.style.backgroundColor = '#1e1e1e';
                    container.style.borderColor = '#2d2d2d';
                    btn.innerHTML = '☀️ مشرق';
                }
            }

            async function searchBranches() {
                const scoreInput = document.getElementById('studentScore').value;
                const cleanScore = scoreInput.replace(/[٠-٩]/g, d => d.charCodeAt(0) - 1632);
                const score = parseFloat(cleanScore);
                const type = document.getElementById('competitionType').value;
                const container = document.getElementById('availableBranches');
                container.innerHTML = '';

                if (isNaN(score)) return alert('الرجاء كتابة مجموع صحيح');

                try {
                    const response = await fetch(`/api/search?score=${score}&type=${type}`);
                    const result = await response.json();
                    if (result.status === 'success') {
                        let filtered = result.data.filter(branch => !selectedWishes.some(w => w.faculty === branch.faculty && w.type === branch.type));
                        if (filtered.length === 0) { container.innerHTML = '<p style="text-align:center;font-size:12px;color:#888;padding:10px;">لا توجد خيارات متاحة.</p>'; return; }
                        filtered.forEach(branch => {
                            const div = document.createElement('div');
                            div.className = 'branch-item';
