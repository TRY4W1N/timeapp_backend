import time


class timeit:
    """
    A context manager that measures the execution time of a code block in nanoseconds.
    """

    def __enter__(self):
        self.start_time = time.perf_counter_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.perf_counter_ns()
        self.duration_ns = self.end_time - self.start_time
        return False
