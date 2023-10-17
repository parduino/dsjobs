import time
from datetime import datetime, timedelta, timezone
from tqdm import tqdm
import logging

# Configuring the logging system
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_status(ag, job_id, time_lapse=15):
    """
    Retrieves and monitors the status of a job from Agave.

    This function initially waits for the job to start, displaying its progress using
    a tqdm progress bar. Once the job starts, it monitors the job's status up to
    a maximum duration specified by the job's "maxHours". If the job completes or fails
    before reaching this maximum duration, it returns the job's final status.

    Args:
      ag (object): The Agave job object used to interact with the job.
      job_id (str): The unique identifier of the job to monitor.
      time_lapse (int, optional): Time interval, in seconds, to wait between status
        checks. Defaults to 15 seconds.

    Returns:
      str: The final status of the job. Typical values include "FINISHED", "FAILED",
           and "STOPPED".

    Raises:
      No exceptions are explicitly raised, but potential exceptions raised by the Agave
      job object or other called functions/methods will propagate.
    """

    previous_status = None
    # Initially check if the job is already running
    status = ag.jobs.getStatus(jobId=job_id)["status"]

    job_details = ag.jobs.get(jobId=job_id)
    max_hours = job_details["maxHours"]

    # Using tqdm to provide visual feedback while waiting for job to start
    with tqdm(desc="Waiting for job to start", dynamic_ncols=True) as pbar:
        while status not in ["RUNNING", "FINISHED", "FAILED", "STOPPED"]:
            time.sleep(time_lapse)
            status = ag.jobs.getStatus(jobId=job_id)["status"]
            pbar.update(1)
            pbar.set_postfix_str(f"Status: {status}")

    # Once the job is running, monitor it for up to maxHours
    max_iterations = int(max_hours * 3600 // time_lapse)

    # Using tqdm for progress bar
    for _ in tqdm(range(max_iterations), desc="Monitoring job", ncols=100):
        status = ag.jobs.getStatus(jobId=job_id)["status"]

        # Print status if it has changed
        if status != previous_status:
            tqdm.write(f"\tStatus: {status}")
            previous_status = status

        # Break the loop if job reaches one of these statuses
        if status in ["FINISHED", "FAILED", "STOPPED"]:
            break

        time.sleep(time_lapse)
    else:
        # This block will execute if the for loop completes without a 'break'
        print("Warning: Maximum monitoring time reached!")

    return status


def get_runtime(ag, job_id):
    """Get the runtime of a job.

    Args:
        ag (object): The Agave object that has the job details.
        job_id (str): The ID of the job for which the runtime needs to be determined.

    Returns:
        None: This function doesn't return a value, but it logs the runtime details.

    """

    logging.info("Runtime Summary")
    logging.info("---------------")

    hist = ag.jobs.getHistory(jobId=job_id)
    logging.info("TOTAL   time: %s", hist[-1]["created"] - hist[0]["created"])

    for i in range(len(hist) - 1):  # To avoid index out of range error in `hist[i+1]`
        if hist[i]["status"] == "RUNNING":
            logging.info(
                "RUNNING time: %s", hist[i + 1]["created"] - hist[i]["created"]
            )
        if hist[i]["status"] == "QUEUED":
            logging.info(
                "QUEUED  time: %s", hist[i + 1]["created"] - hist[i]["created"]
            )
