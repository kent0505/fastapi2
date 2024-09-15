from fastapi                  import FastAPI, Depends
from fastapi.middleware.cors  import CORSMiddleware
from fastapi.staticfiles      import StaticFiles
from src.core.jwt.jwt_handler import JwtAdmin, JwtCustomer
from src.core.utils           import lifespan
from src.core.config          import settings
from src.api.user             import router as user_router
from src.api.category         import router as category_router


app = FastAPI(
    lifespan               = lifespan,
    swagger_ui_parameters  = settings.swagger_ui,
)
app.add_middleware(
    middleware_class  = CORSMiddleware, 
    allow_origins     = settings.allow_origins, 
    allow_credentials = settings.allow_creds, 
    allow_methods     = settings.allow_methods, 
    allow_headers     = settings.allow_headers,
)
app.mount(
    app  = StaticFiles(directory=settings.static),
    path = settings.static_path,
)
app.mount(
    app  = StaticFiles(directory=settings.templates),
    path = settings.templates_path,
)
app.include_router(user_router,     prefix="/api/v1/user",     tags=["User"])
app.include_router(category_router, prefix="/api/v1/category", tags=["Category"], dependencies=[Depends(JwtAdmin()), Depends(JwtCustomer())])


# pip install -r requirements.txt
# cd Desktop/fullstack/blog && venv\Scripts\activate
# uvicorn src.main:app --reload
# sudo lsof -t -i tcp:8000 | xargs kill -9
# , dependencies=[Depends(JwtBearer())]