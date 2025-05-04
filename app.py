from flask import Flask, render_template, redirect, url_for, session
from models.user import User
from models import db
from auth.routes import auth_bp
from course.routes import course_bp
from course.models import Course, UserCourse
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretdev123"
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database", "db.sqlite")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.register_blueprint(auth_bp)
app.register_blueprint(course_bp, url_prefix="/course")
db.init_app(app)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user_id = session["user_id"]
    user = User.query.get(user_id)
    user_courses = UserCourse.query.filter_by(user_id=user_id).all()

    for uc in user_courses:
        print("COURSE:", uc.course.name)

    return render_template("dashboard.html", user=user, user_courses=user_courses)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)