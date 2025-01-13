import base64, re
import aiofiles

import app.config as config

async def save_as_png(base64_data: str, filename: str) -> str:
    """
    :raises: binascii.Error
    """
    # Delete prefix data:image/png;base64,...
    base64_str = re.sub(r"^data:image\/[a-zA-Z]+;base64,", "", base64_data)
    raw_data = base64.b64decode(base64_str)

    file_path = f"{config.system.IMAGES_DIR}/{filename}.png"
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(raw_data)
    return file_path
    



