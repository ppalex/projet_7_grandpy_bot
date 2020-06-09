from flask import render_template
from flask import Blueprint

view = Blueprint('view', __name__)

@view.route('/')
def home():
    return render_template('home.html')


@view.route('/test')
def test():
    return "test"