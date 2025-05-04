import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, send_from_directory, abort, flash
from course.models import db, Course, UserCourse, UserPracticeGeneration
from models.user import User
from datetime import date, timedelta, datetime
from utils.ai_generate import generate_practice_questions

course_bp = Blueprint("course", __name__, url_prefix="/course")

# Predefined course for now
PRELOADED_COURSES = [
    {"name": "AP Psychology", "exam_date": "2025-05-16"},
    {"name": "AP Calculus AB", "exam_date": "2025-05-13"},
    {"name": "AP US History", "exam_date": "2025-05-09"},
]

UNIT_COUNTS = {
    "AP Psychology": 9,
    "AP Calculus AB": 8,
    "AP US History": 9
}

@course_bp.before_request
def preload_courses():
    for course in PRELOADED_COURSES:
        if not Course.query.filter_by(name=course["name"]).first():
            new_course = Course(
                name=course["name"],
                exam_date=date.fromisoformat(course["exam_date"])
            )
            db.session.add(new_course)
    db.session.commit()

@course_bp.route("/select", methods=["GET", "POST"])
def add_course():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user_id = session["user_id"]
    user_course_ids = {uc.course_id for uc in UserCourse.query.filter_by(user_id=user_id).all()}

    available_courses = Course.query.filter(~Course.id.in_(user_course_ids)).all()

    if request.method == "POST":
        selected_id = int(request.form.get("course_id"))
        if selected_id not in user_course_ids:
            db.session.add(UserCourse(user_id=user_id, course_id=selected_id))
            db.session.commit()
        return redirect(url_for("dashboard"))
    
    return render_template("select_course.html", courses=available_courses)

@course_bp.route("/<int:course_id>")
def view_course(course_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    course = Course.query.get_or_404(course_id)
    return render_template("course.html", course=course)

@course_bp.route("/<int:course_id>/vocab")
def vocab_flashcards(course_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    unit_index = int(request.args.get("unit", 0))
    course = Course.query.get_or_404(course_id)

    # Construct expected JSON path from course name (normalized)
    filename = course.name.lower().replace(" ", "_").replace("-", "") + "_vocab.json"
    vocab_path = os.path.join("static", "data", filename)

    vocab_data = {"units": []}
    if os.path.exists(vocab_path):
        with open(vocab_path, "r") as f:
            vocab_data = json.load(f)

    # Check if there are units, else render blank page
    if not vocab_data["units"]:
        return render_template(
            "vocab.html",
            course=course,
            units=[],
            unit_data=[],
            current_unit=0
        )

    # Boundary check for unit index
    if unit_index < 0 or unit_index >= len(vocab_data["units"]):
        abort(404)

    unit_data = vocab_data["units"][unit_index]["terms"]
    return render_template(
        "vocab.html",
        course=course,
        units=vocab_data["units"],
        unit_data=unit_data,
        current_unit=unit_index
    )

@course_bp.route('/<int:course_id>/practice', methods=['GET', 'POST'])
def practice(course_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    course = Course.query.get_or_404(course_id)

    # Supported course mapping: Display Name → File Key
    supported_courses = {
        "AP Psychology": "ap_psychology",
        "AP Calculus AB": "ap_calculus_ab",
        "AP US History": "ap_us_history"
    }

    if course.name not in supported_courses:
        flash("Practice questions for this course are not yet supported.", "warning")
        return render_template('practice.html', questions=[], unit=1, course_id=course_id, unsupported=True)

    course_key = supported_courses[course.name]
    unit = int(request.args.get('unit', 1))

    max_units = UNIT_COUNTS.get(course.name, 9)
    if unit < 1 or unit > max_units:
        unit = 1

    file_path = f'static/data/practice_questions/{course_key}.json'

    # Load cached questions
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    unit_key = f'unit_{unit}'
    questions = data.get(unit_key, [])

    if request.method == 'POST':
        now = datetime.utcnow()
        record = UserPracticeGeneration.query.filter_by(
            user_id=user_id, course_id=course_id, unit_number=unit
        ).first()

        if record and now - record.last_generated < timedelta(hours=24):
            flash('You can only generate new questions once every 24 hours.', 'warning')
        else:
            try:
                content = generate_practice_questions(course.name, unit)
                new_questions = json.loads(content)

                data[unit_key] = new_questions
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)

                if record:
                    record.last_generated = now
                else:
                    record = UserPracticeGeneration(
                        user_id=user_id,
                        course_id=course_id,
                        unit_number=unit,
                        last_generated=now
                    )
                    db.session.add(record)

                db.session.commit()
                questions = new_questions
                flash('New questions generated successfully.', 'success')

            except Exception as e:
                flash(f'Error generating questions: {e}', 'danger')

    return render_template(
        "practice.html",
        questions=questions,
        unit=unit,
        course_id=course_id,
        course=course,
        unit_count=max_units,
        unsupported=(course.name not in supported_courses)
    )

@course_bp.route('/<int:course_id>/mock_exam')
def mock_exam(course_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    course = Course.query.get_or_404(course_id)

    # Only supported for AP Psychology for now
    if course.name != "AP Psychology":
        flash("Mock exam support is not yet available for this course.", "warning")
        return redirect(url_for("course.view_course", course_id=course.id))

    mcqs, frqs = [], []

    try:
        with open("static/data/mock_exams/ap_psychology/section_1_mcqs.json", "r", encoding="utf-8") as f:
            mcqs_data = json.load(f)
            mcqs = mcqs_data.get("questions", [])

        with open("static/data/mock_exams/ap_psychology/section_2_frqs.json", "r", encoding="utf-8") as f:
            frqs = json.load(f)

    except Exception as e:
        flash(f"Error loading mock exam data: {e}", "danger")

    return render_template("mock_exam.html", mcqs=mcqs, frqs=frqs, course=course)


