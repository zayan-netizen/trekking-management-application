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
from datetime import datetime
from sqlalchemy import or_

#Initialized a Flask application and tells the whole application to run w.r.t the content of the instance folder or db files.
app = Flask(__name__, instance_relative_config=True)

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
        return render_template("reg_log/register.html")
    
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
        return render_template("reg_log/register.html", username=username, email=email, first_name=first_name, phone=phone, last_name=last_name, role=role, errors=errors)
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
                return render_template("reg_log/register.html", username=username, email=email, first_name=first_name, phone=phone, last_name=last_name, role=role, errors=errors, experience=experience, specialization=specialization, qualification=qualification)

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

        if user.role == "Trekker":
            user.user_id = f"U{user.id:03d}"
        elif user.role == "Trek Staff":
            user.user_id = f"S{user.id:03d}"

        db.session.commit()
            
        return redirect(url_for('login'))

'''Authentication'''
#Login (Staff and User)
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("reg_log/login.html")
    
    username = request.form["username"]
    password = request.form["password"]

    requested_user = User.query.filter((User.username==username) | (User.email==username)).first()

    if not requested_user:
        error = f"{username} not registered, Please register."
        return render_template("reg_log/login.html", error=error)

    if requested_user.role == "Admin":
            error = "Admin cannot login from this page!!!!!!!"
            return render_template("reg_log/login.html", username=username, error=error)

    if requested_user:
        password_valid = check_password_hash(requested_user.password_hash, password)

    if not password_valid:
        error = f"Incorrect Password"
        return render_template("reg_log/login.html", username=username, error=error)

    if requested_user and password_valid:        
        if not requested_user.active and requested_user.role == "Trekker":
            error = "You have been banned from the application, please contact customer care"
            return render_template("reg_log/login.html", username=username, error=error)
        
        if requested_user.status == "Pending" and requested_user.role == "Trek Staff":
            error = "Pending, you account is still being verified."
            return render_template("reg_log/login.html", username=username, error=error)
        
        if requested_user.status == "Rejected" and requested_user.role == "Trek Staff":
            error = "Your application has been rejected."
            return render_template("reg_log/login.html", username=username, error=error)

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
        return render_template("reg_log/login_admin.html")
    
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
            return render_template("reg_log/login_admin.html", username=username, error=error)
    else:
        error = f"{username} is not a admin, please sign in from the user's login page."
        return render_template("reg_log/login_admin.html", error=error)

''' Admin Dashboards ''' 

#Render Admin Page
@app.route("/admin_dashboard", methods=["GET", "POST"])
@roles_required("Admin")
def admin_dashboard():
    user = db.session.get(User, session["user_id"])
    users = User.query.filter_by(role="Trekker", status="Approved").all()
    users_count = len(users)
    staffs = User.query.filter_by(role="Trek Staff", status="Approved").all()
    staff_count = len(staffs)
    bookings = Booking.query.all()
    total_bookings = len(bookings)
    treks = Trek.query.all()
    trek_count = len(treks)
    bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(4).all()   
    return render_template("admin/admin_dashboard.html", user=user, users_count=users_count, staff_count=staff_count, total_bookings=total_bookings, bookings=bookings, trek_count=trek_count)

# Render Manage Users Page
@app.route("/manage_users", methods=["GET", "POST"])
def manage_users():
    user = db.session.get(User, session["user_id"])

    users = User.query.filter_by(role="Trekker").all()

    return render_template("admin/manage_users.html", users=users, user=user)

#Activates the blacklist user button
@app.route("/blacklist_user/<int:user_id>", methods=["POST"])
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    user.active = False
    db.session.commit()
    flash("User has been blacklisted successfully.!", 'success')
    return redirect(url_for('manage_users'))

#Unblacklist a user.
@app.route("/unblacklist_user/<int:user_id>", methods=["POST"])
def unblacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    user.active = True
    db.session.commit()
    flash("User has been unblacklisted successfully.!", 'success')
    return redirect(url_for('manage_users'))

#View users Profile
@app.route("/view_user/<int:user_id>", methods=["GET"])
def view_user(user_id):
    curr_user = User.query.get_or_404(user_id)
    user = db.session.get(User, session["user_id"])
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return render_template("admin/view_user.html", user=user, curr_user=curr_user, bookings=bookings)

#Renders Staffs Approved Page
@app.route("/manage_staff_approved", methods=["GET"])
def manage_staff_approved():
    user = db.session.get(User, session["user_id"])
    staffs = User.query.filter_by(role="Trek Staff", status="Approved").all()
    pending = User.query.filter_by(role="Trek Staff", status="Pending").count()
    approved = User.query.filter_by(role="Trek Staff", status="Approved").count()
    blacklisted = User.query.filter_by(role="Trek Staff", status="Blacklisted").count()
    return render_template("admin/manage_staff_approved.html", staffs=staffs, user=user, pending=pending, approved=approved, blacklisted=blacklisted)

