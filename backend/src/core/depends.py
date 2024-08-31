from src.core.services.thread_pool import ThreadPool
from src.core.services.async_task_pool import AsyncTaskPool


def _get_thread_pool() -> ThreadPool:
    return ThreadPool()


def _get_async_task_pool() -> AsyncTaskPool:
    return AsyncTaskPool()