import pytest
from assertpy import assert_that

from src.trials.domain.models import Trial
from src.trials.infra.data_source import RestTrialDataSource


@pytest.fixture
def trial_data_source(rest_authentication):
    return RestTrialDataSource(**rest_authentication)


def test_list_trial_data(trial_data_source):
    actual = trial_data_source.list()
    expected = 10

    assert_that(len(actual)).is_equal_to(expected)
    assert_that(actual[0]).is_instance_of(Trial)
