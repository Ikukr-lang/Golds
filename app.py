from flask import Flask
from config import Config
from models import db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.tournament import tournament_bp
from routes.public import public_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(tournament_bp)
app.register_blueprint(public_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
