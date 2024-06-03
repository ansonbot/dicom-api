# from crypt import methods
from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from file_service import FileService
from attribute_handler import AttributeHandler
from constants import GENERIC_ERROR_MSG

app = Flask(__name__)
SWAGGER_URL="/swagger"
API_URL="/static/swagger.yml"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'DICOM API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def home():
    # endpoint to test if the API works
    return jsonify({
        "message": "App up and running successfully"
    })

@app.route("/upload/dicom",methods=["POST"])
def upload_dicom():
    file = request.files.get("file")
    # get dicom file dataset for generating png
    dicom_ds = FileService.validate_dicom_file(file)
    if dicom_ds is not None:
        file_id = FileService.upload_dicom(file, dicom_ds)
        return jsonify({
            "file_id":  file_id
        }), 201
    else:
        return jsonify({
            "error": "Invalid file"
        }), 400

@app.route("/download/png/<file_id>", methods=["GET"])
def download_png(file_id):        
    try:
        file_dir, file_name = FileService.get_png_path(file_id)
        # send image to client and display directly
        return send_from_directory(file_dir, file_name, as_attachment=False)
    # file id not found
    except FileNotFoundError as e:
        err_msg = e.args[0] if len(e.args) > 0 else GENERIC_ERROR_MSG
        return jsonify({
            "error": err_msg
        }), 404

@app.route("/header_attribute", methods=["GET"])
def header_attribute():
    file_id = request.args.get('file_id', "")
    tag_group = request.args.get("tag_group", "")
    tag_element = request.args.get("tag_element", "")
    # query string is incorrect
    if len(file_id) == 0 or len(tag_group) == 0 or len(tag_element) == 0:
        return jsonify({
            "error": "Invalid file id or tags"
        }), 400
    else:
        try:
            attr_dict = AttributeHandler.get_header_attributes(file_id, tag_group, tag_element)
            return jsonify({
                "header_attribute": attr_dict
            }), 200
        # file or tags not found
        except (FileNotFoundError, KeyError) as e:
            err_msg = e.args[0] if len(e.args) > 0 else GENERIC_ERROR_MSG
            return jsonify({
                "error": err_msg
            }), 404
        # just in case of any other errors
        except Exception as e:
            err_msg = e.args[0] if len(e.args) > 0 else GENERIC_ERROR_MSG
            return jsonify({
                "error": err_msg
            }), 400

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)
