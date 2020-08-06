from flask import jsonify
from flask import Blueprint

bp = Blueprint('ping', __name__, url_prefix='/ping')

@bp.route('/', methods=['GET'])
def ping():
    status_code = 200
    response = {'message': 'pong'}
    return jsonify(response), status_code