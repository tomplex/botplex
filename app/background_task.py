import typing
from multiprocessing import Process


def run_background_task(func: typing.Callable):
    p = Process(target=func)
    p.start()
