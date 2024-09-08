

class ApiResponse:
    def __init__(self, status, message=None, data=None):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        response = {"status": self.status}
        if self.message is not None:
            response["message"] = self.message
        if self.data is not None:
            response["data"] = self.data
        return response
