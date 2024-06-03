from io import BytesIO
import os
import json
from app import app

def test_download_png_success():
    # upload a file to ensure data folder has a file
    file_path = "src/tests/test_files/IM000001"
    with open(file_path, "rb") as fh:
        data = {"file": (BytesIO(fh.read()), os.path.basename(file_path))}
    upload_resp = app.test_client().post(
        "/upload/dicom", 
        data=data, 
        content_type="multipart/form-data",
    )
    upload_resp_data = json.loads(upload_resp.data)
    
    # download png using the file id received from the previous call
    file_id = upload_resp_data.get("file_id")
    resp = app.test_client().get(
        f"/download/png/{file_id}"
    )
    assert resp.status_code == 200

def test_download_png_file_not_found():
    # fake file id
    file_id = "3e29d7e59dc8405c866d07c8db8884ab"
    resp = app.test_client().get(
        f"/download/png/{file_id}"
    )
    assert resp.status_code == 404
