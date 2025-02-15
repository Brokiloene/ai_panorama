class AiAPITimeoutError(Exception):
    def __init__(self, action: str):
        self.action = action
        super().__init__(f"Timeout while waiting for {self.action}")
