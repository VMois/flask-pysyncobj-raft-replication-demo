import logging
import time
from typing import Dict

from abstract import Scheduler
from raft import TASKS_QUEUE, is_leader


class FifoScheduler(Scheduler):
    SLEEP_BETWEEN_TASKS_SECONDS = 0.1

    def startup(self) -> None:
        logging.info('FIFO scheduler starts')

    def shutdown(self) -> None:
        logging.info('FIFO scheduler stops')

    @staticmethod
    def _process_task(task: Dict) -> None:
        logging.info(f'Scheduler processing task: {task}')
        time.sleep(1)

    def handle(self) -> None:
        if TASKS_QUEUE.empty() or not is_leader():
            time.sleep(self.SLEEP_BETWEEN_TASKS_SECONDS)
            return

        task = TASKS_QUEUE.get(sync=True)
        self._process_task(task)


class SchedulerFactory:
    @staticmethod
    def create_scheduler(scheduler_type: str = 'fifo') -> Scheduler:
        if scheduler_type == 'fifo':
            return FifoScheduler()
