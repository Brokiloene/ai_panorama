import io

import aioboto3
import botocore
import botocore.exceptions
import types_aiobotocore_s3

import app.config as config
from app.exceptions import S3LoadError, S3NotFoundError
from app.config.system import logger

class S3Service:
    async def get_s3_client(self):
        session = aioboto3.Session()
        return session.client(
            **config.s3.client_config
        )
    
   
    async def upload_object(
        self,
        client: types_aiobotocore_s3.Client,
        data: io.BytesIO, 
        bucket: str, 
        object_name: str
    ):
        """
        :raises `S3LoadError`:
        :raises `S3NotFoundError`:
        """
        try:
            await client.upload_fileobj(
                data, 
                bucket, 
                object_name, 
                ExtraArgs={"ContentType": "image/png"}
            )
            logger.info(f"Object {object_name} uploaded")
        except botocore.exceptions.ClientError as e:
            logger.error(f"S3 file upload error: {e} ({type(e)})")
            raise S3LoadError(
                message=str(e), 
                bucket=bucket, 
                object_name=object_name
            )

    async def download_object(
        self, 
        client: types_aiobotocore_s3.Client,
        bucket: str, 
        object_name: str
    ) -> dict:
        """
        :raises `S3LoadError`:
        :raises `S3NotFoundError`:
        """
        try:
            data = await client.get_object(Bucket=bucket, Key=object_name)
            logger.info(f"Object {object_name} downloaded")
        except botocore.exceptions.ClientError as e:
            logger.error(f"S3 file load error: {e} ({type(e)})")
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise S3NotFoundError(
                    message=str(e), 
                    bucket=bucket, 
                    object_name=object_name
                )
            else:
                raise S3LoadError(
                    message=str(e), 
                    bucket=bucket, 
                    object_name=object_name
                )
        return data
