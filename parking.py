from config import app
# from flask import Flask
# from user import blu as user_blu
from auth import setup as auth_setup
# from slot import blu as slot_blu
# app = Flask(__name__)
# app.register_blueprint(user_blu)
auth_setup(app)
# app.register_blueprint(slot_blu)


@app.route('/')
def hello():
    return 'hello world!!'


if __name__ == '__main__':
    app.run(debug=True)
