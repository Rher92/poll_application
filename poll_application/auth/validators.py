from werkzeug.security import check_password_hash
from base64 import b64decode

from .selectors import get_user_by_email, get_user_by_username


class CreateAccountValidator:
    def __init__(self, username=None, email=None, password=None, valid=True, msg=None):
        self.username = username
        self.email = email
        self.password = password
        self.valid = valid
        self.msg = 'OK'

        self._validations()

    def _validations(self):
        if not self.username:
            self.msg = 'username is required'
            self.valid = False
        elif not self.email:
            self.msg = 'Email is required'
            self.valid = False
        elif not self.password:
            self.msg = 'Password is required'
            self.valid = False                                            
        elif get_user_by_username(self.username):
            self.msg = 'already exist this username'
            self.valid = False
        elif get_user_by_email(self.email):
            self.msg = 'already exist this email'
            self.valid = False


class GenerateTokenValidator:
    def __init__(self, header, valid=True, msg=None):
        self.header = header
        self.valid = True
        self.msg = 'OK'
        self.auth_param = header.get('Authorization')
        self.user = None
        self.password = None
        self._auth_decode = None

        self._validation()

    def _validation(self):
        self._is_header_valid()

    def _is_header_valid(self):
        if not self.auth_param:
            self.valid = False
            self.msg = 'in the request do not exist the Authorization param'
        else:
            self._setup_user_and_password()
            self._is_valid_user()

    def _is_valid_user(self):
        if not self.user:
            self.msg = 'username not exist'
            self.valid = False
        else:
            self._is_valid_password()

    def _is_valid_password(self):
        if not check_password_hash(self.user.password, self.password):
            self.msg = 'passoword is not valid'
            self.valid = False

    def _setup_user_and_password(self):
        self._make_auth_param_decode()
        username = self._auth_decode[0].lower()
        password = self._auth_decode[1]

        self.user = get_user_by_username(username)
        self.password = password

    def _make_auth_param_decode(self):
        auth_encode = self.auth_param.split()[1]
        self._auth_decode = b64decode(auth_encode).decode("utf-8").split(':')
