from flask import Flask
from .views import view
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.register_blueprint(view)


if __name__ == '__main__':
    app.run(debug=True)
    