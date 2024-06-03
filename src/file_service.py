import os
import io
import glob
import pydicom
from pydicom.errors import InvalidDicomError
from datetime import datetime, timezone
from image_handler import ImageHandler             
from utilities import get_uuid_hex
from constants import (DATA_DIR_PATH, DCM_EXT, PNG_EXT)

class FileService:
	def __init__(self):
		pass

	@staticmethod
	def validate_dicom_file(file):
		if not file:
			return None
		file_bytes = io.BytesIO(file.read())
		file.seek(0)
		try:
			return pydicom.dcmread(file_bytes)
		except InvalidDicomError:
			return None
	
	@staticmethod
	def upload_dicom(file, dicom_ds=None):
		timestamp = datetime.now(timezone.utc).strftime(f"%Y%m%d%H%M%S")
		uuid = get_uuid_hex()
		file_name = f"{timestamp}_{uuid}_{file.filename}"
		dicom_path = os.path.join(DATA_DIR_PATH, f"{file_name}{DCM_EXT}")
		file.save(dicom_path)
		if dicom_ds is not None:
			png = ImageHandler.dicom_to_png(dicom_ds)
			png_path = os.path.join(DATA_DIR_PATH, f"{file_name}{PNG_EXT}")
			png.save(png_path)	
		return uuid

	@staticmethod
	def get_png_path(file_id):
		paths = glob.glob(os.path.join(DATA_DIR_PATH, f"*_{file_id}_*{PNG_EXT}"))
		if len(paths) > 0:
			return DATA_DIR_PATH, os.path.basename(paths[0])
		else:
			raise FileNotFoundError("File not found")
