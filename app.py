from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db
from models.user import User
from config import Config
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    csrf = CSRFProtect(app)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from routes.auth import auth_bp
    from routes.post import post_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
