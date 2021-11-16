from assertpy import assert_that

from src.trials.application.unit_of_work import SqlTrialUnitOfWork


def list_all_trial(session):
    return list(session.execute(
        "SELECT * FROM trials"
    ))


def insert_trials(session, trials):
    trials_str = ""
    for trial in trials:
        trials_str += f"('{trial.trial_id}', '{trial.name}', '{trial.period}', '{trial.scope}', '{trial.category}', '{trial.institution}', '{trial.stage}', '{trial.subjects_count}', '{trial.department}'),"

    session.execute(
        "INSERT INTO trials (trial_id, name, period, scope, category, institution, stage, subjects_count, department) VALUES "
        + trials_str[:-1]
    )


def test_put_multiple_trials(session_factory, trials):
    uow = SqlTrialUnitOfWork(session_factory=session_factory)
    session = session_factory()
    with uow:
        uow.trials.bulk_insert(trials)
        actual = list_all_trial(session)

        assert_that(len(actual)).is_equal_to(len(trials))


def test_list_by_ids(session_factory, trials):
    session = session_factory()
    insert_trials(session, trials)
    session.commit()

    trial_ids = list(map(lambda trial: trial.trial_id, trials))
    uow = SqlTrialUnitOfWork(session_factory)
    with uow:
        actual = uow.trials.list_by_ids(trial_ids)
        assert_that(len(actual)).is_equal_to(len(trials))
