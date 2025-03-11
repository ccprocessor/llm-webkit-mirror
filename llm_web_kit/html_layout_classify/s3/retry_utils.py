import functools
import time


def get_func_path(func) -> str:
    if not callable(func):
        return func
    return f'{func.__module__}.{func.__name__}'


def with_retry(func=None, max_retries=5, sleep_time=3):
    def try_sleep():
        try:
            time.sleep(sleep_time)
        except Exception:
            pass

    def get_msg(func, args, kwargs):
        msg = f'Retry exhausted for [{get_func_path(func)}]'
        msg += f', args={args}' if args else ''
        msg += f', kwargs={kwargs}' if kwargs else ''
        return msg

    def handle(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            last_e = None
            while True:
                if retries > max_retries:
                    msg = get_msg(func, args, kwargs)
                    raise Exception(msg) from last_e
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    last_e = e
                    try_sleep()

        return wrapper

    if func is not None:
        return handle(func)

    return handle
