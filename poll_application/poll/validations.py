from datetime import datetime

def validate_all_data_to_create_poll(user, token, request):
    poll_title = (request.form.get('title')).capitalize()
    question_titles = request.form.getlist('questions')
    tag_titles = request.form.getlist('tags')
    _close_date =  request.form.get('close_date')
    close_date = datetime.fromisoformat(_close_date)

    user_validated = UserValidated(user, token)
    close_date_validated = DateCloseValidated(close_date)    
    poll_title_validated = PollTitlesValidated(user, poll_title)
    question_titles_validated = ValidatedAux(question_titles)
    tag_titles_validated = ValidatedAux(tag_titles)

    _return = None
    if not user_validated.valid:
        _return = user_validated
    elif not close_date_validated.valid:
        _return = close_date_validated   
    elif not poll_title_validated.valid:
        _return = poll_title_validated
    elif not question_titles_validated.valid:
        _return = question_titles_validated
    elif not tag_titles_validated.valid:
        _return = tag_titles_validated

    if not _return:
        _return = Data(
            poll_title,
            close_date,
            tag_titles,
            question_titles
        )

    return _return


class Data:

    def __init__(self, title, date, tags, questions):
        self.title = title
        self.close_date = date
        self.tags = tags
        self.questions = questions
        self.valid = True
        self.msg = 'OK'


class ValidatedAux:
    
    def __init__(self, data=None, error_msg=None, valid=True):
        self.data = data
        self.msg = 'OK'
        self.valid = valid

        self.is_none()

    def __str__(self):
        return f'{self.validated} - {self.msg}'

    def is_none(self):
        if not self.data:
            self.valid = False
            self.error = self.error_msg


class UserValidated(ValidatedAux):

    def __init__(self, user, token, valid=True):
        self.user = user
        self.msg = 'OK'
        self.valid = valid
        self.token = token

        self.is_token_valid()
        self.is_user_exist()

    def is_user_exist(self):
        if not self.user:
            self.valid = False
            self.msg = 'user not exist'

    def is_token_valid(self):
        if self.user.token != self.token:
            self.valid = False
            self.msg = 'token not valid'


class DateCloseValidated(ValidatedAux):
    def __init__(self, data, error_msg=None, valid=True):
        super().__init__(data, error_msg, valid)

        if self.valid:
            self.is_time_valid()
    
    def is_time_valid(self):
        if self.data < datetime.now():
            self.msg = 'the date close must be greater than current time'


class PollTitlesValidated(ValidatedAux):
    def __init__(self, user, data, error_msg=None, valid=True):
        super().__init__(data, error_msg, valid)
        self.user = user

        if self.valid:
            self.is_title_valid()
    
    def is_title_valid(self):
        polls = self.user.poll
        poll_titles = [_poll.title for _poll in polls]

        if self.data in poll_titles:
           self.msg = f'this poll {self.data} already exist by the user {self.user}'

