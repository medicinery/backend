from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(max_workers=4)


def run_in_thread(func):
    def wrapper(*args, **kwargs):
        return executor.submit(func, *args, **kwargs)

    return wrapper
