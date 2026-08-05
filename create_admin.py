from werkzeug.security import generate_password_hash

from models.model import db, User

def create_admin_if_not_created():

    admin = User.query.filter_by(role="Admin").first()

    if admin:
        print("Admin already exists")

    else:
        admin = User(
            username="akzayan8",
            email = "akzayan@gmail.com",
            password_hash = generate_password_hash("akzayan8"),
            f_name="Zayan",
            l_name = "A K",
            phone=None,
            role = "Admin",
            status="Approved",
            active=True
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin Created Successfully")