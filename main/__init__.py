from flask import Flask
from main.controllers import blueprints_ctrl

app = Flask(__name__)


for bp in blueprints_ctrl:
    app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=True)
