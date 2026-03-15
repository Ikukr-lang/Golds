from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Регистрация blueprint'ов
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.tournament import tournament_bp
from routes.public import public_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(tournament_bp)
app.register_blueprint(public_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
