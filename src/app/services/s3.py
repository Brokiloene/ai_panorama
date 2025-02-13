from typing import Any, BinaryIO, Mapping

import aioboto3
import botocore
import botocore.exceptions
import types_aiobotocore_s3

from app.config.s3 import s3_config
from app.config.system import logger
from app.exceptions import S3LoadError, S3NotFoundError


class S3Service:
    async def get_s3_client(self):
        session = aioboto3.Session()
        return session.client(  # type: ignore
            service_name=s3_config.service_name,
            endpoint_url=s3_config.endpoint_url,
            aws_access_key_id=s3_config.aws_access_key_id,
            aws_secret_access_key=s3_config.aws_secret_access_key,
            verify=s3_config.verify,
        )

    async def upload_object(
        self,
        client: types_aiobotocore_s3.Client,
        data: BinaryIO,
        bucket: str,
        object_name: str,
        content_type: str | None,
    ):
        """
        :raises `S3LoadError`:
        :raises `S3NotFoundError`:
        """
        try:
            if content_type is None:
                raise S3LoadError(
                    message="File Upload format is None",
                    bucket=bucket,
                    object_name=object_name,
                )
            await client.upload_fileobj(
                data, bucket, object_name, ExtraArgs={"ContentType": content_type}
            )
            logger.info(f"Object {object_name} uploaded")
        except botocore.exceptions.ClientError as exc:
            raise S3LoadError(
                message="S3 file upload error", bucket=bucket, object_name=object_name
            ) from exc

    async def download_object(
        self, client: types_aiobotocore_s3.Client, bucket: str, object_name: str
    ) -> Mapping[str, Any]:
        """
        :raises `S3LoadError`:
        :raises `S3NotFoundError`:
        """
        try:
            data = await client.get_object(Bucket=bucket, Key=object_name)
            logger.info(f"Object {object_name} downloaded")
        except botocore.exceptions.ClientError as exc:
            logger.error(f"S3 file load error: {exc} ({type(exc)})")
            if exc.response["Error"]["Code"] == "NoSuchKey":
                raise S3NotFoundError(
                    message="Could not find object with such key",
                    bucket=bucket,
                    object_name=object_name,
                ) from exc

            raise S3LoadError(
                message="Could not load object with such key",
                bucket=bucket,
                object_name=object_name,
            ) from exc
        return data
