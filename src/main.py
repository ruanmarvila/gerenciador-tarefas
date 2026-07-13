from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.exceptions import ModelError
from src.tasks.router import router as task_router
from src.users.routers import auth_router, user_router

app = FastAPI(
    title="Task Manager",
    version="1.0.0",
    description="Task management API"
)

@app.exception_handler(ModelError)
async def model_error_handler(request: Request, exc: ModelError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)