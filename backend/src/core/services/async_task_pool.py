import asyncio
from typing import Callable, Any


class AsyncTaskPool:
    async def run_task(self, func: Callable, task: Any) -> Any:
        try:
            result = await func(task)
            return result, None
        except Exception as e:
            return None, {
                "func": func,
                "error": str(e)
            }

    async def run_tasks(self, func: Callable, tasks: list[Any]) -> tuple[list, list[dict]]:
        tasks_coroutines = [self.run_task(func, task) for task in tasks]
        completed_tasks = await asyncio.gather(*tasks_coroutines)

        results = []
        errors = []
        for result, error in completed_tasks:
            if error:
                errors.append(error)
            elif result:
                results.append(result)
        return results, errors