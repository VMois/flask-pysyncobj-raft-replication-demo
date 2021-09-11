import logging
import signal
from flask import Flask, request, jsonify
from pysyncobj import SyncObj
from typing import List

from scheduler import TASKS_QUEUE, SchedulerFactory


def create_app(raft_host: str, partners: List[str]):
    # for development purposes only
    logging.basicConfig(level=logging.DEBUG)

    app = Flask(__name__)
    sync_obj = SyncObj(raft_host, partners, consumers=[TASKS_QUEUE])
    sync_obj.waitBinded()
    sync_obj.waitReady()

    @app.route('/task', methods=['POST'])
    def submit_task():
        task = request.json
        logging.debug(f'Received task via POST: {task}')
        TASKS_QUEUE.put(task, sync=True)
        return jsonify({'success': 'OK'})

    @app.route('/status/raft', methods=['GET'])
    def raft_status():
        print(sync_obj.getStatus())
        return jsonify({'success': 'OK'})

    scheduler = SchedulerFactory.create_scheduler()
    scheduler.start()

    def sigint_handler(signum, frame):
        scheduler.stop()
        sync_obj.destroy()
        exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    return app
