'''
    Main file into which all the logics the 
    application goes into.
'''

#Imports
from flask import Flask, redirect, url_for, render_template, request, flash, session
from models.model import db, User, Trek, Booking, StaffProfile
from create_admin import create_admin_is_not_created
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

#Initialized a Flask application
app = Flask(__name__)

#Configuarations for the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trek.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "133ffffffffffbfbhs"

#Initialise database with the app configuarations.
db.init_app(app)

#app.app_context connect this piece of code with application
with app.app_context():
    #Initialize Database
    db.create_all()
    #Create Admin
    create_admin_is_not_created()
    print(f"Database initialised successfully")

#Make the endpoint available to each function at all times.
@app.context_processor
def current_page():
    return dict(current_page=request.endpoint)

'''Authorisation'''
def roles_required(*roles):
    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            if session.get("role") not in roles:
                return redirect(url_for("access_denied"))

            return f(*args, **kwargs)

        return wrapper

    return decorator
    
#Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    errors = []

    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form["username"]

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        errors.append("Username already exists")

    email = request.form["email"]
    existing_email = User.query.filter_by(email=email).first()

    if existing_email:
        errors.append("This email is already registered")

    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        errors.append("Passwords do not match")

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    phone = request.form["phone"]
    role = request.form["role"]

    if errors:
        return render_template("register.html", username=username, email=email, first_name=first_name, phone=phone, last_name=last_name, role=role, errors=errors)
    else:
        flash(f"Registration successfull, redirecting to login page........", "success")
        if role == "Trekker":
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                f_name=first_name,
                l_name=last_name,
                phone=phone,
                role=role,
                status="Approved",
                active=True
                )
        else:
            experience = request.form["experience"]
            qualification = request.form["qualification"]
            specialization = request.form["specialization"]
            address = request.form["address"]

            if not experience or (not qualification) or (not specialization) or (not address):
                errors.append(f"All fields are required")
                return render_template("register.html", username=username, email=email, first_name=first_name, phone=phone, last_name=last_name, role=role, errors=errors, experience=experience, specialization=specialization, qualification=qualification)

            flash("Registration successfull, please wait till the admin approves to login !")
            user = User(username=username,
                email=email,
                password_hash=generate_password_hash(password),
                f_name=first_name,
                l_name=last_name,
                phone=phone,
                role=role,
                status="Pending",
                active=False
                )
            
            staff = StaffProfile(experience=experience,
                    qualification=qualification,
                    specialization=specialization,
                    address=address
                    )
            
            user.staff_profile = staff
            
        db.session.add(user)
        db.session.commit()
            
        return redirect(url_for('login'))

'''Authentication'''
#Login (Staff and User)
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form["username"]
    password = request.form["password"]

    requested_user = User.query.filter((User.username==username) | (User.email==username)).first()

    if not requested_user:
        error = f"{username} not registered, Please register."
        return render_template("login.html", error=error)

    if requested_user.role == "Admin":
            error = "Admin cannot login from this page!!!!!!!"
            return render_template("login.html", username=username, error=error)

    if requested_user:
        password_valid = check_password_hash(requested_user.password_hash, password)

    if not password_valid:
        error = f"Incorrect Password"
        return render_template("login.html", username=username, error=error)

    if requested_user and password_valid:        
        if not requested_user.active and requested_user.role == "Trekker":
            error = "You have been banned from the application, please contact customer care"
            return render_template("login.html", username=username, error=error)
        
        if requested_user.status == "Pending" and requested_user.role == "Trek Staff":
            error = "Pending, you account is still being verified."
            return render_template("login.html", username=username, error=error)
        
        if requested_user.status == "Rejected" and requested_user.role == "Trek Staff":
            error = "Your application has been rejected."
            return render_template("login.html", username=username, error=error)

        flash("Login successfull, redirecting now.....", "success")

        session["user_id"] = requested_user.id
        session["role"] = requested_user.role

        if requested_user.role == "Trekker":
            return redirect(url_for('user_dashboard'))
        elif requested_user.role == "Trek Staff":
            return redirect(url_for('staff_dashboard'))
        
#Login - Admin
@app.route("/login-admin", methods=["GET", "POST"])
def login_admin():

    if request.method == "GET":
        return render_template("login_admin.html")
    
    username = request.form["username"]
    password = request.form["password"]

    requested_user = User.query.filter_by(username=username).first()

    if requested_user and requested_user.role == "Admin":
        if check_password_hash(requested_user.password_hash, password):
            session["user_id"] = requested_user.id
            session["role"] = requested_user.role
            return redirect(url_for('admin_dashboard'))
        else:
            error = f"Incorrect Password"
            return render_template("login_admin.html", username=username, error=error)
    else:
        error = f"{username} is not a admin, please sign in from the user's login page."
        return render_template("login_admin.html", error=error)

''' Admin Dashboards '''      
@app.route("/admin_dashboard", methods=["GET", "POST"])
@roles_required("Admin")
def admin_dashboard():
    user = db.session.get(User, session["user_id"])

    return render_template("base.html", user=user)

'''Staff Dashboard'''
@app.route("/staff_dashboard", methods=["POST", "GET"])
@roles_required("Trek Staff")
def staff_dashboard():

    user = db.session.get(User, session["user_id"])

    if request.method == "GET":
        return render_template("staff_dashboard.html", user=user)
    
'''User Dashboard'''
@app.route("/user_dashboard", methods=["POST", "GET"])
@roles_required("Trekker")
def user_dashboard():

    user = db.session.get(User, session["user_id"])

    if request.method == "GET":
        return render_template("user_dashboard.html", user=user)

#Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
 
#Access Denied Page
@app.route("/access_denied.html", methods=["GET"])
def access_denied():
    if request.method == "GET":
        return render_template("access_denied.html")
#Runs application
if __name__ == "__main__":
    app.run(debug=True)



