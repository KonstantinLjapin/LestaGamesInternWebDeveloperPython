from typing import Annotated, Union
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
app = FastAPI()


@app.get("/")
def read_root():
    return FileResponse("src/templates/index.html")


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

