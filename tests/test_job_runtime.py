import unittest
from unittest.mock import MagicMock, patch
import logging
import io

import dsjobs as ds


class TestGetRuntime(unittest.TestCase):
    def setUp(self):
        self.ag_mock = MagicMock()
        self.job_id = "12345"

        # Mocking the log output capture
        self.log_output = io.StringIO()
        logging.basicConfig(stream=self.log_output)

    def test_get_runtime(self):
        # Sample mock data for job history
        mock_history = [
            {"status": "QUEUED", "created": 10},
            {"status": "QUEUED", "created": 20},
            {"status": "RUNNING", "created": 30},
            {"status": "RUNNING", "created": 40},
        ]

        self.ag_mock.jobs.getHistory.return_value = mock_history

        # Call the function
        ds.get_runtime(self.ag_mock, self.job_id)

        # Check if the correct logging occurred
        logs = self.log_output.getvalue()

        # self.assertIn("TOTAL   time: 30", logs)
        # self.assertIn("RUNNING time: 10", logs)
        # self.assertIn("QUEUED  time: 10", logs)

    def tearDown(self):
        # Cleanup after tests
        self.log_output.close()


if __name__ == "__main__":
    unittest.main()
