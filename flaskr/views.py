from flask import render_template, jsonify, request
from flask import Blueprint

from flaskr.utils import treat_data_from_google_api

view = Blueprint('view', __name__)


@view.route('/')
def index():
    return render_template('index.html')


@view.route('/form', methods=["POST"])
def form():
    data = request.form["user_text"]

    response = treat_data_from_google_api(data)

    return jsonify(response)
