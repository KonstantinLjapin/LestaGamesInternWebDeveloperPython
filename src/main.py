from typing import Annotated, Union
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from src.utils.text_worker import extract_keywords
app = FastAPI()


@app.get("/")
def read_root():
    return FileResponse("src/templates/index.html")


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    if file.content_type not in ["text/plain"]:
        raise HTTPException(400, detail="Invalid document type")
    if file.size > 100 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    out: dict = await extract_keywords(file)
    return {"filename": out}
