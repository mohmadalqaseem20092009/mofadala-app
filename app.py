from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# قاعدة البيانات المهيأة خصيصاً لتتوافق مع نظام الفلترة المطور لديك
DATA = [
    {"name": "السنة التحضيرية للكليات الطبية", "university": "جميع الجامعات", "type": "عامة", "min_score": 94.5},
    {"name": "السنة التحضيرية للكليات الطبية", "university": "جميع الجامعات", "type": "موازي", "min_score": 92.0},
    {"name": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "عامة", "min_score": 85.0},
    {"name": "الهندسة المعلوماتية", "university": "جامعة دمشق", "type": "موازي", "min_score": 80.0},
    {"name": "الهندسة المعلوماتية", "university": "جامعة حلب", "type": "عامة", "min_score": 84.0},
    {"name": "الهندسة المعلوماتية", "university": "جامعة حلب", "type": "موازي", "min_score": 79.0},
    {"name": "الهندسة الطبية", "university": "جامعة دمشق", "type": "عامة", "min_score": 80.0},
    {"name": "الهندسة الطبية", "university": "جامعة دمشق", "type": "موازي", "min_score": 75.0},
    {"name": "كلية الحقوق", "university": "جامعة دمشق", "type": "عامة", "min_score": 65.0},
    {"name": "كلية الحقوق", "university": "جامعة دمشق", "type": "موازي", "min_score": 55.0},
    {"name": "المعهد التقاني الطبي (تخدير)", "university": "جامعة دمشق", "type": "عامة", "min_score": 65.0},
    {"name": "المعهد التقاني الطبي (تخدير)", "university": "جامعة دمشق", "type": "موازي", "min_score": 60.0}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        user_score = float(request.form.get("score", 0))
        selected_type = request.form.get("type", "كل الأنواع")
        
        accepted_branches = []
        for branch in DATA:
            if user_score >= branch["min_score"]:
                if selected_type == "كل الأنواع" or branch["type"] == selected_type:
                    accepted_branches.append(branch)
                    
        # ترتيب الأفرع من الأعلى للأقل بناءً على الحد الأدنى
        accepted_branches = sorted(accepted_branches, key=lambda x: x["min_score"], reverse=True)
        return jsonify({"status": "success", "data": accepted_branches})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
