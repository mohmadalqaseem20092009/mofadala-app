from flask import Flask, render_template, request

app = Flask(__name__)

# قاعدة البيانات المستخرجة من ملف المفاضلة الرسمي لعام 2025-2026
BRANCHES_DATA = [
    {"name": "السنة التحضيرية للكليات الطبية", "university": "جميع الجامعات", "general": 94.5, "parallel": 92.0},
    {"name": "السنة التحضيرية (المحافظات الشرقية)", "university": "دير الزور - الحسكة - الرقة", "general": 90.0, "parallel": 85.0},
    {"name": "الهندسة المعلوماتية", "university": "جامعة دمشق", "general": 85.0, "parallel": 80.0},
    {"name": "الهندسة المعلوماتية", "university": "جامعة حلب", "general": 84.0, "parallel": 79.0},
    {"name": "الهندسة المعلوماتية", "university": "جامعة اللاذقية", "general": 84.0, "parallel": 79.0},
    {"name": "الهندسة المعلوماتية (برمجيات)", "university": "جامعة حمص", "general": 84.0, "parallel": 80.0},
    {"name": "الهندسة الطبية", "university": "جامعة دمشق", "general": 80.0, "parallel": 75.0},
    {"name": "الهندسة المدنية", "university": "جامعة دمشق", "general": 80.0, "parallel": 75.0},
    {"name": "الهندسة المعمارية", "university": "جامعة دمشق", "general": 75.0, "parallel": 70.0},
    {"name": "الطب البيطري", "university": "جامعة حماة", "general": 68.0, "parallel": 63.0},
    {"name": "الهندسة الزراعية", "university": "جامعة دمشق", "general": 70.0, "parallel": 62.0},
    {"name": "كلية الاقتصاد", "university": "جامعة دمشق", "general": 75.0, "parallel": 62.0},
    {"name": "كلية الحقوق", "university": "جامعة دمشق", "general": 65.0, "parallel": 55.0},
    {"name": "كلية الإعلام", "university": "جامعة دمشق", "general": 65.0, "parallel": 60.0},
    {"name": "المعهد التقاني لطب الأسنان (تعويضات)", "university": "جامعة حلب", "general": 70.0, "parallel": 60.0},
    {"name": "المعهد التقاني الطبي (تخدير)", "university": "جامعة دمشق", "general": 65.0, "parallel": 60.0}
]

@app.route("/", methods=["GET", "POST"])
def index():
    eligible_branches = []
    score = None
    
    if request.method == "POST":
        try:
            score = float(request.form.get("score", 0))
            for branch in BRANCHES_DATA:
                can_general = score >= branch["general"]
                can_parallel = score >= branch["parallel"]
                
                # إذا كان الطالب مؤهلاً لأي منهما، يتم إضافة الفرع للنتائج
                if can_general or can_parallel:
                    eligible_branches.append({
                        "name": branch["name"],
                        "university": branch["university"],
                        "general_req": branch["general"],
                        "parallel_req": branch["parallel"],
                        "status_general": "متاح ✅" if can_general else "غير متاح ❌",
                        "status_parallel": "متاح ✅" if can_parallel else "غير متاح ❌"
                    })
        except ValueError:
            pass
            
    return render_template("index.html", eligible_branches=eligible_branches, score=score)

if __name__ == "__main__":
    app.run(debug=True)

