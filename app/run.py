# run.py (place this in /home/andreea/Desktop/ASC/Tema1/asc-public/assignments/1-le-stats-sportif/)

"""
    This module represents the main entry point for the web application.

    It initializes and runs the Flask web server.
    It first tests data access to verify the DataIngestor is properly initialized.

"""

import sys
import os

# Now you can import from app using absolute imports
from app import webserver

# Add the current directory to Python's path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    # Before running the webserver, you can test data access here
    print("Testing Data_Value access...")

    # Try to get the data_values from the DataIngestor instance
    if hasattr(webserver, 'data_ingestor') and hasattr(webserver.data_ingestor, 'data_values'):
        print("Data values from webserver.data_ingestor:")
        print(webserver.data_ingestor.data_values.head(10))  # Print first 10 values
    else:
        print("Could not access data_values from data_ingestor")

    # Run the Flask webserver
    # webserver.run(debug=True)
