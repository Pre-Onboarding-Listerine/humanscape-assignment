from datetime import datetime

from assertpy import assert_that

from src.trials.application.unit_of_work import SqlTrialUnitOfWork
from src.trials.exceptions import DoesNotExistTrialsException, DuplicatedTrialsException


def list_all_trial(session):
    return list(session.execute(
        "SELECT * FROM trials"
    ))


def insert_trials(session, trials):
    trials_str = ""
    for trial in trials:
        trials_str += f"('{trial.trial_id}', '{trial.name}', '{trial.period}', '{trial.scope}', '{trial.category}', '{trial.institution}', '{trial.stage}', '{trial.subjects_count}', '{trial.department}', '{datetime.utcnow()}', '{datetime.utcnow()}'),"

    session.execute(
        "INSERT INTO trials (trial_id, name, period, scope, category, institution, stage, subjects_count, department, created_at, updated_at) VALUES "
        + trials_str[:-1]
    )


def test_bulk_insert_multiple_trials_with_not_exist_trials(session_factory, trials):
    uow = SqlTrialUnitOfWork(session_factory=session_factory)
    session = session_factory()
    with uow:
        uow.trials.bulk_insert(trials)
        actual = list_all_trial(session)

        assert_that(len(actual)).is_equal_to(len(trials))


def test_bulk_insert_trials_with_exist_trials(session_factory, trials):
    session = session_factory()
    insert_trials(session, trials)
    session.commit()

    uow = SqlTrialUnitOfWork(session_factory=session_factory)
    with uow:
        assert_that(uow.trials.bulk_insert).raises(DuplicatedTrialsException).when_called_with(trials)


def test_list_by_ids(session_factory, trials):
    session = session_factory()
    insert_trials(session, trials)
    session.commit()

    trial_ids = list(map(lambda trial: trial.trial_id, trials))
    uow = SqlTrialUnitOfWork(session_factory)
    with uow:
        actual = uow.trials.list_by_ids(trial_ids)
        assert_that(len(actual)).is_equal_to(len(trials))


def test_bulk_update_with_not_exist_rows(session_factory, trials):
    uow = SqlTrialUnitOfWork(session_factory)
    with uow:
        assert_that(uow.trials.bulk_update).raises(DoesNotExistTrialsException).when_called_with(trials)


def test_bulk_update_with_exist_rows(session_factory, trials):
    session = session_factory()
    insert_trials(session, trials)
    session.commit()

    before = list_all_trial(session)
    uow = SqlTrialUnitOfWork(session_factory)
    with uow:
        for i, trial in enumerate(trials):
            trial.id = i + 1
        uow.trials.bulk_update(trials)
        uow.commit()
    after = list_all_trial(session)

    assert_that(before[0].trial_id).is_equal_to(after[0].trial_id)
    assert_that(before[0].updated_at).is_not_equal_to(after[0].updated_at)
