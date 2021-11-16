from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.configs.database import Base, engine
from src.trials.exception_handler import trial_not_found_exception_handler
from src.trials.exceptions import TrialNotFoundException
from src.trials.routers import router as trial_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(trial_router)

add_pagination(app)

app.add_exception_handler(TrialNotFoundException, trial_not_found_exception_handler)
