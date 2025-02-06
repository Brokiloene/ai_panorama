class S3BaseError(Exception):
    def __init__(self, message: str, bucket: str, object_name: str):
        super().__init__(message)
        self.bucket: str = bucket
        self.object_name :str = object_name
