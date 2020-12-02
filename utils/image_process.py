import cv2
import urllib
import numpy as np
import os
import platform
# import dlib
import base64


def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)

    # otherwise, the image does not reside on disk
    else:   
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.request.urlopen(url)
            data = resp.read()
 
        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()
 
        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
    # return the image
    return image


def _save_image(image_detail_filename, file_dir, file_obj, file_ext):
    if "Windows" in platform.platform() and "/" in file_dir:
        file_dir = file_dir.replace('/', '\\')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_dir+image_detail_filename+file_ext,'wb+') as file:
        for chunk in file_obj.chunks():
            file.write(chunk)
    image_detail_upload = os.path.join(file_dir, image_detail_filename+file_ext)
    return image_detail_upload

def image_to_base64(img):
    if isinstance(img, str):
        img = cv2.imread(img)
    else:
        pass

    image = cv2.imencode('.jpg', img)[1]
    image_encode = str(base64.b64encode(image))[2:-1]

    return image_encode