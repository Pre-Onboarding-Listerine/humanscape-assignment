from typing import List

from src.configs.data_source_configs import BATCH_SIZE
from src.trials.application.unit_of_work import AbstractTrialUnitOfWork
from src.trials.domain import models
from src.trials.dto import TrialListParams
from src.trials.infra.data_source import AbstractTrialDataSource


class TrialBatchService:
    def __init__(self, data_source: AbstractTrialDataSource, uow: AbstractTrialUnitOfWork):
        self.data_source = data_source
        self.uow = uow
        self.batch_size = BATCH_SIZE
        self.page = 0

    def _classify_data(self, collected):
        collected_ids = list(map(lambda trial: trial.trial_id, collected))
        exist_trials = sorted(self.uow.trials.list_by_ids(collected_ids), key=lambda trial: trial.trial_id)
        exist_ids = list(map(lambda trial: trial.trial_id, exist_trials))
        create_required = list(filter(lambda trial: trial.trial_id not in exist_ids, collected))
        collected_existing_trials = list(filter(lambda trial: trial.trial_id in exist_ids, collected))
        update_check_required = sorted(collected_existing_trials, key=lambda trial: trial.trial_id)

        return create_required, update_check_required, exist_trials

    def _check_modified(self, new, old):
        if new.name != old.name:
            return True
        if new.period != old.period:
            return True
        if new.scope != old.scope:
            return True
        if new.category != old.category:
            return True
        if new.institution != old.institution:
            return True
        if new.stage != old.stage:
            return True
        if new.subjects_count != old.subjects_count:
            return True
        if new.department != old.department:
            return True
        return False

    def _get_modified(self, update_check_required, currents):
        update_required = []
        for collected, current in zip(update_check_required, currents):
            collected.id = current.id
            if self._check_modified(collected, current):
                update_required.append(collected)

        return update_required

    def synchronize(self):
        while True:
            self.page += 1
            collected = self.data_source.list(page=self.page, per_page=self.batch_size)
            if not collected:
                break
            with self.uow:
                create_required, update_check_required, currents = self._classify_data(collected)
                update_required = self._get_modified(update_check_required, currents)

                self.uow.trials.bulk_insert(create_required)
                self.uow.trials.bulk_update(update_required)
                self.uow.commit()


class TrialReadService:
    def __init__(self, uow: AbstractTrialUnitOfWork):
        self.uow = uow

    def get_trial(self, trial_id: str) -> models.Trial:
        with self.uow:
            return self.uow.trials.get(trial_id=trial_id)

    def get_trials(self, params: TrialListParams) -> List[models.Trial]:
        with self.uow:
            return self.uow.trials.list(params)
