import random
import logging
import time
from typing import Dict

from abstract import Scheduler
from raft import TASKS_QUEUE, is_leader


class IOHeavyScheduler(Scheduler):
    SLEEP_BETWEEN_TASKS_SECONDS = 0.05

    def startup(self) -> None:
        logging.info('IOHeavyScheduler starts')

    def shutdown(self) -> None:
        logging.info('IOHeavyScheduler stops')

    @staticmethod
    def _erlang_distribution_approximation(k: float = 2, gamma: float = 2) -> float:
        return random.gammavariate(k, 1 / gamma)

    def _simulate_send_task(self, task: Dict) -> None:
        logging.debug(f'IOHeavyScheduler sends task: {task}')
        io_will_take_seconds = self._erlang_distribution_approximation() / task.get('divider', 2)
        time.sleep(io_will_take_seconds)

    def handle(self) -> None:
        if TASKS_QUEUE.empty() or not is_leader():
            time.sleep(self.SLEEP_BETWEEN_TASKS_SECONDS)
            return

        # TODO: this is blocking and needs sync of the cluster
        task = TASKS_QUEUE.get(sync=True)

        self._simulate_send_task(task)


class SchedulerFactory:
    @staticmethod
    def create_scheduler(scheduler_type: str = 'io') -> Scheduler:
        if scheduler_type == 'io':
            return IOHeavyScheduler()
