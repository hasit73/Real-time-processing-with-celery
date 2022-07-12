import random
import time

from real_time_celery.celery import app
from real_time_celery.utils import const
from real_time_celery.utils.data_generator import RandomDataGenerator
from real_time_celery.utils.data_processor import DataProcessor
from real_time_celery.utils.logger_util import create_logger

# Define logger and class objects
logger = create_logger("celery_tasks")
data_gen = RandomDataGenerator()
data_processor = DataProcessor()

# Define one mutual list to put all pending user requests.
REQUESTS_QUEUE = []


@app.task(name="Generated data")
def generate_data():
    """Generate random number of records using DateGenerator.

    Returns:
        dict: Generated data.
    """
    num_of_records = random.randint(100, 1000)
    logger.info("Fetching {0} samples from Data generator.".format(num_of_records))
    data, exec_time = data_gen.generate_data(samples=num_of_records)
    logger.info(
        "Data received from Data generator in {0} ms.".format(
            round(exec_time * 1000, 2)
        )
    )
    return data


@app.task(name="Real time data generation job")
def start_data_generator():
    """Start continuos live data generation."""
    while True:
        response = generate_data.delay()
        REQUESTS_QUEUE.append(response)
        time.sleep(const.DATA_GENERATION_INTERVAL)


@app.task(name="Process data")
def processing_data(data):
    """Process input data.

    Args:
        data (list): list of records.
    """
    logger.info(
        "Total {0} samples will be submitted to DataProcessor.".format(
            len(data.get("data", []))
        )
    )
    data, exec_time = data_processor.process_data(data)
    logger.info(
        "DataProcessor has completed processing in {0} ms.".format(
            round(exec_time * 1000, 2)
        )
    )


@app.task(name="Real time data processing job")
def start_data_processor():
    """Start continuos data processing job."""
    while True:
        if len(REQUESTS_QUEUE):
            response = REQUESTS_QUEUE[0]
            if response.state.lower() == "success":
                data = response.get()
                processing_data.delay(data)
                REQUESTS_QUEUE.remove(response)

            else:
                logger.info(
                    "Results are not ready yet for task id {0}.".format(
                        response.task_id
                    )
                )
                logger.info(const.SLEEPING_LOG.format(2))
                time.sleep(2)
        else:
            logger.info(const.SLEEPING_LOG.format(const.WAIT_INTERVAL))
            time.sleep(const.WAIT_INTERVAL)
        time.sleep(const.DATA_PROCESSOR_INTERVAL)


def manage_tasks():
    """Manage all tasks."""
    start_data_generator.delay()
    start_data_processor.delay()
