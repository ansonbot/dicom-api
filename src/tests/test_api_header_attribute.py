import pytest
from io import BytesIO
import os
import json
from app import app

@pytest.fixture
def file_id():
    # upload a file to ensure data folder has a file
    file_path = "src/tests/test_files/IM000001"
    with open(file_path, "rb") as fh:
        data = {"file": (BytesIO(fh.read()), os.path.basename(file_path))}
    resp = app.test_client().post(
        "/upload/dicom", 
        data=data, 
        content_type="multipart/form-data",
    )
    resp_data = json.loads(resp.data)
    file_id = resp_data.get("file_id", "")
    return file_id

@pytest.mark.usefixtures("file_id")
def test_header_attribute_success(file_id):
    # get header attribute using the file id received from the previous call
    resp = app.test_client().get(
        f"/header_attribute?file_id={file_id}&tag_group=10&tag_element=10"
    )
    assert resp.status_code == 200

def test_header_attribute_invalid_input():
    file_id = ""
    resp = app.test_client().get(
        f"/header_attribute?file_id={file_id}&tag_group=10&tag_element=10"
    )
    resp_data = json.loads(resp.data)
    msg = resp_data.get("error", "")
    assert msg == "Invalid file id or tags"
    assert resp.status_code == 400

def test_header_attribute_file_not_found():
    file_id = "made_up_file_id"
    resp = app.test_client().get(
        f"/header_attribute?file_id={file_id}&tag_group=10&tag_element=10"
    )
    resp_data = json.loads(resp.data)
    msg = resp_data.get("error", "")
    assert msg == "File not found"
    assert resp.status_code == 404

@pytest.mark.usefixtures("file_id")
def test_header_attribute_tag_not_found(file_id):
    resp = app.test_client().get(
        f"/header_attribute?file_id={file_id}&tag_group=0&tag_element=0"
    )
    resp_data = json.loads(resp.data)
    msg = resp_data.get("error", "")
    assert msg == "Tag not found"
    assert resp.status_code == 404