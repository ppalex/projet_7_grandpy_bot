from flask import render_template, jsonify, request
from flask import Blueprint

from flaskr.utils import treat_data_from_user

view = Blueprint('view', __name__)


@view.route('/')
def index():
    """This function displays the index template.

    Returns:
        [Template]: This page is the main page of the app.
    """
    return render_template('index.html')


@view.route('/form', methods=["POST"])
def form():
    """This function get the data from the question-form.

    Returns:
        [JSON]: The response contains the lat, long, url, and the
                different messages.
    """
    data = request.form["user_text"]
    response = treat_data_from_user(data)

    return jsonify(response)
