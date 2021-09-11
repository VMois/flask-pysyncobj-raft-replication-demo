import logging
import threading
import time
from abc import abstractmethod, ABC
from typing import Dict

from pysyncobj.batteries import ReplQueue

TASKS_QUEUE = ReplQueue(maxsize=10000)


class Scheduler(threading.Thread, ABC):
    def __init__(self):
        super(Scheduler, self).__init__()
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def _stopped(self) -> bool:
        return self._stop_event.is_set()

    @abstractmethod
    def startup(self) -> None:
        """
        Method that is called before the scheduler starts.
        Init all necessary resources here.
        :return: None
        """
        raise NotImplemented

    @abstractmethod
    def shutdown(self) -> None:
        """
        Method that is called shortly after stop() method was called.
        Use it to clean up all resources before scheduler exits.
        :return: None
        """
        raise NotImplemented

    @abstractmethod
    def handle(self) -> None:
        """
        Method that should contain business logic of the scheduler.
        Will be executed in the loop until stop() method is called.
        Must be non-blocking.
        :return: None
        """
        raise NotImplemented

    def run(self) -> None:
        """
        This method will be executed in a separate thread
        when Scheduler.start() is called.
        :return: None
        """
        self.startup()
        while not self._stopped():
            self.handle()
        self.shutdown()


class FifoScheduler(Scheduler):
    def startup(self) -> None:
        logging.info('FIFO scheduler starts')

    def shutdown(self) -> None:
        logging.info('FIFO scheduler stops')

    @staticmethod
    def _process_task(task: Dict) -> None:
        logging.info(f'Scheduler processing task: {task}')
        time.sleep(1)

    def handle(self) -> None:
        if TASKS_QUEUE.empty():
            time.sleep(0.2)
            return
        task = TASKS_QUEUE.get(sync=True)
        self._process_task(task)


class SchedulerFactory:
    @staticmethod
    def create_scheduler(scheduler_type: str = 'fifo') -> Scheduler:
        if scheduler_type == 'fifo':
            return FifoScheduler()
