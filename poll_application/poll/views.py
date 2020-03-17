from datetime import datetime

from flask import jsonify
from flask import Blueprint
from flask import request

from models import User, db, Poll, \
    Question, Answer, Tag

bp = Blueprint('poll', __name__, url_prefix='/api/poll')

@bp.route('/new/users/<username>/token/<token>/', methods=['POST'])
def create_poll(username, token):
    if request.method == 'POST':
        username = username.lower()        
        user = User.query.filter_by(username=username).first()
        _validation = validation(user, token)
        if _validation:
            return _validation

        poll_title = (request.form.get('title')).capitalize()
        question_titles = request.form.getlist('questions')
        tag_titles = request.form.getlist('tags')
        close_date =  request.form.get('close_date')

        if not (poll_title or question_titles or tag_titles or close_date):
            response = {
                'message': 'the request has not all data'
            }
            return jsonify(response), 400
        
        close_date = datetime.fromisoformat(close_date)
        
        if close_date < datetime.now():
            response = {
                'message': 'the date close must be greater than current time'
            }
            return jsonify(response), 400            

        poll_titles = [_poll.title for _poll in user.poll]

        if poll_title in poll_titles:
            response = {
                'message': 'this poll {} already exist for the user {}'.format(poll_title, username)
            }
            return jsonify(response), 400
 
        new_poll = Poll(
            title=poll_title,
            user_id=user.id,
            close_date=close_date)

        db.session.add(new_poll)
        db.session.commit()

        if not question_titles:
            response = {
                'message': 'this poll has no questions'
            }
            return jsonify(response), 400
            
        for _question in question_titles:
            question = Question(
                question=_question.capitalize(),
                poll_id=new_poll.id)

            db.session.add(question)
            db.session.commit()        

        if tag_titles:
            for _tag in tag_titles:
                _tag.lower()
                tag = Tag.query.filter_by(title=_tag).first()
                if not tag:
                    tag = Tag(title=_tag)
                    db.session.add(tag)
                    db.session.commit()
                
                new_poll.tags.append(tag)
            db.session.add(new_poll)
            db.session.commit()

        response = {
            'message': 'Success'
        }
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
        user = User.query.filter_by(username=username).first()        
        _validation = validation(user, token)
        if _validation:
            return _validation

        _user = (request.args.get('user')).lower()

        if _user == 'all':
            user = User.query.filter().all()
        else:
            user = User.query.filter_by(username=_user)

        if not user:
            response = {
                'message': 'the user: {} do not exist'.format(_user)
            }
            return jsonify(response), 400

        user_list = []
        for _user in user:
            questions_user = _user.get_questions()
            
            user_list.append({
                _user.username : questions_user
            })
        
        response = {'users': user_list}
        return jsonify(response), 200


@bp.route('questions_and_answers/users/<username>/token/<token>/', methods=['GET'])
def get_questions_answers(username, token):
    if request.method == 'GET':
        username = username.lower()
        user = User.query.filter_by(username=username).first()        
        _validation = validation(user, token)
        if _validation:
            return _validation

        _user = (request.args.get('user')).lower()
        user = User.query.filter_by(username=_user).first()

        if not user:
            response = {
                'message': 'the user: {} do not exist'.format(_user)
            }
            return jsonify(response), 400

        return jsonify(user.get_full_data()), 200


def validation(user, token):
    _return = None
    
    if not user:
        response = {
            'message': 'user do not exist'}
        _return = jsonify(response), 400
        return _return

    if token != user.token:
        response = {
            'message': 'Invalid token'}
        _return = jsonify(response), 400

    return _return