from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

# Create a SQLAlchemy database, and create a string which holds our database.db 
db = SQLAlchemy()
DB_NAME = "database.db"

# When we create our app we make a Flask object, configure our password, make our db url, and instatiate the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # Import our .views and .auth for usage now
    from .views import views
    from .auth import auth

    # We are taking our blueprints of our views and auth pages and registering them onto our app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    # Create our database
    create_database(app)

    # Create our login manager which uses our auth page and instatiate it
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # To load our user we get the ID and return the search (query) of the ID as an int
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return our app
    return app

# To create a database (by checking whether it exists (if not)) we create a new database using the app
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database')
