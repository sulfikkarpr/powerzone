from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth_router, users_router, plans_router, progress_router, payments_router, messaging_router, analytics_router

app = FastAPI(title=settings.app_name)

origins = settings.cors_origins if isinstance(settings.cors_origins, list) else [settings.cors_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = FastAPI()

app.include_router(auth_router.router, prefix=settings.api_prefix)
app.include_router(users_router.router, prefix=settings.api_prefix)
app.include_router(plans_router.router, prefix=settings.api_prefix)
app.include_router(progress_router.router, prefix=settings.api_prefix)
app.include_router(payments_router.router, prefix=settings.api_prefix)
app.include_router(messaging_router.router, prefix=settings.api_prefix)
app.include_router(analytics_router.router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    return {"status": "ok", "app": settings.app_name}