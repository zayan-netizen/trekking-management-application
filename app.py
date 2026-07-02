'''
    Main file into which all the logics the 
    application goes into.
'''

#Imports
from flask import Flask
from models.model import db
from create_admin import create_admin_is_not_created

#Initialized a Flask application
app = Flask(__name__)

#Configuarations for the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trek.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Initialise database with the app configuarations.
db.init_app(app)

#app.app_context connect this piece of code with application
with app.app_context():
    #Initialize Database
    db.create_all()
    #Create Admin
    create_admin_is_not_created()
    print(f"Database initialised successfully")

#Runs application
if __name__ == "__main__":
    app.run(debug=True)