#Renders Staffs Pending Page
@app.route("/manage_staff_pending", methods=["GET"])
def manage_staff_pending():
    user = db.session.get(User, session["user_id"])
    staffs = User.query.filter_by(role="Trek Staff", status="Pending").all()
    pending = User.query.filter_by(role="Trek Staff", status="Pending").count()
    approved = User.query.filter_by(role="Trek Staff", status="Approved").count()
    blacklisted = User.query.filter_by(role="Trek Staff", status="Blacklisted").count()
    return render_template("admin/manage_staff_pending.html", staffs=staffs, user=user, pending=pending, approved=approved, blacklisted=blacklisted)

#Render Staffs Blacklisted Page
@app.route("/manage_staff_blacklisted", methods=["GET"])
def manage_staff_blacklisted():
    user = db.session.get(User, session["user_id"])
    staffs = User.query.filter_by(role="Trek Staff", status="Blacklisted").all()
    pending = User.query.filter_by(role="Trek Staff", status="Pending").count()
    approved = User.query.filter_by(role="Trek Staff", status="Approved").count()
    blacklisted = User.query.filter_by(role="Trek Staff", status="Blacklisted").count()
    return render_template("admin/manage_staff_blacklisted.html", staffs=staffs, user=user, pending=pending, approved=approved, blacklisted=blacklisted)

#Approve Staff
@app.route("/approve_staff/<int:staff_id>", methods=["POST"])
def approve_staff(staff_id):
    user = User.query.get_or_404(staff_id)
    user.status = "Approved"
    user.active = True
    db.session.commit()
    return redirect(url_for('manage_staff_pending'))

#BlackList Staff
@app.route("/blacklist_staff/<int:staff_id>", methods=["POST"])
def blacklist_staff(staff_id):
    user = User.query.get_or_404(staff_id)
    user.status = "Blacklisted"
    user.active = False
    db.session.commit()
    return redirect(url_for('manage_staff_pending'))

#To view a staffs profile.
@app.route("/view_staff/<int:staff_id>", methods=["GET"])
def view_staff(staff_id):
    staff = User.query.get_or_404(staff_id)
    user = db.session.get(User, session["user_id"])
    return render_template("admin/view_staff.html", user=user, staff=staff)

#Renders all the treks, and to edit it.
@app.route("/add_edit_treks", methods=["POST", "GET"])
def add_edit_treks():
    user = db.session.get(User, session["user_id"])
    treks = Trek.query.all()
    return render_template("admin/add_edit_treks.html", user=user, treks=treks)

#Add Trek
@app.route("/add_trek", methods=["GET", "POST"])
def add_trek():
    user = db.session.get(User, session["user_id"])
    staffs = User.query.filter_by(role="Trek Staff", status="Approved").all()
    if request.method == "POST":
        trek_name = request.form["trek_name"]
        location = request.form["location"]
        difficulty = request.form["difficulty"]
        description = request.form["description"]
        total_slots = int(request.form["total_slots"])
        start_date = datetime.strptime(
                request.form["start_date"],
                "%Y-%m-%d"
                ).date()

        end_date = datetime.strptime(
                request.form["end_date"],
                "%Y-%m-%d"
                ).date()
        
        meeting_point = request.form["meeting_point"]
        price = float(request.form["price"])
        staff_id = request.form.get("staff_id")
        status = request.form.get("status")

        if not trek_name or not location or not difficulty or not description or not total_slots or not start_date or not end_date or not meeting_point or not price or not staff_id:
            error = f"All entries are mandatory"
            return render_template("admin/add_trek.html", trek=None, trek_name=trek_name, location=location, difficulty=difficulty, description=description, total_slots=total_slots, start_date=start_date, end_date=end_date, meeting_point=meeting_point, price=price, staff_id=staff_id, error=error, user=user, status=status, staffs=staffs)
        
        trek = Trek(
            trek_name=trek_name,
            location=location,
            difficulty=difficulty,
            description=description,
            total_slots=total_slots,
            available_slots=total_slots,
            start_date=start_date,
            end_date=end_date,
            meeting_point=meeting_point,
            staff_id=staff_id,
            price=price,
            status=status
        )

        db.session.add(trek)
        db.session.commit()

        return redirect(url_for('add_edit_treks'))
    
    return render_template("admin/add_trek.html", user=user, staffs=staffs, trek=None)

#View Trek
@app.route("/view_trek/<int:trek_id>", methods=["GET"])
def view_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    user = db.session.get(User, session["user_id"])
    return render_template("admin/view_trek.html", user=user, trek=trek)

