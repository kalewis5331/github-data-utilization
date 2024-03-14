from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controller import repo_lang_controller, total_utilization_controller

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(repo_lang_controller.router)
app.include_router(total_utilization_controller.router)


@app.get("/")
async def root(request: Request):
    await repo_lang_controller.create_bar_chart()
    return templates.TemplateResponse(request=request, name="base.html")
