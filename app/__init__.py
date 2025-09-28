"""
    This module initializes a Flask web application with data processing capabilities.
"""

import os
from flask import Flask
from .data_ingestor import DataIngestor
from .task_runner import ThreadPool

if not os.path.exists('results'):
    os.mkdir('results')

webserver = Flask(__name__)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.tasks_runner = ThreadPool(webserver.data_ingestor) 
webserver.job_counter = 1

from app import routes
