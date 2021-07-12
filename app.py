from flask import Flask, request, jsonify
import json
import requests
import random


import config
import db
import mailag


app = Flask(__name__)


def generate_code():
    return random.randint(100000, 999999)


@app.route("/code/send/", methods=["POST"])
def set_email():
    """Send code to new email"""
    j_request = request.json
    r = db.find_user(j_request['name'])
    code = generate_code()
    if r == 'this profile isnt in database':
        db.add_user(j_request['name'], j_request['email'], code)
        print(mailag.send_message(j_request['email'], "Привет! Это бот авторизации. Код подтверждения авторизации: " + str(code)))
    elif r <= 15:
        db.change_email(j_request['name'], j_request['email'], code)
        print(mailag.send_message(j_request['email'], "Привет! Это бот авторизации. Код подтверждения авторизации: " + str(code)))
    else:
        return json.dumps({'success': 'to many attempts'}), 420, {'ContentType': 'application/json'}
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/code/resend/", methods=["POST"])
def resend_code():
    """Resend code to old email"""
    j_request = request.json
    r = db.find_user(j_request['name'])
    code = generate_code()
    if r <= 15:
        db.change_code(j_request['name'], code)
        email = db.get_email(j_request['name'])
        mailag.send_message(email, "Привет! Это бот авторизации. Код подтверждения авторизации: " + str(code))
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': 'to many attempts'}), 420, {'ContentType': 'application/json'}
    return jsonify(db.get_all())


@app.route("/code/get/", methods=["GET"])
def get_code():
    j_request = request.json
    return jsonify({'code': str(db.get_code(j_request['name']))})


if __name__ == "__main__":
    app.run(debug=True)
