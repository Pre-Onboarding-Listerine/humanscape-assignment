import logging
import signal
import sys

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.blocking import BlockingScheduler

import cron
import tasks
from src.configs.database import Base, engine

logging.basicConfig(
    format="[%(asctime)s] [PID %(process)d] [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s",
    level=logging.DEBUG,
)

logging.getLogger("pika").setLevel(logging.WARNING)


def main():
    Base.metadata.create_all(bind=engine)

    jobstores = {
        'default': RedisJobStore(
            host='localhost',
            port=6379,
            password="redispassword"
        )
    }

    scheduler = BlockingScheduler(jobstores=jobstores)
    print(cron.JOBS)
    for trigger, module_path, func_name in cron.JOBS:
        print(trigger)
        print(module_path)
        print(func_name)
        job_path = f"{module_path}:{func_name}.send"
        job_name = f"{module_path}.{func_name}"
        scheduler.add_job(job_path, trigger=trigger, name=job_name)

    def shutdown(signum, frame):
        scheduler.shutdown()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    scheduler.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
