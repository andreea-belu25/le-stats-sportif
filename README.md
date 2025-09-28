
This project implements a multi-threaded Flask web server that processes and analyzes nutrition, physical activity, and obesity data 
from 2011 to 2022 in US states, also considering demographic catgories.


Organization
----

- __init__.py: Initializes the Flask web application with data processing capabilities.
- run.py: Main entry point for the web application. Initializes and runs the Flask web server.
- webserver_log.py: Creates a logger named 'webserver' that captures all log levels, using a rotating file handler and a custom time format.
- data_ingestor.py: Handles core data processing functionality for the health statistics application.
- routes.py: Implements all the API endpoints.
- task_runner.py: Manages synchronization and data processing tasks submitted to a thread pool.
- unittests/TestWebserver.py: Contains tests to validate the webserver's functionality that is not checked by the automated checker.


Implementation
----

I chose to keep data processing logic in data_ingestor.py for easier code modularity and debugging. 
For synchronization, I used a simple Event() mechanism as it was sufficient for the application's needs. The job status is continuously 
updated to track task execution progress. I implemented a dictionary mapping task types to corresponding data ingestor functions, 
eliminating the need for conditional checks and enhancing code modularity.
The unit tests cover functionality not tested by the checker, such as handling invalid job IDs, processing requests during shutdown, and 
validating proper CSV reading.

I consider this project was helpful, because I discovered how easy is to use pandas functions for efficient data manipulation.
I also got in contact with implementing synchronization in Python and learning about it. Although, I met with some challenges managing the
synchronization part.
I also learned more about developing and testing RESTful APIs.
I also discovered about unittests, which at some point represent also a difficulty in implementing and logging.

Although, I consider there is also room for improvement, I am quite satisfied with the final version of this project.


Functionality Details
---
`data_ingestor.py`:
   #get_state_mean(self, question):
    - identifies all rows where the 'Question' column matches the input question
    - groups the filtered data by state, creating groups where each contains all data for a specific state
    - for each state group, calculates the mean of the 'Data_Value' column
    - sorts these means in ascending order
    - returns a dictionary with all states and their mean values

    #get_state_mean(self, state, question):
    - the logic is similar to get_states_mean(), but it applies only to a specific state, filtering data by both question and state

    #get_best5(self, question):
    - gets the mean values for all states, using get_state_mean() function
    - depending on the type of question, returns either the first five values or the last five values as a dictionary

    #get_worst5(self, question):
    - the logic is similar to get_best5()

    #get_global_mean(self, question):
    - filters the dataset for a specific health question
    - calculates the average of all Data_Value entries across all states
    - returns a dictionary with a single key "global_mean" and the calculated average

    #get_diff_from_mean(self, question):
    - gets the global mean for a question
    - gets the mean for each state
    - calculates the difference (global mean - state mean) for every state
    - returns a dictionary mapping each state to its difference from the global mean

    #get_state_diff_from_mean(self, state, question):
    - the logic is similar to get_diff_from_mean(), but it applies only to a specific state

    #get_mean_by_category(self, question):
    - filters the dataset for a specific health question
    - groups data by state, category (StratificationCategory1), and segment (Stratification1)
    - calculates the mean for each unique combination
    - returns a dictionary where keys are formatted as "(state, category, segment)" strings and values are the corresponding means

    #get_state_mean_by_category(self, state, question):
    - the logic is similar to get_diff_from_mean(), but it applies only to a specific state

`routes.py`:
    Each endpoint validates the request method, checks if the server is shutting down, processes data through a task queue, 
    and returns the appropriate response.

`task_runner.py`:
    Threadpool class:
      - determines thread count from environment variable or CPU count
      - manages a task queue, shutdown event (used for ensuring all tasks are completed), and job results dictionary
      - provides methods for task submission and job status tracking

    TaskRunner class:
      - maps task types to corresponding data ingestor methods
      - continuously checks the queue for new tasks
      - updates job status through processing stages
      - saves results to disk as JSON files

    
Useful Resources
---
- ASC course materials from OCW
- Pandas documentation
- Postman for manual request testing
