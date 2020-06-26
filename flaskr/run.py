from flask import Flask
from flaskr.views import view

import configuration.config as conf

conf.load('./configuration/config.yml')

app = Flask(__name__)
app.register_blueprint(view)

app.secret_key = conf.value['SECRET_KEY']
app.debug = conf.value['DEBUG']


def main():
    app.run()


if __name__ == '__main__':
    """Main method to launch the app."""
    main()
