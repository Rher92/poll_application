from poll_application.models import User, db, Poll, \
    Question, Answer, Tag


def get_user(username):
    return User.query.filter_by(username=username).first()


def get_full_polls_data_by_user(user):
    _data = []
    polls_lyst = []
    for poll in user.poll:
        questions_lyst = []

        for question in poll.questions:
            answers_lyst = [{'answer': answer._answer, 'id': answer.id} for answer in question.answer]
            aux_lyst = {'title': question._question, \
                        'id': question.id, \
                        'answers' : answers_lyst}
            questions_lyst.append(aux_lyst)

        poll_aux = {'id': poll.id, \
                    'questions': questions_lyst, \
                    'title': poll.title}
        polls_lyst.append(poll_aux)

    _data.append({'polls': polls_lyst})
    _return = {'user':user.username, 'data':_data}

    return _return