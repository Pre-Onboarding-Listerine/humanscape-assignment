from src.configs.data_source_configs import BATCH_SIZE
from src.trials.application.unit_of_work import AbstractTrialUnitOfWork
from src.trials.infra.data_source import AbstractTrialDataSource


class TrialBatchService:
    def __init__(self, data_source: AbstractTrialDataSource, uow: AbstractTrialUnitOfWork):
        self.data_source = data_source
        self.uow = uow
        self.batch_size = BATCH_SIZE

    def synchronize(self):
        page = 0
        while True:
            page += 1
            collected = self.data_source.list(page=page, per_page=self.batch_size)
            if not collected:
                break
            with self.uow:
                collected_ids = list(map(lambda trial: trial.id, collected))
                exist_trials = sorted(self.uow.trials.list_by_ids(collected_ids), key=lambda trial: trial.id)
                exist_ids = list(map(lambda trial: trial.id, exist_trials))
                new_trials = list(filter(lambda trial: trial.id not in exist_ids, collected))
                collected_existing_trials = list(filter(lambda trial: trial.id in exist_ids, collected))
                collected_existing_trials = sorted(collected_existing_trials, key=lambda trial: trial.id)

                updated = []
                for collected, exist in zip(collected_existing_trials, exist_trials):
                    if collected != exist:
                        updated.append(collected)

                self.uow.trials.bulk_insert(new_trials)
                self.uow.trials.bulk_update(updated)
                self.uow.commit()
