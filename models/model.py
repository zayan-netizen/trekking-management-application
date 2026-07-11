#Imports
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Initialized database
db = SQLAlchemy()

#User Table(main)
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.String,
        nullable=True,
        unique=True
    )
    
    username = db.Column(
        db.String(30),
        unique = True,
        nullable = False
    )

    email = db.Column(
        db.String(30),
        unique = True,
        nullable = False
    )

    password_hash = db.Column(
        db.String(255),
        nullable = False,
    )

    f_name = db.Column(
        db.String(20),
        nullable = False,
    )

    l_name = db.Column(
        db.String(20),
        nullable = False
    )

    phone = db.Column(
        db.String(10),
        nullable = True
    )

    role = db.Column(
        db.String(30),
        nullable = False
    )

    status = db.Column(
        db.String(20),
        nullable = False,
        default = "Pending"
    )

    active = db.Column(
        db.Boolean,
        nullable = False,
        default = True
    )

    created_at = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        nullable = False
    )

    updated_at = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        onupdate = datetime.utcnow,
        nullable = False
    )

    #Relationship with Booking table, helpfull in retreiving all the bookings.
    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True
    )

    #Relationship with Trek table, helfull in retreiving all the tasks of a staff
    staff = db.relationship(
        "Trek",
        backref="user",
        lazy=True
    )

    '''
        Relationship with staff_profile table to retreive information
        about the staff which is stored in StaffProfile
    '''
    staff_profile = db.relationship(
        "StaffProfile",
        backref="user",
        uselist = False,
        lazy=True
    )

#Treks Table
class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    trek_name = db.Column(
        db.String(50),
        nullable = False,
    )

    location = db.Column(
        db.String(255),
        nullable = False,
    )

    difficulty = db.Column(
        db.String(30),
        nullable = False
    )

    description = db.Column(
        db.Text,
        nullable = False
    )

    total_slots = db.Column(
        db.Integer,
        nullable = False
    )

    available_slots = db.Column(
        db.Integer,
        nullable = True
    )

    start_date = db.Column(
        db.Date,
        nullable = False
    )

    end_date = db.Column(
        db.Date,
        nullable = False
    )

    meeting_point = db.Column(
        db.String(255),
        nullable = False
    )

    price = db.Column(
        db.Float,
        nullable = False
    )

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable = True
    )

    status = db.Column(
        db.String,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.utcnow,
        onupdate = datetime.utcnow
    )

    image = db.Column(db.String(255), nullable=True)

    #Relationship with bookings table, for example helps in finding no. of available slots.
    bookings = db.relationship(
        "Booking",
        backref="trek",
        lazy=True
    )

#Booking table
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    booking_number = db.Column(
        db.String(20), 
        unique=True, 
        nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable = False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable = False
    )

    booking_date = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.utcnow
    )

    booking_status = db.Column(
        db.String(50),
        nullable = False
    )

    cancellation_reason = db.Column(
        db.String(100),
        nullable = True
    )

#StaffProfile table
class StaffProfile(db.Model):
    __tablename__ = "staffs"

    id = db.Column(
        db.Integer,
        unique = True,
        primary_key = True,
        autoincrement = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    experience = db.Column(
        db.String(255),
        nullable = False
    )

    qualification = db.Column(
        db.String(255),
        nullable = False
    )

    specialization = db.Column(
        db.String(255),
        nullable = False
    )

    address = db.Column(
        db.String(255),
        nullable = False,
    )

    joining_date = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        nullable = True
    )

    updated_at = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        onupdate = datetime.utcnow,
        nullable = False
    )

  

