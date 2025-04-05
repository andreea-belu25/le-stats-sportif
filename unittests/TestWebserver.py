"""
    Unit tests for the web server application.
"""

import unittest
import time
import json

from app import webserver
from app.data_ingestor import DataIngestor

class TestWebserver(unittest.TestCase):

    """
        Test suite for verifying web server API functionality.
        Each test method is designed to verify a specific aspect of the server's behavior,
        with proper setup.
    """

    def setUp(self):

        """
            This method is executed before each test case.
            It initializes the web server and the task runner.
        """

        self.webserver = webserver
        self.webserver.testing = True
        self.client = self.webserver.test_client()
        self.data_ingestor = DataIngestor('./nutrition_activity_obesity_usa_subset.csv')


    def test_csv_read_correctly(self):
        
        """
            This test verifies that the CSV file is read correctly.
        """

        #  Check that the DataFrame was created
        self.assertIsNotNone(self.data_ingestor.df)
        
        #  Check that the DataFrame is not empty
        self.assertGreater(len(self.data_ingestor.df), 0)

        expected_columns = ['LocationDesc', 'Question', 'Data_Value',
                            'Stratification1', 'StratificationCategory1']
        
        #  Check that only the expected columns were loaded
        for column in expected_columns:
            self.assertIn(column, self.data_ingestor.df.columns)


    def test_get_results_invalid_job_id_high(self):

        """
            This test verifies that the API correctly handles requests with invalid job IDs.
        """

        invalid_id_high = 9999
        
        response = self.client.get(f"/api/get_results/{invalid_id_high}")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_response = {
            "reason": "Invalid job_id",
            "status": "error"
        }

        self.assertEqual(response_data, expected_response)


    def test_get_results_invalid_job_id_low(self):

        """
            This test verifies that the API correctly handles requests with invalid job IDs.
        """

        invalid_id_low = 0

        response = self.client.get(f"/api/get_results/{invalid_id_low}")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)

        expected_response = {
            "reason": "Invalid job_id",
            "status": "error"
        }

        self.assertEqual(response_data, expected_response)


    def test_graceful_shutdown(self):
        
        """
            This test verifies that the graceful shutdown mechanism works correctly.
        """
        
        response = self.client.get("/api/graceful_shutdown")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertIn(response_data["status"], ["done", "running"])

        data = {
            "question": "Percent of adults who report consuming fruit less than one time daily",
            "state": "Wyoming"
        }
        
        response = self.client.post("/api/state_mean", json = data)
        
        # Verify response contains error when server is shutting down
        response_data = json.loads(response.data)
        self.assertEqual(response_data.get("status"), "error")
        self.assertEqual(response_data.get("reason"), "shutting down")


    def test_get_all_jobs(self):
        
        """
            This test verifies that the jobs endpoint correctly returns all jobs.
        """

        response = self.client.get("/api/jobs")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
    
        self.assertEqual(response_data["status"], "done")
        self.assertIn("data", response_data)


    def test_get_num_jobs(self):

        """
            This test verifies that the num_jobs endpoint correctly returns the number of jobs.
        """

        response = self.client.get("/api/num_jobs")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertEqual(response_data["status"], "done")
        self.assertTrue("remaining_jobs" in response_data)
    

    def test_post_num_job(self):

        """
            This test verifies that the num_jobs endpoint correctly rejects POST requests.
        """

        response = self.client.post("/api/num_jobs")
        self.assertEqual(response.status_code, 405)
        
        # Check if response contains error message
        # When using Flask test client, we need to check if content exists
        if response.data:
            try:
                response_data = json.loads(response.data)
                if "error" in response_data:
                    self.assertEqual(response_data["error"], "Method not allowed")
            except json.JSONDecodeError:
                pass  # If not JSON, that's okay for a 405 response
