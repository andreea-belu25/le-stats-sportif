"""
    This module contains the logic for processing API endpoints requests.
"""

import json
from flask import request, jsonify
from app import webserver
from .webserver_log import logger

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():

    """
        This function is a model for handling API requests.
        It expects and returns some JSON data.
    """

    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)

    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):

    """
        This function handle API requests for getting results from a job_id.
        It receives a job_id and returns the status of processing that job.
    """

    if request.method == 'GET':
        logger.info("Hopefully get results from {'job_id': %s}", job_id)

        job_id = int(job_id)

        if job_id > int(webserver.job_counter) or job_id < 1:
            logger.error("Invalid job_id: %d", job_id)
            return jsonify({"status": "error", "reason": "Invalid job_id"})

        job_status = webserver.tasks_runner.get_job_status(job_id)

        if job_status and job_status["status"] == "completed":
            with open(f'results/job_{job_id}.json', 'r', encoding = 'utf-8') as file:
                try:
                    result = json.load(file)
                    return jsonify({"status": "done", "data": result})
                except json.JSONDecodeError:
                    return jsonify({"status": "running"})
        else:
            return jsonify({"status": "running"})
    else:
        return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():

    """
        This function should no longer receive POST requests if the webserver
        is shutting down.
        It handles API requests for getting data about states mean.
        It returns the job_id that can be used to follow the result status.
    """

    if getattr(webserver, 'shutting_down', False):
        logger.error("Server is shutting down")
        return jsonify({"status": "error", "reason": "shutting down"})

    if request.method == 'POST':
        data = request.json
        logger.info("Got request data: %s for hopefully get_states_mean", data)

        job_id = webserver.job_counter
        webserver.job_counter += 1
        webserver.tasks_runner.submit("get_states_mean", [data["question"]], job_id)

        return jsonify({"job_id": job_id})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():

    """
        This function should no longer receive POST requests if the webserver
        is shutting down.
        It handles API requests for getting data about a specific state mean.
        It returns the job_id that can be used to follow the result status.
    """

    if getattr(webserver, 'shutting_down', False):
        logger.error("Server is shutting down")
        return jsonify({"status": "error", "reason": "shutting down"})

    if request.method == 'POST':
        data = request.json
        logger.info("Got request data: %s for hopefully get_state_mean", data)

        job_id = webserver.job_counter
        webserver.job_counter += 1
        webserver.tasks_runner.submit("get_state_mean", [data["state"], data["question"]], job_id)

        return jsonify({"job_id": job_id})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/best5', methods=['POST'])
