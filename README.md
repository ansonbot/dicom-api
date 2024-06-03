# DICOM API

## Installation (Windows)

1. Install Python. This repo was tested using version 3.10.6
2. Navigate to repo's root directory
3. Set up Python virtual environment `python -m venv .venv`
4. Install requirements `pip install -r requirements.txt` 

## Run Local Flask Server

1. Run `python src/app.py`
2. Browse to http://localhost:8080/swagger/ for using the API through Swagger UI

## Run Tests

1. Navigate to repo's root directory
2. Run `python -m pytest src/tests`

## VSCode Settings

Create `.vscode` folder, then add the following files:

**launch.json**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask",
            "type": "debugpy",
            "request": "launch",
            "console": "internalConsole",
            "stopOnEntry": false,
            "program": "${workspaceFolder}/src/app.py"
        }
    ]
}
```
**settings.json**
```json
{
    "python.testing.pytestArgs": [
        "src/tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "files.eol": "\n",
    "editor.rulers": [
        79,
        120
    ]
}
```

## API Endpoints

The base URL for the API is: http://localhost:5000

### Upload a DICOM File

Uploads a DICOM file to the server.

- **URL**: `/upload/dicom`
- **Method**: `POST`
- **Description**: Upload a DICOM file.
- **Consumes**: `multipart/form-data`
- **Produces**: `application/json`
- **Parameters**:
  - `file` (formData, required): The file to upload.
- **Success Response**:
  - **Code**: 201 Created
  - **Content**:
    ```json
    {
      "file_id": "a_hexadecimal_uuid"
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**:
    ```json
    {
      "error": "An error message"
    }
    ```

### Download a PNG File

Downloads a PNG file that was converted from a DICOM file.

- **URL**: `/download/png/{file_id}`
- **Method**: `GET`
- **Description**: Endpoint to download a file from the server.
- **Produces**: `application/octet-stream`
- **Parameters**:
  - `file_id` (path, required): The ID of the file to download.
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: Binary file data.
- **Error Responses**:
  - **Code**: 404 Not Found
  - **Content**:
    ```json
    {
      "error": "An error message"
    }
    ```

### Get DICOM Header Attributes

Returns the header attributes of a DICOM file by its ID and specified tag group and element.

- **URL**: `/header_attribute`
- **Method**: `GET`
- **Description**: Returns DICOM file's header attributes by ID.
- **Produces**: `application/json`
- **Parameters**:
  - `file_id` (query, required): The ID of the DICOM file.
  - `tag_group` (query, required): The tag group of the header attribute.
  - `tag_element` (query, required): The tag element of the header attribute.
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "header_attributes": {
        "VR": "value",
        "name": "value",
        "value": "value"
      }
    }
    ```
- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**:
    ```json
    {
      "error": "An error message"
    }
    ```
## Curl Requests

### Upload a DICOM File
```bash
curl -X POST http://localhost:5000/upload/dicom -F "file=@path/to/your/file.dcm"
```
### Download a PNG File
```bash
curl -X GET http://localhost:5000/download/png/{file_id}
```
### Get DICOM Header Attributes
```bash
curl -X GET "http://localhost:5000/header_attribute?file_id={file_id}&tag_group={tag_group}&tag_element={tag_element}"
```

## To Do List

Because this repo is a coding excercise, many features are not included. Here is a list of items that can be added to this Flask API:

- Security features, like authentication using JWT. A top priority for an API handling health care data. 
- Use a database and object storage instead of local directory.
- Add users. Each users can only access the DICOM files they uploaded.
- Containerization for production deployment.
- Add a build pipeline
- Add more tests, including unit tests