import abc
from typing import List

from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import parse_obj_as
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

from src.trials.domain import models
from src.trials.dto import TrialListParams
from src.trials.exceptions import DoesNotExistTrialsException, DuplicatedTrialsException, TrialNotFoundException
from src.trials.infra import orm


class AbstractTrialRepository(abc.ABC):
    @abc.abstractmethod
    def bulk_insert(self, trials: List[models.Trial]):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, trial_id: str) -> models.Trial:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, params: TrialListParams) -> List[models.Trial]:
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
        try:
            self.session.bulk_insert_mappings(orm.Trial, trial_dicts)
        except IntegrityError as e:
            raise DuplicatedTrialsException(e)

    def get(self, trial_id: str) -> models.Trial:
        trial = self.session.query(orm.Trial).filter(orm.Trial.trial_id == trial_id).first()
        if not trial:
            raise TrialNotFoundException(f"trial {trial_id} is not found")
        return models.Trial.from_orm(trial)

    def list(self, params: TrialListParams) -> List[models.Trial]:
        query = self.session.query(orm.Trial).filter()
        if params.start:
            query = query.filter(orm.Trial.updated_at >= params.start)
        if params.end:
            query = query.filter(orm.Trial.updated_at < params.end)
        return paginate(query)

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
