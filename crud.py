from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas


def get_detail_trial_by_id(db: Session, trial_id: str):
    selected_trial = db.query(models.Trial).get(models.Trial.trial_id == trial_id)

    trial_data = [{
        "trial_id": selected_trial.trial_id,
        "name": selected_trial.name,
        "period": selected_trial.period,
        "scope": selected_trial.scope,
        "category": selected_trial.category,
        "institution": selected_trial.institution,
        "stage": selected_trial.stage,
        "subjects_count": selected_trial.subjects_count,
        "department": selected_trial.department
    }]
    
    return trial_data


def get_list_trial(db: Session, offset: int = 0, limit: int = 5, updated_at: datetime):
    today = datetime.date.today()
    diff_days = datetime.timedelta(days=7)

    selected_trials = db.query(models.Trial).filter(models.Trial.updated_at__range=['today', 'today - diff_days'])[offset:offset+limit]

    trial_infos = [{
        "trial_id": selected_trial.trial_id,
        "name": selected_trial.name,
        "period": selected_trial.period,
        "scope": selected_trial.scope,
        "category": selected_trial.category,
        "institution": selected_trial.institution,
        "stage": selected_trial.stage,
        "subjects_count": selected_trial.subjects_count,
        "department": selected_trial.department
    } for selected_trial in selected_trials]

    return trial_infos
