from datetime import datetime

from flask import jsonify
from flask import Blueprint
from flask import request

from poll_application.models import User, db, Poll, \
    Question, Answer, Tag
from .selectors import get_user, get_full_polls_data_by_user, \
    get_questions_by_user
from .services import save_poll, save_questions, save_tags
from .validations import validate_all_data_to_create_poll, \
    UserValidated

bp = Blueprint('poll', __name__, url_prefix='/api/poll')

@bp.route('/new/users/<username>/token/<token>/', methods=['POST'])
def create_poll(username, token):
    if request.method == 'POST':
        user = get_user(username.lower())
        obj = validate_all_data_to_create_poll(user, token, request)

        response = obj.msg
        if obj.valid:
            poll = save_poll(obj, user)
            save_questions(obj, poll)
            save_tags(obj, poll)
            response = {'message': 'Success'}

        return jsonify(response), 200            


@bp.route('/<poll_id>/answer', methods=['POST'])
def create_answer(poll_id):
    if request.method == 'POST':
        poll = Poll.query.filter_by(id=poll_id).first()
        if not poll:
            response = {
                'message': 'the poll do not exist'
            }
            return jsonify(response), 400

        if poll.close_date < datetime.now():
            response = {
                'message': 'the poll has expired'
            }
            return jsonify(response), 400            
        
        payload = request.form.to_dict()

        answer_list = []
        for question_id in payload.keys():
            answer = payload[question_id]
            qid = int(question_id)

            question = Question.query.filter_by(id=qid,poll_id=poll_id).first()
            if not question:
                response = {
                    'message' : 'the question with id:{} do not exist.'.format(qid)
                }
                return jsonify(response), 400

            if Question.query.filter_by(id=qid).first().counter == 4:
                continue

            new_answer = Answer(_answer=answer, question_id=question.id)
            answer_list.append(new_answer)
        
        for answer in answer_list:
            db.session.add(answer)
            db.session.commit()

            question = Question.query.filter_by(id=answer.question_id).first()
            counter = question.counter
            counter += 1
            question.counter = counter
            db.session.add(question)
            db.session.commit()

        response = {
            'message' : 'Success'
        }
        return jsonify(response), 200


@bp.route('all/users/<username>/token/<token>/', methods=['GET'])
def get_poll(username, token):
    if request.method == 'GET':
        username = username.lower()
        user = User.query.filter_by(username=username).first()
        _validation = validation(user, token)
        if _validation:
            return _validation

        if request.args.get('tag'):
            tag = (request.args.get('tag')).lower()
            _tag = Tag.query.filter_by(title=tag).first()

            if not _tag:
                response = {
                    'message': 'this tag are not registrated'.format(tag)}
                return jsonify(response), 400

            polls = Poll.query.filter(Poll.tags.contains(_tag)).all() 

            if not polls:
                response = {
                    'message': 'there are not polls with tag:{}'.format(tag)}
                return jsonify(response), 400           

            _polls = [{'title': poll.title, 'id': poll.id} for poll in polls]
        else:
            polls = Poll.query.filter().all()
            _polls = [{'title': poll.title, 'id': poll.id} for poll in polls]
        
        response = {'polls': _polls}
        return jsonify(response), 200


@bp.route('questions/users/<username>/token/<token>/', methods=['GET'])
def get_questions(username, token):
    if request.method == 'GET':
        username = username.lower()
        user = get_user(username)
        user_validated = UserValidated(user, token)

        status_code = 401
        response = user_validated.msg

        if user_validated.valid:
            status_code = 200
            _username = (request.args.get('user')).lower()
            response = get_questions_by_user(_username)

        return jsonify(response), status_code


@bp.route('questions_and_answers/users/<username>/token/<token>/', methods=['GET'])
def get_questions_answers(username, token):
    if request.method == 'GET':
        username = username.lower()
        user = get_user(username) 
        user_validated = UserValidated(user, token)

        status_code = 401
        response = user_validated.msg

        if user_validated.valid:
            status_code = 200
            response = get_full_polls_data_by_user(user)

        return jsonify(response), status_code
