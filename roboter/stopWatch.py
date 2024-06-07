from datetime import datetime, timedelta

class StopWatch:
    """
    Class for setting a stopwatch used for time-dependant functions
    """

    def __init__(self):
        self.startTime = datetime.now()

    def start(self, durationS : int) -> None:
        """
        Starts a new stopwatch

        Parameters
        ----------
        durationS: Specified duration in seconds the stopwatch should run

        Returns
        ----------
        None
        """

        self.startTime = datetime.now()
        self.duration = durationS * 1000

    def isFinished(self) -> bool:
        """
        Returning if the specified duration has already been exceeded

        Returns
        ----------
        bool
        """
        
        return datetime.now() >= self.startTime + timedelta(milliseconds=self.duration)