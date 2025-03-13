from unittest.mock import AsyncMock

import botocore
import botocore.exceptions
import pytest
import types_aiobotocore_s3

from app.services.s3 import S3LoadError, S3NotFoundError, S3Service


@pytest.fixture
def s3_service() -> S3Service:
    return S3Service()


async def test_upload_object_success(s3_service):
    mock_client = AsyncMock(spec_set=types_aiobotocore_s3.Client)
    mock_client.upload_fileobj = AsyncMock()
    mock_data = AsyncMock()

    await s3_service.upload_object(
        client=mock_client,
        data=mock_data,
        bucket="test-bucket",
        object_name="test.txt",
        content_type="text/plain",
    )

    mock_client.upload_fileobj.assert_awaited_once_with(
        mock_data, "test-bucket", "test.txt", ExtraArgs={"ContentType": "text/plain"}
    )


async def test_upload_object_no_contenttype_error(s3_service):
    mock_client = AsyncMock(spec_set=types_aiobotocore_s3.Client)
    mock_client.upload_fileobj = AsyncMock()
    mock_data = AsyncMock()

    with pytest.raises(S3LoadError, match="File Upload format is None"):
        await s3_service.upload_object(
            client=mock_client,
            data=mock_data,
            bucket="test-bucket",
            object_name="test.txt",
            content_type=None,
        )


async def test_upload_object_error(s3_service):
    mock_client = AsyncMock(spec_set=types_aiobotocore_s3.Client)
    mock_client.upload_fileobj.side_effect = botocore.exceptions.ClientError(
        error_response={"Error": {"Code": "400", "Message": "Test Error"}},
        operation_name="UploadFile",
    )
    mock_data = AsyncMock()

    with pytest.raises(S3LoadError, match="S3 file upload error"):
        await s3_service.upload_object(
            client=mock_client,
            data=mock_data,
            bucket="test-bucket",
            object_name="test.txt",
            content_type="text/plain",
        )


async def test_download_object_success(s3_service):
    mock_client = AsyncMock(spec_set_set=types_aiobotocore_s3.Client)
    mock_client.get_object = AsyncMock()
    mock_client.get_object.return_value = {"test data": "test value"}

    res = await s3_service.download_object(mock_client, "test bucket", "test.txt")

    mock_client.get_object.assert_awaited_once_with(
        Bucket="test bucket", Key="test.txt"
    )
    assert res == {"test data": "test value"}


async def test_download_object_error_not_found(s3_service):
    mock_client = AsyncMock(spec_set_set=types_aiobotocore_s3.Client)
    mock_client.get_object = AsyncMock()
    mock_client.get_object.side_effect = botocore.exceptions.ClientError(
        error_response={"Error": {"Code": "NoSuchKey", "Message": "Test Error"}},
        operation_name="DownloadFile",
    )

    with pytest.raises(S3NotFoundError, match="Could not find object with such key"):
        await s3_service.download_object(mock_client, "test bucket", "test.txt")


async def test_download_object_error_load_error(s3_service):
    mock_client = AsyncMock(spec_set_set=types_aiobotocore_s3.Client)
    mock_client.get_object = AsyncMock()
    mock_client.get_object.side_effect = botocore.exceptions.ClientError(
        error_response={"Error": {"Code": "400", "Message": "Test Error"}},
        operation_name="DownloadFile",
    )

    with pytest.raises(S3LoadError, match="Could not load object with such key"):
        await s3_service.download_object(mock_client, "test bucket", "test.txt")
