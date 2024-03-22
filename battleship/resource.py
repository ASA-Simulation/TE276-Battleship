class TimeResource(object):
    """TimeResource is a singleton that manages the execution time."""

    # simulation integration step
    __delta_time: float = 0.0

    # execution time tracker
    __exec_time: float = 0.0

    # singleton pattern
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(TimeResource, cls).__new__(cls)
        return cls.instance

    @classmethod
    def add_time(cls) -> float:
        cls.__exec_time += cls.__delta_time
        return cls.get_time()

    @classmethod
    def set_dt(cls, dt: float) -> None:
        cls.__delta_time = dt

    @classmethod
    def get_dt(cls):
        return cls.__delta_time

    @classmethod
    def get_rate(cls):
        return 1.0 / cls.__delta_time

    @classmethod
    def get_time(cls):
        return cls.__exec_time
