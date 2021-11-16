from starlette import status
from starlette.responses import JSONResponse


def trial_not_found_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})
