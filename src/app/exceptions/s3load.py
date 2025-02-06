from .s3base_error import S3BaseError

class S3LoadError(S3BaseError):
    def __str__(self):
        return f"S3LoadError: {self.message}, bucket: {self.bucket}, key: {self.object_name}"

