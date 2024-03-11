from fastapi import FastAPI

from controller import repo_lang_controller

app = FastAPI()

app.include_router(repo_lang_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
