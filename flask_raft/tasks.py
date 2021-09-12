import logging
import uuid

from flask import Blueprint, jsonify, request

from raft import get_distributed_queue, is_leader, get_status

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/', methods=['POST'])
def submit_task():
    if not is_leader():
        leader_address = get_status()['leader']
        return jsonify({
            'status': 'NOT_LEADER',
            'leader': leader_address,
        }), 400

    task = request.json
    logging.debug(f'Received task: {task}')

    task_id = str(uuid.uuid4())

    task['id'] = task_id

    # TODO: made submitting of tasks more error prone
    queue = get_distributed_queue()
    queue.put(task, sync=True)

    return jsonify({
        'status': 'SUBMITTED',
        'id': task_id,
    })
