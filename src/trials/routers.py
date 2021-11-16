from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from starlette import status

from src.dependencies import get_session_factory
from src.trials.application.services import TrialReadService
from src.trials.application.unit_of_work import SqlTrialUnitOfWork
from src.trials.domain import models
from src.trials.dto import TrialListParams, TrialViewData

router = APIRouter()


@router.get("/trials/{trial_id}", status_code=status.HTTP_200_OK, response_model=models.Trial)
def retrieve_trial(
        trial_id: str,
        session_factory=Depends(get_session_factory)
):
    service = TrialReadService(uow=SqlTrialUnitOfWork(session_factory))
    return service.get_trial(trial_id=trial_id)


@router.get("/list", status_code=status.HTTP_200_OK, response_model=Page[TrialViewData])
def list_trials(
        start: Optional[str] = None,
        end: Optional[str] = None,
        session_factory=Depends(get_session_factory)
):
    params = TrialListParams(
        start=datetime.strptime(start, "%Y-%m-%d %H:%M:%S") if start else None,
        end=datetime.strptime(end, "%Y-%m-%d %H:%M:%S") if end else None,
    )
    service = TrialReadService(uow=SqlTrialUnitOfWork(session_factory))
    return service.get_trials(params=params)