#To edit a trek.
@app.route("/edit_trek/<int:trek_id>", methods=["POST", "GET"])
def edit_trek(trek_id):
    staffs = User.query.filter_by(role='Trek Staff', status='Approved').all()
    user = db.session.get(User, session["user_id"])
    trek = Trek.query.get_or_404(trek_id)

    if request.method == "POST":
        trek.trek_name = request.form["trek_name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.description = request.form["description"]
        trek.total_slots = int(request.form["total_slots"])
        trek.start_date = datetime.strptime(
            request.form["start_date"], "%Y-%m-%d"
        ).date()
        trek.end_date = datetime.strptime(
            request.form["end_date"], "%Y-%m-%d"
        ).date()
        trek.meeting_point = request.form["meeting_point"]
        trek.price = float(request.form["price"])
        trek.staff_id = request.form["staff_id"]
        trek.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("add_edit_treks"))
    
    return render_template("admin/add_trek.html", trek=trek, user=user, trek_name=trek.trek_name, location=trek.location, description=trek.description, total_slots=trek.total_slots, start_date=trek.start_date, end_date=trek.end_date, meeting_point=trek.meeting_point, price=trek.price, staff_id=trek.staff_id, staffs=staffs)

#To remove a trek.
@app.route("/remove_trek/<int:trek_id>", methods=["POST", "GET"])
def remove_trek(trek_id):
    user = db.session.get(User, session["user_id"])
    trek = Trek.query.get_or_404(trek_id)
    trek.status = "Cancelled"
    db.session.commit()
    return redirect(url_for('add_edit_treks'))

#Show all bookings
@app.route("/bookings", methods=["POST", "GET"])
def bookings():
    user = db.session.get(User, session["user_id"])
    bookings_ = Booking.query.all()
    return render_template("admin/bookings.html", user=user, bookings_=bookings_)

#View the details of a booking
@app.route("/view_booking/<int:booking_id>", methods=["GET"])
def view_booking(booking_id):
    user = db.session.get(User, session["user_id"])
    booking = Booking.query.get_or_404(booking_id)
    return render_template("admin/view_booking.html", user=user, booking=booking)

'''Staff Dashboard'''
@app.route("/staff_dashboard", methods=["POST", "GET"])
@roles_required("Trek Staff")
def staff_dashboard():

    user = db.session.get(User, session["user_id"])

    assigned_treks = Trek.query.filter_by(staff_id=user.id).all()

    users = Booking.query.join(Trek).filter(Trek.staff_id == user.id, Booking.booking_status != "Cancelled").all()

    registered_count = 0
    for trek in assigned_treks:
        if trek.status != 'Cancelled':
            booking_count = Booking.query.filter(Booking.trek_id==trek.id, Booking.booking_status != "Cancelled").count()
            registered_count += booking_count

    return render_template("staff/staff_dashboard.html", user=user, registered_count=registered_count, assigned_trek_count=len(assigned_treks), treks=assigned_treks, users=users)
    
#It shows all the treks assgined to that staff.
@app.route("/my_treks", methods=["POST", "GET"])
def my_treks():
    user = db.session.get(User, session["user_id"])

    treks = Trek.query.filter_by(staff_id=user.id).all()

    return render_template("staff/my_treks.html", user=user, treks=treks)

#It shows all the participants, to that staff, not necessary.
@app.route("/participants", methods=["POST", "GET"])
def participants():
    user = db.session.get(User, session["user_id"])

    bookings = (Booking.query.join(Trek).filter(Trek.staff_id == user.id, Booking.booking_status != "Cancelled").all())

    return render_template("staff/participants.html", user=user, bookings=bookings)

#Shows all the participants to the staff of that particular trek
@app.route("/participants_trek/<int:trek_id>", methods=["GET"])
def participants_trek(trek_id):
    user = db.session.get(User, session["user_id"])
    trek = Trek.query.filter(Trek.id==trek_id).first()
    bookings = Booking.query.filter(Booking.trek_id==trek_id, Booking.booking_status != "Cancelled").all()    
    return render_template("staff/participants_trek.html", user=user, bookings=bookings, trek=trek)

'''User Dashboard'''
@app.route("/user_dashboard", methods=["POST", "GET"])
@roles_required("Trekker")
def user_dashboard():

    user = db.session.get(User, session["user_id"])

    booking_completed = Booking.query.join(Trek).filter(Booking.booking_status != "Cancelled", Trek.status=="completed", Booking.user_id==user.id).count()
    total_bookings = Booking.query.filter(Booking.booking_status=="Success", Booking.user_id==user.id).count()
    bookings = Booking.query.join(Trek).filter(Trek.status != "Cancelled", Booking.user_id==user.id, Booking.booking_status=="Success", Trek.status != 'completed').all()

    return render_template("user/user_dashboard.html", user=user, booking_completed=booking_completed, total_bookings=total_bookings, bookings=bookings)

