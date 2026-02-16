import mimetypes

from starlette.responses import JSONResponse

custom_mimetype = mimetypes.add_type("application/javascript", ".js", True)

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, HTTPException, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from Models.DbContext import DbContext
from Routes.RessourcesRouter import RessourcesRouter
from Routes.VoitureRouter import VoitureRouter
from Services.RessourcesService import RessourceService
from Services.VoitureService import VoitureService

DB_FILENAME = './Database/db.sqlite'
RESSOURCE_FILENAME = 'Ressources/ressources.json'
API_LINK = "/api"

dbContext = DbContext(DB_FILENAME)
app = FastAPI()
app.include_router(VoitureRouter(VoitureService(dbContext), API_LINK).router)
app.include_router(RessourcesRouter(RessourceService(RESSOURCE_FILENAME), API_LINK).router)

app.mount("/static", StaticFiles(directory="www/static"), name="static")


templates = Jinja2Templates(directory="www")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.exception_handler(StarletteHTTPException)
async def unicorn_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404 and API_LINK not in request.url.path:  # pass to frontend
        return templates.TemplateResponse(name="index.html", request=request, context= {"initial_status_code": 404},
                                          status_code=404)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
