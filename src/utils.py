import base64

import os



def image_to_base64(image_path):

    """Resim dosyasını Base64 string'e çevirir (Export için)"""

    if not os.path.exists(image_path):

        return None

    try:

        with open(image_path, "rb") as img_file:

            return base64.b64encode(img_file.read()).decode('utf-8')

    except Exception as e:

        print(f"Image conversion error: {e}")

        return None



def base64_to_image(base64_string, save_path):

    """Base64 string'i resim dosyasına çevirir (Import için)"""

    try:

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        

        with open(save_path, "wb") as img_file:

            img_file.write(base64.b64decode(base64_string))

        return True

    except Exception as e:

        print(f"Image save error: {e}")

        return False