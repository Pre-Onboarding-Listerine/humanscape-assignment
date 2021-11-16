import abc
from typing import List

from pydantic import parse_obj_as
from sqlalchemy.orm.exc import StaleDataError

from src.trials.domain import models
from src.trials.exceptions import DoesNotExistTrialsException
from src.trials.infra import orm


class AbstractTrialRepository(abc.ABC):
    @abc.abstractmethod
    def bulk_insert(self, trials: List[models.Trial]):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, trial_id: str) -> models.Trial:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[models.Trial]:
        raise NotImplementedError

    @abc.abstractmethod
    def list_by_ids(self, ids: List[str]) -> List[models.Trial]:
        raise NotImplementedError

    @abc.abstractmethod
    def bulk_update(self, modified: List[models.Trial]):
        raise NotImplementedError


class SqlTrialRepository(AbstractTrialRepository):
    def __init__(self, session):
        self.session = session

    def bulk_insert(self, trials: List[models.Trial]):
        trial_dicts = list(map(lambda trial: trial.dict(), trials))
        self.session.bulk_insert_mappings(orm.Trial, trial_dicts)

    def get(self, trial_id: str) -> models.Trial:
        pass

    def list(self) -> List[models.Trial]:
        pass

    def list_by_ids(self, ids: List[str]) -> List[models.Trial]:
        return parse_obj_as(
            List[models.Trial],
            self.session.query(orm.Trial).filter(orm.Trial.trial_id.in_(ids)).all()
        )

    def bulk_update(self, modified: List[models.Trial]):
        trial_dicts = list(map(lambda trial: trial.dict(), modified))
        try:
            self.session.bulk_update_mappings(orm.Trial, trial_dicts)
        except StaleDataError as e:
            raise DoesNotExistTrialsException(e)
