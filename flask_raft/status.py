import json

from flask import Blueprint, current_app

from raft import get_status

bp = Blueprint('status', __name__, url_prefix='/status')


@bp.route('/raft', methods=['GET'])
def raft_status():
    return current_app.response_class(
        json.dumps(get_status(), indent=4, sort_keys=True),
        mimetype='application/json')
