from datetime import datetime

from flask import jsonify
from flask import Blueprint
from flask import request

from poll_application.models import User, db, Poll, \
    Question, Answer, Tag
from .selectors import get_user, get_full_polls_data_by_user, \
    get_questions_by_user, get_polls, get_poll_by_id, \
    get_questions_by_id_and_poll_id
from .services import save_poll, save_questions, save_tags, \
    save_messages
from .validators import validate_all_data_to_create_poll, \
    UserValidated, PollValidation, QuestionValidation

bp = Blueprint('poll', __name__, url_prefix='/api/poll')

@bp.route('/new/users/<username>/token/<token>/', methods=['POST'])
def create_poll(username, token):
    if request.method == 'POST':
        user = get_user(username.lower())
        obj = validate_all_data_to_create_poll(user, token, request)

        status_code = 400
        response = obj.msg
        if obj.valid:
            status_code = 200
            poll = save_poll(obj, user)
            save_questions(obj, poll)
            save_tags(obj, poll)
            response = {'message': 'Success'}

        return jsonify(response), status_code


@bp.route('/<poll_id>/answer', methods=['POST'])
def create_answer(poll_id):
    if request.method == 'POST':
        poll = get_poll_by_id(poll_id)
        poll_validation = PollValidation(poll)
        
        status_code = 400
        response = poll_validation.msg
        if poll_validation.valid:
            payload = request.form.to_dict()

            answers = []
            _save_message = True
            for question_id in payload.keys():
                answer = payload[question_id]
                qid = int(question_id)
                poll_id = int(poll_id)
                question = get_questions_by_id_and_poll_id(qid=qid, poll_id=poll_id)
                question_valid = QuestionValidation(question)

                if not question_valid.valid:
                    _save_message = False
                    response = question_valid.msg
                    break

                if not question_valid.has_max_answer:
                    new_answer = Answer(_answer=answer, question_id=question.id)
                    answers.append(new_answer)

            if _save_message:
                status_code = 200
                response = {'message': 'Success'}
                save_messages(answers)

        return jsonify(response), status_code


@bp.route('all/users/<username>/token/<token>/', methods=['GET'])
def get_poll(username, token):
    if request.method == 'GET':
        username = username.lower()
        user = get_user(username)
        user_validated = UserValidated(user, token)

        status_code = 401
        response = user_validated.msg

        if user_validated.valid:
            status_code = 200
            tag = request.args.get('tag')
            response = get_polls(tag)

        return jsonify(response), status_code


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
