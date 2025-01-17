from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="", tags=["files"])


# Use File, bytes, and UploadFile to declare files to be uploaded in the request, sent as form data.
@router.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "fileb_content_type": fileb.content_type,
        "token": token,
    }


# upload files from fastapi
@router.post("/uploadfile")
async def create_upload_file(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filename": [file.filename for file in files]}


@router.get("/")
async def main():
    content = """
        <body>
            <form action="/files/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
            </form>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)
