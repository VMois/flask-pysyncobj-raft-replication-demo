import threading
from abc import abstractmethod, ABC


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
