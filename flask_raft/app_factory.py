import logging
import signal
from typing import List

from flask import Flask

import status
import tasks
from raft import create_sync_obj, get_sync_obj
from scheduler import SchedulerFactory


def create_app(raft_host: str, partners: List[str]):
    # for development purposes only
    logging.basicConfig(level=logging.DEBUG)

    app = Flask(__name__)

    create_sync_obj(raft_host, partners)
    sync_obj = get_sync_obj()

    app.register_blueprint(tasks.bp)
    app.register_blueprint(status.bp)

    scheduler = SchedulerFactory.create_scheduler()
    scheduler.start()

    def sigint_handler(signum, frame):
        scheduler.stop()
        sync_obj.destroy()
        exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    return app
