from flask import Blueprint

post_bp = Blueprint('post', __name__, template_folder='templates/post')

from post import routes
