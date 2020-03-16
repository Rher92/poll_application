from secrets import token_hex

from flask import jsonify
from flask import Blueprint
from flask import request
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from base64 import b64decode

from models import User, db, Poll, Question, Answer

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    _error = []

    if request.method == 'POST':
        username = (request.form.get('username')).lower()
        email = request.form.get('email')
        password = request.form.get('password')

        # data form Validation
        if not username:
            _error.append('Username is required.')
        if not email:
            _error.append('Email is required.')
        if not password:
            _error.append('Password is required.')

        # validation if the user, username and email are registrated
        if User.query.filter_by(username=username, email=email).first():
            _error.append('User {} is already registered.'.format(username))
        elif User.query.filter_by(username=username).first():
            _error.append('Username {} is already registered.'.format(username))
        elif User.query.filter_by(email=email).first():
            _error.append('email {} is already registered.'.format(email))            

        if _error:
            response = {
                'message': 'Failed',
                'error': _error}
            return jsonify(response), 400

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()     

        response = {
            'message': 'Success'}
        return jsonify(response), 200        


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

     