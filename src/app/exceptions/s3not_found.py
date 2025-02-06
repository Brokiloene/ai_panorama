from .s3base_error import S3BaseError

class S3NotFoundError(S3BaseError):
    def __str__(self):
        return f"S3NotFoundError: {self.message}, bucket: {self.bucket}, key: {self.object_name}"
