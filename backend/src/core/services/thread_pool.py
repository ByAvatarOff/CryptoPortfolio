import concurrent.futures
from typing import Callable
from concurrent.futures import ThreadPoolExecutor


class ThreadPool:
    def __init__(self, max_workers: int = 10) -> None:
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def run_tasks(self, func: Callable, tasks: list, *args, **kwargs) -> tuple[list, list[dict]]:
        futures = [self.executor.submit(func, task, *args, **kwargs) for task in tasks]

        results = []
        errors = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.extend(result)
            except Exception as e:
                errors.append({
                    "func": func,
                    "error": e
                })
                continue

        return results, errors