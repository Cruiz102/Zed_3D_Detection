#  Python Functions and decorators for analizing  the performance and memory of the application
import sys
import tracemalloc
import psutil
import os


def print_memory_usage(PythonObject: object):
    bytes: int = sys.getsizeof(PythonObject)
    print(f"Memory usage of {PythonObject} is {bytes * 10**-3} kB")



def print_time_usage(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time usage of {func.__name__} is {(end - start) * 10**3} ms")
        return result
    return wrapper

def get_tracemalloc_memory_usage():
    tracemalloc.start()

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 ]")
    for stat in top_stats[:20]:
        print(stat)



def measure_memory(func, *args, **kwargs):
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 ** 2  # memory use in MB
    
    result = func(*args, **kwargs)

    mem_after = process.memory_info().rss / 1024 ** 2  # memory use in MB
    print(f"Memory used: {mem_after - mem_before:.2f} MB")
    return result


def measure_disk_usage(func, *args, **kwargs):
    # process = psutil.Process(os.getpid())
    # disk_before = process.memory_info().rss / 1024 ** 2  # memory use in MB

    # result = func(*args, **kwargs)
    # return result

    pass



def measure_temperature(func, *args, **kwargs):
    # process = psutil.Process(os.getpid())
    # temperature_before = process.memory_info().rss / 1024 ** 2

    pass




def measure_mean_time_usage(func, iterations: int, *args, **kwargs):
    pass
