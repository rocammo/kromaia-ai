class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Log(metaclass=Singleton):
    def __init__(self, verbose: bool = None):
        self.verbose = verbose

    def vprint(self, args):
        if self.verbose:
            print(args)
