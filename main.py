from fastapi import FastAPI

from routers.business import router as business_router
from routers.services import router as service_router
from routers.appointments import router as appointment_router
from routers.auth import router as auth_router
from routers.refresh_token import router as refresh_token_router
from routers.users import router as users_router

from core.exception import (
    AppException,
    app_exception_handler,
    unhandled_exception_handler,
)

app = FastAPI(title="TerminToGo API")

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(business_router)
app.include_router(service_router)
app.include_router(appointment_router)
app.include_router(auth_router)
app.include_router(refresh_token_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "TerminToGo API is running"}