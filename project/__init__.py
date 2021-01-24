from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from firebase import firebase

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
firebase = firebase.FirebaseApplication('https://supershop-53157-default-rtdb.firebaseio.com/', None)

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_BINDS'] = {
            'user': 'sqlite:///user.sqlite',
            }    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
