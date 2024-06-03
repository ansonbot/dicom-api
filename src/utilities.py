import uuid
import os
from constants import DATA_DIR_PATH

def get_uuid_hex():
    return str(uuid.uuid4().hex)

def clean_data_dir():
    for filename in os.listdir(DATA_DIR_PATH):
        os.remove(os.path.join(DATA_DIR_PATH, filename))
