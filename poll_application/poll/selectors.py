from poll_application.models import User, db, Poll, \
    Question, Answer, Tag


def get_user(username):
    return User.query.filter_by(username=username).first()


def get_all_users():
    return User.query.filter().all()


def get_tag(tag):
    return Tag.query.filter_by(title=tag).first()


def get_poll_with_tag(tag):
    return Poll.query.filter(Poll.tags.contains(tag)).all() 


def get_all_polls():
    return Poll.query.filter().all()


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


def get_questions_by_polls(polls):
    _polls = []

    for _poll in polls:
        questions = []
        questions += [{'id': question.id, 'title':question._question} for question in _poll.questions]
        poll_aux = {'id': _poll.id, 'title': _poll.title, 'questions': questions}
        _polls.append(poll_aux)
    _return = {'polls': _polls}

    return _return


def get_questions_by_user(username):
    if username == 'all':
        user = get_all_users()
    else:
        user = get_user(username)

    _return = 'User not exist'
    if user:
        questions = []

        if user.__class__ is list:
            for _user in user:
                questions_for_user = get_questions_by_polls(_user.poll)
                questions.append({
                    _user.username : questions_for_user
                })
        else:
            questions_for_user = get_questions_by_polls(user.poll)
            questions.append({
                user.username : questions_for_user
            })
        _return = questions

    return _return


def _get_polls_through_tag(tag):
    _tag = get_tag(tag)
    _return = f'this tag: {tag} are not registrated'
    if _tag:
        polls = Poll.query.filter(Poll.tags.contains(_tag)).all() 
        _return = [{'title': poll.title, 'id': poll.id} for poll in polls] 
    return _return   


def _get_all_polls_modify():
    polls = get_all_polls()
    return [{'title': poll.title, 'id': poll.id} for poll in polls]


def get_polls(tag):    
    if tag:
        _polls = _get_polls_through_tag(tag.lower())
    else:
        _polls = _get_all_polls_modify() 
    
    return  {'polls': _polls}


def get_poll_by_id(poll_id):
    return Poll.query.filter_by(id=poll_id).first()


def get_questions_by_id_and_poll_id(qid, poll_id):
    return Question.query.filter_by(id=qid, poll_id=poll_id).first()


