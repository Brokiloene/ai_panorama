import binascii

import app.config as config
from app.config.system import logger
from app.utils.base64_to_image import save_as_png


async def save_image_service(image: str, filename: str) -> str:
    if image:
        try:
            image_path = await save_as_png(base64_data=image, filename=filename)
            logger.info(f"Image {image_path} saved.")
        except binascii.Error as err:
            image_path = config.system.IMAGE_PLACEHOLDER
            logger.error(f"Could not save image: {err}")

    else:
        image_path = config.system.IMAGE_PLACEHOLDER
        logger.warning(f"Bad image: {image}")
    if image_path == config.system.IMAGE_PLACEHOLDER:
        logger.warning(f"Image {image_path} saved.")
        
    return image_path
    