from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controller import repo_lang_controller

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(repo_lang_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
