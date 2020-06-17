from flask import Flask
from flaskr.views import view

import configuration.config as conf

conf.load('./configuration/config.yml')

app = Flask(__name__)
app.register_blueprint(view)

app.secret_key = conf.value['SECRET_KEY']
app.debug = conf.value['DEBUG']

if __name__ == '__main__':    
    
    app.run()
    