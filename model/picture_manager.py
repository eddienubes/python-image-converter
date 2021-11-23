import numpy
from PIL import ImageTk, Image
from cv2 import cv2
import numpy as np


class PictureManager:
    def resize_image(self, bytes_array: numpy.array, width=400, height=400) -> numpy.array:
        return cv2.resize(bytes_array, (width, height), interpolation=cv2.INTER_AREA)

    def open(self, file_path):
        return np.flip(cv2.imread(file_path), axis=-1)

    def convert_to_photo_image(self, bytes_array: numpy.array):
        image = Image.fromarray(bytes_array.astype('uint8'), 'RGB')
        return ImageTk.PhotoImage(image)

    def brighten_image(self, image: numpy.array, brightness: float) -> numpy.array:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        v = hsv[:, :, 2]
        if brightness >= 1:
            v = np.where(v <= 255 - brightness, v + brightness, 255)
        else:
            v = v * brightness

        hsv[:, :, 2] = v

        brighten_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return brighten_image

    def save_image(self, path: str, image: numpy.array, img_format: str) -> None:
        if not path and img_format != 'png' and img_format != 'jpeg':
            return

        if img_format == 'jpeg':
            cv2.imwrite(path, np.flip(image, axis=-1), [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        if img_format == 'png':
            cv2.imwrite(path, np.flip(image, axis=-1))
