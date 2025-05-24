"""
This module enables the execution of tasks in different processes using Queues.
The Executor class is a wrapper around the multiprocessing standard library.
Ideal for CPU bound tasks that can be parallelized.
"""
import time
from multiprocessing import Process, Queue
from typing import Any, Callable, Sequence


# Define task_function at the top level of the module
def task_function(data: Any) -> None:
    """
    Example Job function that processes data.

    Args:
        data (Any): Any input data required by the job.
    """
    print(f"Processing {data}")
    time.sleep(1)  # Simulate work


class Executor:
    """
    Executor class to manage worker processes.
    """

    def __init__(self, num_workers: int = 4) -> None:
        self.tasks_queue: Queue = Queue()
        self.workers = [
            Process(target=self.worker) for _ in range(num_workers)
        ]  # noqa: E501
        for worker in self.workers:
            worker.start()

    def add_task(self, task: Callable | None, *args: Sequence[Any]) -> None:
        """
        Add a task to the queue. Task should be a callable with its arguments.
        """
        self.tasks_queue.put((task, args))

    def worker(self) -> None:
        """
        Worker process: Retrieve tasks from the queue and execute them.
        """
        while True:
            task, args = self.tasks_queue.get()
            if task is None:
                # None is the signal to stop.
                break
            task(*args)

    def stop_workers(self) -> None:
        """
        Stop all worker processes.
        """
        for _ in self.workers:
            self.add_task(None)  # Signal to stop.
        for worker in self.workers:
            worker.join()

    def execute(self, task: Callable, *args: Sequence[Any]) -> None:
        """
        Execute method to add tasks. Now accepts a task and its arguments.
        """
        # Add tasks
        for arg in args:
            self.add_task(task, arg)


if __name__ == "__main__":
    executor = Executor(num_workers=4)
    # Now you can pass task_function and its arguments directly to execute
    data_items = [f"data {i}" for i in range(10)]
    executor.execute(task_function, *data_items)

    time.sleep(5)  # Wait for some tasks to process
    executor.stop_workers()
