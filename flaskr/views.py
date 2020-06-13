from flask import render_template, jsonify, request
from flask import Blueprint

from flaskr.models import GoogleApi

view = Blueprint('view', __name__)

@view.route('/')
def index():
    return render_template('index.html')


@view.route('/form', methods=["POST"])
def form():
    data = request.form["user_text"]
    
    # google_api = GoogleApi()    
    # google_api_response = google_api.send_request(data)
    google_api_response = "null"
    return jsonify(google_api_response)


