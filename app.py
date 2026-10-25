from flask import Flask, render_template_string, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = 'mofadala_history.xlsx'

DATA_COLLEGES = [
    {"name": "السنة التحضيرية للكليات الطبية", "university": "جامعة دمشق", "general": 94.5, "parallel": 92.0},
    {"name": "السنة التحضيرية للكليات الطبية", "university": "جامعة حلب", "general": 94.0, "parallel": 91.5},
    {"name": "السنة التحضيرية للكليات الطبية", "university": "جامعة تشرين (اللاذقية)", "general": 94.0, "parallel": 91.5},
    {"name": "السنة التحضيرية للكليات الطبية", "university": "جامعة البعث (حمص)", "general": 93.8, "parallel": 91.0},
    {"name": "الهندسة المعلوماتية", "university": "جامعة دمشق", "general": 85.0, "parallel": 80.0},
    {"name": "الهندسة المعلوماتية", "university": "جامعة حلب", "general": 84.0, "parallel": 79.0},
    {"name": "الهندسة الطبية", "university": "جامعة دمشق", "general": 80.0, "parallel": 75.0},
    {"name": "الهندسة المعمارية", "university": "جامعة دمشق", "general": 75.0, "parallel": 70.0},
    {"name": "الهندسة المدنية", "university": "جامعة دمشق", "general": 80.0, "parallel": 75.0},
    {"name": "كلية الاقتصاد", "university": "جامعة دمشق", "general": 75.0, "parallel": 62.0},
    {"name": "كلية الحقوق", "university": "جامعة دمشق", "general": 60.0, "parallel": 50.0},
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google" content="notranslate">
    <title>بوابة التنبؤ بمفاضلة الفرع العلمي 2026</title>
    <link href="https://googleapis.com" rel="stylesheet">
    <style>
        :root { --bg-color: #f4f6f4; --card-bg: #ffffff; --primary: #2d4a22; --primary-hover: #1e3316; --text-main: #1e293b; --text-muted: #64748b; --success: #10b981; --danger: #ef4444; --border: #e2e8f0; }
        body { font-family: 'Tajawal', sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 20px; display: flex; justify-content: center; align-items: flex-start; min-height: 100vh; }
        .main-container { width: 100%; max-width: 850px; background: var(--card-bg); border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); padding: 40px 30px; box-sizing: border-box; }
        .header { text-align: center; margin-bottom: 35px; }
        .header h1 { font-size: 28px; font-weight: 900; color: var(--primary); margin: 0 0 10px 0; }
        .header p { color: var(--text-muted); margin: 0; font-size: 16px; }
        .form-section { background: #f8fafc; padding: 25px; border-radius: 18px; border: 1px solid var(--border); margin-bottom: 35px; }
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 600px) { .form-grid { grid-template-columns: 1fr; } body { padding: 10px; } .main-container { padding: 25px 15px; border-radius: 16px; } }
        label { display: block; font-weight: 700; margin-bottom: 8px; font-size: 15px; }
        input[type="number"], select { width: 100%; padding: 14px; border: 2px solid var(--border); border-radius: 12px; font-size: 16px; font-family: inherit; box-sizing: border-box; outline: none; transition: border-color 0.3s; }
        input[type="number"]:focus, select:focus { border-color: var(--primary); }
        button { grid-column: 1 / -1; width: 100%; padding: 15px; background-color: var(--primary); color: white; border: none; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; transition: background 0.3s, transform 0.1s; }
        button:hover { background-color: var(--primary-hover); }
        button:active { transform: scale(0.99); }
        .results-header { font-size: 20px; font-weight: 700; margin-bottom: 20px; border-bottom: 2px solid var(--border); padding-bottom: 10px; display: flex; justify-content: space-between; }
        .results-grid { display: grid; grid-template-columns: 1fr; gap: 15px; }
        .college-card { border: 1px solid var(--border); border-radius: 14px; padding: 20px; display: flex; justify-content: space-between; align-items: center; transition: transform 0.2s, box-shadow 0.2s; }
        .college-card:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.03); }
        .college-info h3 { margin: 0 0 6px 0; font-size: 18px; font-weight: 700; }
        .college-info p { margin: 0; color: var(--text-muted); font-size: 14px; }
        .status-badge { padding: 8px 16px; border-radius: 30px; font-weight: 700; font-size: 14px; text-align: center; min-width: 110px; }
        .badge-success { background-color: #d1fae5; color: var(--success); }
        .badge-danger { background-color: #fee2e2; color: var(--danger); }
    </style>
</head>
<body>
<div class="main-container">
    <div class="header">
        <h1>🎓 نظام فرز مفاضلة الفرع العلمي</h1>
        <p>أدخل مجموعك المئوي لمعرفة الكليات والجامعات المتاحة لك لعام 2026/2027</p>
    </div>
    <p style="text-align: center; color: var(--primary); font-size: 16px; margin-bottom: 10px; font-weight: 700;">💻 تصميم وتطوير المبرمج محمد القاسم</p>

    <div class="form-section">
        <form method="POST" action="/">
            <div class="form-grid">
                <div>
                    <label for="score">مجموعك المئوي الصافي (%):</label>
                    <input type="number" step="0.01" min="50" max="100" name="score" id="score" value="{{ user_score }}" placeholder="مثال: 83.5" required>
                </div>
                <div>
                    <label for="type">نوع المفاضلة المستهدفة:</label>
                    <select name="type" id="type">
                        <option value="general" {% if selected_type == 'general' %}selected{% endif %}>مفاضلة عامة</option>
                        <option value="parallel" {% if selected_type == 'parallel' %}selected{% endif %}>تعليم موازي</option>
                    </select>
                </div>
                <button type="submit">🔍 تحليل درجاتي وعرض الأفرع</button>
            </div>
        </form>
    </div>
    {% if results is not none %}
    <div class="results-header">
        <span>نتائج الفحص والتحليل التلقائي:</span>
        <span style="color: var(--primary);">مجموعك: {{ user_score }}%</span>
    </div>
    <div class="results-grid">
        {% for college in results %}
        <div class="college-card">
            <div class="college-info">
                <h3>{{ college.name }}</h3>
                <p>📍 {{ college.university }} | الحد المطلوب: {{ college.required_score }}%</p>
            </div>
            <div>
                {% if college.is_available %}
                <div class="status-badge badge-success">✓ متاح لك للتدوين</div>
                {% else %}
                <div class="status-badge badge-danger">✕ أعلى من مجموعك</div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</div>
</body>
</html>
"""

def save_to_excel(score, mofadala_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {'وقت الفحص': [timestamp], 'المجموع المدخل': [score], 'نوع المفاضلة': ['عامة' if mofadala_type == 'general' else 'موازي']}
    new_df = pd.DataFrame(new_entry)
    if os.path.exists(EXCEL_FILE):
        try:
            old_df = pd.read_excel(EXCEL_FILE)
            combined_df = pd.concat([old_df, new_df], ignore_index=True)
            combined_df.to_excel(EXCEL_FILE, index=False)
        except Exception:
            new_df.to_excel(EXCEL_FILE, index=False)
    else:
        new_df.to_excel(EXCEL_FILE, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_score = ""
    selected_type = "general"
    results = None
    if request.method == 'POST':
        try:
            user_score = float(request.form.get('score', 0))
            selected_type = request.form.get('type', 'general')
            save_to_excel(user_score, selected_type)
            results = []
            for college in DATA_COLLEGES:
                required_score = college['general'] if selected_type == 'general' else college['parallel']
                results.append({
                    "name": college['name'],
                    "university": college['university'],
                    "required_score": required_score,
                    "is_available": user_score >= required_score
                })
            results = sorted(results, key=lambda x: x['is_available'], reverse=True)
        except ValueError:
            pass
    return render_template_string(HTML_TEMPLATE, user_score=user_score, selected_type=selected_type, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
