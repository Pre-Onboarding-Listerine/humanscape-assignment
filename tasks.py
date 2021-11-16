import dramatiq
from dramatiq.brokers.redis import RedisBroker

from cron import cron
from src.configs.data_source_configs import END_POINT, AUTHORIZATION, SERVICE_KEY
from src.configs.database import SessionLocal
from src.configs.redis_config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from src.trials.application.services import TrialBatchService
from src.trials.application.unit_of_work import SqlTrialUnitOfWork
from src.trials.exceptions import UnauthorizedAuthenticationKeyException, OpenAPIServerErrorException
from src.trials.infra.data_source import RestTrialDataSource

redis_broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
dramatiq.set_broker(redis_broker)


@cron("* * * * *")
@dramatiq.actor
def synchronize_data():
    data_source = RestTrialDataSource(url=END_POINT, authorization=AUTHORIZATION, service_key=SERVICE_KEY)
    uow = SqlTrialUnitOfWork(SessionLocal)
    try:
        TrialBatchService(data_source, uow).synchronize()
    except UnauthorizedAuthenticationKeyException as e:
        print(e)
    except OpenAPIServerErrorException as e:
        print(e)
