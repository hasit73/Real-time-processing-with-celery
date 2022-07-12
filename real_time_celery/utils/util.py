import time


def compute_time(func):
    """Decorate input function with inner function.

    Args:
        func (func): Function to be decorated.
    """
    def wrapped_func(*args, **kwargs):
        """Decorate function to compute execution time

        Returns:
            tuple: Input function results, execution time.
        """
        execution_time = time.perf_counter()
        response = func(*args, **kwargs)
        execution_time = time.perf_counter() - execution_time
        return response, execution_time
    return wrapped_func

