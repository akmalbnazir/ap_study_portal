from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email")
        password = request.form.get("password")

        if action == "login":
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session["user_id"] = user.id
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid login credentials.")
        
        elif action == "signup":
            if User.query.filter_by(email=email).first():
                flash("Email already exists.")
            else:
                new_user = User(email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                session["user_id"] = new_user.id
                return redirect(url_for("dashboard"))
        
    return render_template("index.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("auth.index"))