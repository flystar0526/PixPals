from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from models import db, User
from config import Config
from auth import auth_bp
from user import user_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = '請先登入以訪問此頁面'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# 註冊 Blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