def best5_request():

    """
        This function should no longer receive POST requests if the webserver
        is shutting down.
        It handles API requests for getting data about best5 states based on some criteria.
        It returns the job_id that can be used to follow the result status.
    """

    if getattr(webserver, 'shutting_down', False):
        logger.error("Server is shutting down")
        return jsonify({"status": "error", "reason": "shutting down"})

    if request.method == 'POST':
        data = request.json
        logger.info("Got request data: %s for hopefully get_best5", data)

        job_id = webserver.job_counter
        webserver.job_counter += 1
        webserver.tasks_runner.submit("get_best5", [data["question"]], job_id)

        return jsonify({"job_id": job_id})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():

    """
        This function should no longer receive POST requests if the webserver
        is shutting down.
        It handles API requests for getting data about worst5 states based on some criteria.
        It returns the job_id that can be used to follow the result status.
    
    """

    if getattr(webserver, 'shutting_down', False):
        logger.error("Server is shutting down")
        return jsonify({"status": "error", "reason": "shutting down"})

    if request.method == 'POST':
        data = request.json
        logger.info("Got request data: %s for hopefully get_worst5", data)

        job_id = webserver.job_counter
        webserver.job_counter += 1
        webserver.tasks_runner.submit("get_worst5", [data["question"]], job_id)

        return jsonify({"job_id": job_id})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():

    """
        This function should no longer receive POST requests if the webserver
        is shutting down.
        It handles API requests for getting data about global mean.
        It returns the job_id that can be used to follow the result status.
    """

    if getattr(webserver, 'shutting_down', False):
        logger.error("Server is shutting down")
        return jsonify({"status": "error", "reason": "shutting down"})

    if request.method == 'POST':
        data = request.json
        logger.info("Got request data: %s for hopefully get_global_mean", data)

        job_id = webserver.job_counter
        webserver.job_counter += 1
        webserver.tasks_runner.submit("get_global_mean", [data["question"]], job_id)

        return jsonify({"job_id": job_id})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():

    """
        This function should no longer receive POST requests if the webserver
        is shutting down.
        It handles API requests for getting data about diff from mean.
        It returns the job_id that can be used to follow the result status.
    """

    if getattr(webserver, 'shutting_down', False):
        logger.error("Server is shutting down")
        return jsonify({"status": "error", "reason": "shutting down"})

    if request.method == 'POST':
        data = request.json
        logger.info("Got request data: %s for hopefully get_diff_from_mean", data)

        job_id = webserver.job_counter
        webserver.job_counter += 1
        webserver.tasks_runner.submit("get_diff_from_mean", [data["question"]], job_id)

        return jsonify({"job_id": job_id})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():

    """
        This function should no longer receive POST requests if the webserver
        is shutting down.
        It handles API requests for getting data about state diff from mean.
        It returns the job_id that can be used to follow the result status.
    """

    if getattr(webserver, 'shutting_down', False):
        logger.error("Server is shutting down")
        return jsonify({"status": "error", "reason": "shutting down"})

    if request.method == 'POST':
        data = request.json
        logger.info("Got request data: %s for hopefully get_diff_from_mean", data)

        job_id = webserver.job_counter
        webserver.job_counter += 1
        webserver.tasks_runner.submit("get_state_diff_from_mean",
                                      [data["state"], data["question"]], job_id)

        return jsonify({"job_id": job_id})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():

    """
        This function should no longer receive POST requests if the webserver
        is shutting down.
        It handles API requests for getting data about mean by category.
        It returns the job_id that can be used to follow the result status.
    """

    if getattr(webserver, 'shutting_down', False):
        logger.error("Server is shutting down")
        return jsonify({"status": "error", "reason": "shutting down"})

    if request.method == 'POST':
        data = request.json
        logger.info("Got request data: %s for hopefully get_mean_by_category", data)

        job_id = webserver.job_counter
        webserver.job_counter += 1
        webserver.tasks_runner.submit("get_mean_by_category", [data["question"]], job_id)

        return jsonify({"job_id": job_id})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():

    """
        This function should no longer receive POST requests if the webserver
        is shutting down.
        It handles API requests for getting data about state mean by category.
        It returns the job_id that can be used to follow the result status.
    """

    if getattr(webserver, 'shutting_down', False):
        logger.error("Server is shutting down")
        return jsonify({"status": "error", "reason": "shutting down"})

    if request.method == 'POST':
        data = request.json
        logger.info("Got request data: %s for hopefully get_state_mean_by_category", data)

        job_id = webserver.job_counter
        webserver.job_counter += 1
        webserver.tasks_runner.submit("get_state_mean_by_category",
                                     [data["state"], data["question"]], job_id)

        return jsonify({"job_id": job_id})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/graceful_shutdown', methods = ['GET'])
def graceful_shutdown():

    """
        This function should shutdown the webserver and return the
        status for task runners.
    """

    if request.method == 'GET':
        logger.info("Graceful shutdown requested")
        webserver.shutting_down = True
        webserver.tasks_runner.shutdown()

        if webserver.tasks_runner.tasks_queue.empty():
            return jsonify({"status": "done"})

        return jsonify({"status": "running"})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/jobs', methods = ['GET'])
def get_all_jobs():

    """
        This function return the status and its corresponding id for
        each job.
    """

    if request.method == 'GET':
        logger.info("Getting all jobs")

        jobs_data = []

        for job_id in range(1, webserver.job_counter):
            job_status = webserver.tasks_runner.get_job_status(job_id)
            jobs_data.append({str(job_id): job_status})

        return jsonify({"status": "done", "data": jobs_data})

    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/num_jobs', methods = ['GET'])
def get_num_jobs():

    """
        This function should return the number of remaining jobs
        to process. After shutting down the webserver and after 
        a specific time, the server could be stopped completely.
    """

    if request.method == 'GET':
        remaining_jobs = webserver.tasks_runner.tasks_queue.qsize()

        return jsonify({"status": "done", "remaining_jobs": remaining_jobs})

    return jsonify({"error": "Method not allowed"}), 405


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():

    """
        Displays an HTML welcome page listing all defined routes in the application.
    """

    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = "".join(f"<p>{route}</p>" for route in routes)

    msg += paragraphs
    return msg

def get_defined_routes():

    """
        A helper function that collects all defined routes from the webserver's URL map.
    """

    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
