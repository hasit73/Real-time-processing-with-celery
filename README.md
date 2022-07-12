## Real-time-processing-with-celery
Real time data generation and processing using celery module in Python

### Prerequisites

- RabbitMQ (Message Broker)
- Python3

### Python requirements

```
celery
eventlet
flower
```

### Usage

Step 1:

- Update `broker` argument parameter while creating Celery class object in real_time_celery/celery.py file.

Step 2:

- Start rabbitmq service if it is not running. Execute following command to start service.
- `rabbitmq-service.bat start`
- NOTE: If ENV variable hasn't set then go to the directory (C:\Program Files\RabbitMQ Server\rabbitmq_server-3.10.5\sbin).

Step 3:

- Execute following commands to run celery app
- `celery -A real_time_celery worker -P eventlet -l info` (Start workers in celery to execute user requests).
- `celery -A real_time_celery flower -l info` (Start flower job, it provides better UI to monitor celery tasks).
- `python -m real_time_celery.run_tasks` (Start real time data generation and processing). 
