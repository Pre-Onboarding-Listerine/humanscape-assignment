import abc
from typing import List

import requests
from starlette import status

from src.trials.domain.models import Trial
from src.trials.exceptions import UnauthorizedAuthenticationKeyException, OpenAPIServerErrorException


class AbstractTrialDataSource(abc.ABC):
    @abc.abstractmethod
    def list(self, page: int = 1, per_page: int = 10, return_type: str = "json") -> List[Trial]:
        raise NotImplementedError


class RestTrialDataSource(AbstractTrialDataSource):
    def __init__(self, url: str, authorization: str, service_key: str):
        self.url = url
        self.authorization = authorization
        self.service_key = service_key

    def list(self, page: int = 1, per_page: int = 10, return_type: str = "json") -> List[Trial]:
        headers = {"Authorization": self.authorization}
        params = {
            "serviceKey": self.service_key,
            "page": page,
            "perPage": per_page,
            "return_type": return_type
        }

        response = requests.get(url=self.url, headers=headers, params=params)
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise UnauthorizedAuthenticationKeyException("authentication key is not authorized")
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise OpenAPIServerErrorException(f"the end point {self.url} returned server error")

        data = response.json()['data']
        return list(map(
            lambda trial: Trial(
                trial_id=trial["과제번호"],
                name=trial["과제명"],
                period=trial["연구기간"],
                scope=trial["연구범위"],
                category=trial["연구종류"],
                institution=trial["연구책임기관"],
                stage=trial["임상시험단계(연구모형)"],
                subjects_count=int(trial["전체목표연구대상자수"]) if trial["전체목표연구대상자수"] else 0,
                department=trial["진료과"]
            ),
            data
        ))
