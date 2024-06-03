
import pydicom
from pydicom.errors import InvalidDicomError
import base64
import glob
import os
from constants import (DATA_DIR_PATH, DCM_EXT)

class AttributeHandler:
    def __init__(self):
        pass

    @classmethod
    def process_data_element_value(cls, value):
        if isinstance(value, bytes):
            # return base64 string instead of bytes
            return base64.b64encode(value).decode("utf-8")
        elif isinstance(value, pydicom.sequence.Sequence) and len(value) == 1:
            # a DataElement's value could contain a DataSet
            # return a list of header attribute dicts recursively
            ds = value[0]
            nested_header_attrs = []
            for data_elm in ds:
                nested_header_attrs.append(cls.get_data_element_dict(data_elm))
            return nested_header_attrs
        else:
            # return a string for values that are not yet defined
            return str(value)

    @classmethod
    def get_data_element_dict(cls, data_elm):
        return {
            "VR": data_elm.VR,
            "name": data_elm.name,
            "value": cls.process_data_element_value(data_elm.value),
        }

    @classmethod
    def get_header_attributes(cls, file_id, tag_group, tag_element):
        paths = glob.glob(os.path.join(DATA_DIR_PATH, f"*_{file_id}_*{DCM_EXT}"))
        if len(paths) > 0:
            file_path = paths[0]
            try:
                ds = pydicom.dcmread(file_path)
                data_elm = ds[tag_group, tag_element]
                return cls.get_data_element_dict(data_elm)
            except InvalidDicomError:
                raise InvalidDicomError("File is corrupted")
            except KeyError:
                raise KeyError("Tag not found")
            except Exception:
                return Exception
        else:
            raise FileNotFoundError("File not found")
