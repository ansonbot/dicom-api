from io import BytesIO
import os
from app import app

def test_file_upload_dicom_success():
    file_path = "src/tests/test_files/IM000001"
    with open(file_path, "rb") as fh:
        data = {"file": (BytesIO(fh.read()), os.path.basename(file_path))}
    resp = app.test_client().post(
        "/upload/dicom", 
        data=data, 
        content_type="multipart/form-data",
    )
    assert resp.status_code == 201

def test_file_upload_dicom_invalid_file():
    file_path = "src/tests/test_files/copy-data-pipeline.json"
    with open(file_path, "rb") as fh:
        data = {"file": (BytesIO(fh.read()), os.path.basename(file_path))}
    resp = app.test_client().post(
        "/upload/dicom", 
        data=data, 
        content_type="multipart/form-data",
    )
    assert resp.status_code == 400
