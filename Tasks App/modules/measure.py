try:
    import psutil
except ImportError:
    psutil = None
import time
from typing import Any, Optional


def measure(func, *args, **kwargs) -> tuple[Any, Optional[float], Optional[float]]:
    if not psutil:
        result: Any = func(*args, **kwargs)
        return result, None, None
    start_time: float = time.time()
    start_memory: Any = psutil.Process().memory_info().rss

    result = func(*args, **kwargs)

    end_time: float = time.time()
    end_memory: Any = psutil.Process().memory_info().rss

    elapsed_time: float = end_time - start_time
    memory_diff: Any = end_memory - start_memory

    return result, elapsed_time, memory_diff