from celery import Celery

app = Celery(
    "test_celery",
    broker="amqp://hasit73:****@localhost/hasit_celery",
    backend="rpc://",
    include=["real_time_celery.tasks"],
)
