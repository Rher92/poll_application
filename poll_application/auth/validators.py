from .selectors import get_user_by_email, get_user_by_username


class CreateAccountValidator:
    def __init__(self, username=None, email=None, password=None, valid=True):
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
