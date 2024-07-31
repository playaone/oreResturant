import secrets
import os
from PIL import Image
from flask import current_app as app

def upload_image(picture):
    _, file_ext = os.path.splitext(picture.filename)
    secret_hex = secrets.token_hex(8)
    image_name = secret_hex + file_ext
    image_path = os.path.join(app.root_path, 'static/images/product', image_name)
    
    output_size = (250, 250)
    resized_image = Image.open(picture)

    output_image = resized_image.resize(output_size)

    output_image.save(image_path)

    return image_name