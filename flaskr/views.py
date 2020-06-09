from flask import render_template
from flask import Blueprint

view = Blueprint('view', __name__)

@view.route('/')
def index():
    return render_template('index.html')


@view.route('/test')
def test():
    return "test"