#Shows all available treks to the user, it also includes a search option to browse treks using trek_name, location or difficulty. 
@app.route("/browse_tasks", methods=["POST", "GET"])
def browse_tasks():
    user = db.session.get(User, session["user_id"])

    trek_name = request.args.get("trek_name", "").strip()
    location = request.args.get("location", "").strip()
    difficulty = request.args.get("difficulty", "").strip()

    query = Trek.query.filter(Trek.status == "open")

    if trek_name:
        query = query.filter(Trek.trek_name.ilike(f"%{trek_name}%"))

    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))

    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)

    treks = query.all()
    
    return render_template("user/browse_tasks.html", user=user, treks=treks)

#To book a trek, it also checks if all slots has been filled, and autoincrements available slots.
@app.route("/book/<int:trek_id>")
def book(trek_id):
    user = db.session.get(User, session["user_id"])
    booking = Booking.query.filter_by(user_id=user.id, trek_id=trek_id).first()
    trek = Trek.query.get_or_404(trek_id)

    if booking:
        error = ("Already booked for this event")
        return render_template("user/my_bookings.html", user=user, error=error)
    
    if trek.status == "Cancelled":
        error = "Trek was removed by the owner"
        return render_template("user/my_bookings.html", user=user, error=error)
    
    if trek.available_slots <= 0:
        error = ("Slots filled!")
        return render_template("user/my_bookings.html", user=user, error=error)
    
    booking = Booking(
        user_id=user.id,
        trek_id=trek_id,
        booking_status="Success"
    )

    db.session.add(booking)
    db.session.commit()
    
    booking.trek.available_slots -= 1
    
    booking.booking_number = f"B{booking.id:03d}"

    db.session.commit()

    return redirect(url_for('my_bookings'))

#Display bookings that already has been done.
@app.route("/history", methods=["POST", "GET"])
def history():
    user = db.session.get(User, session["user_id"])
    bookings = Booking.query.join(Trek).filter(Trek.status == 'completed', Booking.user_id==user.id).all()
    return render_template("user/history.html", user=user, bookings=bookings)

#View all bookings, which are not completed nor cancelled, so basically all valid bookings, which are yet to be done.
@app.route("/my_bookings", methods=["POST", "GET"])
def my_bookings():
    user = db.session.get(User, session["user_id"])
    bookings = Booking.query.join(Trek).filter(Booking.user_id==user.id, Trek.status!='completed').all()
    return render_template("user/my_bookings.html", user=user, bookings=bookings)

#Cancel Booking (User)
@app.route("/cancel_booking/<int:booking_id>", methods=["GET", "POST"])
def cancel_booking(booking_id):
    booking = Booking.query.filter(Booking.id==booking_id).first()
    if booking:
        booking.booking_status = "Cancelled"
        booking.trek.available_slots += 1
        db.session.commit()
    else:
        flash("Booking not found.")

    return redirect(url_for('my_bookings'))

#Search Admin
@app.route("/search", methods=["GET"])
def search():
    user = db.session.get(User, session["user_id"])

    query = request.args.get("search_text", "").strip()
    category = request.args.get("category", "all").strip()

    treks = []
    staffs = []
    users = []
    
    if category == "all" or category == "trek":
        treks = Trek.query.filter(
            or_(
                Trek.trek_name.ilike(f"%{query}%"),
                Trek.location.ilike(f"%{query}%")
            )
        ).all()

    if category == "all" or category == "user":
        users = User.query.filter(
            User.role=='Trekker',
            or_(
                User.f_name.ilike(f"%{query}%"),
                User.username.ilike(f"%{query}%")
            )
        ).all()

    if category == "all" or category == "staff":
        staffs = User.query.filter(
            User.role == 'Trek Staff',
            or_(
                User.user_id.ilike(f"%{query}%"),
                User.f_name.ilike(f"%{query}%")
            )
        ).all()

    return render_template("admin/search.html", user=user, treks=treks, users=users, staffs=staffs)

#Profile
@app.route("/profile", methods=["POST", "GET"])
def profile():
    user = db.session.get(User, session["user_id"])

    experience = ""
    qualification = ""
    specialization = ""
    address = ""

    if user.role == 'Trek Staff':
        experience = user.staff_profile.experience
        qualification = user.staff_profile.qualification
        specialization = user.staff_profile.specialization
        address = user.staff_profile.address

    if request.method == "POST":
        user.staff_profile.experience = request.form["experience"]
        user.staff_profile.qualification = request.form["qualification"]
        user.staff_profile.specialization = request.form["specialization"]
        user.staff_profile.address = request.form["address"]

        db.session.commit()

        return redirect(url_for('profile'))

    return render_template("profile.html", user=user, experience=experience, qualification=qualification, specialization=specialization, address=address)

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



