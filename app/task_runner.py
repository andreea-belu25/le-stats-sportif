"""
    This module handles the synchronization.
"""

from queue import Queue, Empty
from threading import Thread
import threading
import os
import json

class ThreadPool:

    """
        It implements a ThreadPool of TaskRunners.
        It submits tasks in the queue, it stops all
        the task runners in the queue and also provide
        a status for a specific job_id.
    """

    def __init__(self, data_ingestor):

        """
            It initializes a Threadpool with the env var TP_NUM_THREADS
            if it is defined, otherwise using the number of logical CPUs available.

            It uses a queue for tasks, an Event variable which should stop the 
            webserver when it is set, a list for task runners, a dict in which
            to keep the results and the data extracted from csv.
        """

        self.num_threads = os.getenv("TP_NUM_OF_THREADS")
        if self.num_threads is None:
            self.num_threads = os.cpu_count()

        self.tasks_queue = Queue()
        self.graceful_shutdown = threading.Event()
        self.task_runners = []
        self.job_results = {}
        self.data_ingestor = data_ingestor

        for i in range(self.num_threads):
            task_runner = TaskRunner(i, self)
            task_runner.start()
            self.task_runners.append(task_runner)


    def submit(self, task_type, args, job_id):

        """
            It adds a task in the queue, udpating its arguments in the 
            job_results too.
        """

        self.job_results[job_id] = {
            "status": "pending",
            "task_type": task_type,
            "worker": None,
        }

        self.tasks_queue.put((task_type, args, job_id))


    def shutdown(self):

        """
            It stops all the task runners.
        """

        self.graceful_shutdown.set()
        for task_runner in self.task_runners:
            task_runner.join()


    def get_job_status(self, job_id):

        """
            It gets job_status for a provided job_id.
        """

        if job_id in self.job_results:
            return self.job_results[job_id]

        return None


class TaskRunner(Thread):

    """
        It handles a job.
        It constantly updates its status.
        It writes the result to a specific file.
    """

    def __init__(self, index, threadpool):

        """
            It initializes each task runner.
            It uses a dictonary to link task type and the function that
            has to be executed by the task runner.
        """

        super().__init__()
        self.index = index
        self.tasks_queue = threadpool.tasks_queue
        self.graceful_shutdown = threadpool.graceful_shutdown
        self.data_ingestor = threadpool.data_ingestor
        self.job_results = threadpool.job_results

        self.tasks_dict = {
            "get_states_mean" : self.data_ingestor.get_states_mean,
            "get_state_mean" : self.data_ingestor.get_state_mean,
            "get_best5" : self.data_ingestor.get_best5,
            "get_worst5" : self.data_ingestor.get_worst5,
            "get_global_mean" : self.data_ingestor.get_global_mean,
            "get_diff_from_mean" : self.data_ingestor.get_diff_from_mean,
            "get_state_diff_from_mean" : self.data_ingestor.get_state_diff_from_mean,
            "get_mean_by_category" : self.data_ingestor.get_mean_by_category,
            "get_state_mean_by_category" : self.data_ingestor.get_state_mean_by_category
        }


    def run(self):

        """
            It gets pending job
            It updates job status from 'pending' to processing'
            It executes the job and save the result to disk
            It updates job status from 'processing' to 'completed'
            It repeats until graceful_shutdown
        """

        while True:
            if self.graceful_shutdown.is_set() and self.tasks_queue.empty():
                return

            try:
                task_type, args, job_id = self.tasks_queue.get(timeout = 0.5)
            except Empty:
                continue

            self.job_results[job_id] = {
                "status": "processing",
                "task_type": task_type,
                "worker": self.index,
            }

            result = self.tasks_dict[task_type](*args)

            self.save_result(job_id, result)

            self.job_results[job_id] = {
                "status": "completed",
                "task_type": task_type,
                "worker": self.index,
            }


    def save_result(self, job_id, result):

        """
            It saves the result to 'results/job_{job_id}.json' file
        """

        os.makedirs('results', exist_ok = True)
        filename = f"results/job_{job_id}.json"

        with open(filename, 'w', encoding = 'utf-8') as result_file:
            json.dump(result, result_file)
 