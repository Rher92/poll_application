from secrets import token_hex

from flask import jsonify
from flask import Blueprint
from flask import request
from werkzeug.security import check_password_hash
from base64 import b64decode

from .validators import CreateAccountValidator, GenerateTokenValidator
from .services import create_user, save_user

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


@bp.route('/generate_token', methods=['PUT'])
def generate_token():
    if request.method == 'PUT':
        validation = GenerateTokenValidator(request.headers)

        status_code = 400
        response = {'message': validation.msg}
        if validation.valid:
            user = validation.user
            user.token = token_hex(16)
            save_user(user)
            
            status_code = 200
            response = {
                'message':'Success',
                'token': user.token}
        
        return jsonify(response), status_code

     