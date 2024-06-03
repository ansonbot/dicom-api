import numpy as np
from PIL import Image

class ImageHandler:
    def __init__(self):
        pass

    @staticmethod
    def dicom_to_png(dicom_ds):
        pixel_arr = dicom_ds.pixel_array.astype(float)
        pixel_arr = (np.maximum(pixel_arr, 0) / pixel_arr.max()) * 255
        output_image = np.uint8(pixel_arr)
        output_image = Image.fromarray(output_image)
        return output_image
