from secrets import token_hex

from flask import jsonify
from flask import Blueprint
from flask import request
from werkzeug.security import check_password_hash
from base64 import b64decode

from poll_application.models import User, db, Poll, Question, Answer
from .validators import CreateAccountValidator
from .services import create_user

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = (request.form.get('username')).lower()
        email = request.form.get('email')
        password = request.form.get('password')

        validation =  CreateAccountValidator(
            username,
            email,
            password
        )

        status_code = 400
        response = {'message': validation.msg}
        if validation.valid:
            response = {'message': 'Success'}
            status_code = 201
            create_user(username, email, password)

        return jsonify(response), status_code


@bp.route('/generate_token', methods=['GET'])
def generate_token():
    _error = None

    if request.method == 'GET':
        if not request.headers.get('Authorization'):
            response = {
                'message': 'in the request do not exist the Authorization param'
            }
            return jsonify(response), 400

        auth_encode = request.headers.get('Authorization').split()[1]
        auth_decode = b64decode(auth_encode).decode("utf-8").split(':')

        username = (auth_decode[0]).lower()
        password = auth_decode[1]
    
        user = User.query.filter_by(username=username).first()
    
        if not user:
            _error = 'Incorrect username'
        elif not check_password_hash(user.password, password):
            _error = 'Incorrect Password'

        if not _error:
            user.token = token_hex(16)
            
            db.session.add(user)
            db.session.commit()
            
            response = {
                'message':'Success',
                'token': user.token}
            return jsonify(response), 200

        response = {
            'message':'Failed',
            'error':_error}
        return jsonify(response), 400

     