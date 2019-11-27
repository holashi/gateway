# This module defines tools that gateway need, and the grpc/rest tools will be define specially. 
# 
# open_and_serialize_image(filename): 
#   Open an image file in base64 byte string. This string is used to create json when use rest api.
# 
# PIL2B64(PIL_img): 
#   Transform PIL image object to Base64 string
# 
# resize_and_serialize_image(filename,width,height): 
#   Resize image and transform into base64 string format



import base64
from PIL import Image
import io


# image tools :

def open_and_serialize_image(filename):
    with open(filename, "rb") as f:
        image = f.read()
    return base64.urlsafe_b64encode(image).decode('utf-8')

def PIL2B64(PIL_img):
    output_buffer = io.BytesIO()
    PIL_img.save(output_buffer, format='PNG')
    base64_str = base64.urlsafe_b64encode(output_buffer.getvalue())
    return base64_str

def resize_and_serialize_image(filename,width,height):
    image = Image.open(filename)
    image = image.resize((width, height), Image.BILINEAR)
    return PIL2B64(image)
 