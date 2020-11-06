import time
import math
from datetime import datetime

def curtime():
    from datetime import datetime
    dt = datetime.now()
    return dt.microsecond

def func_per_second(fn, *args):
    """
    Runs a function every second

    Parameters:
    fn -> Function object
    """

    starttime = curtime()
    while True:
        fn(*args)
        time.sleep((1000.0 - ((curtime() - starttime) % 1000.0)) / 1000)


def get_distance(x1, y1, x2, y2):
    """
    Returns distance two points
    """

    return math.sqrt(pow(abs(x1-x2), 2) + pow(abs(y1-y2), 2))


def check_within_range(x1, y1, range1, x2, y2):
    """
    Returns boolean whether (x2, y2) is in range of (x1, y1)
    """

    return pow(abs(x1-x2), 2) + pow(abs(y1-y2), 2) <= pow(range1, 2)
