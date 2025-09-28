from rest_framework.exceptions import APIException
from rest_framework import status


class UserAgreementsRequiredException(APIException):
    status_code = status.HTTP_428_PRECONDITION_REQUIRED

    def __init__(self, required_agreements):
        self.detail = {
            'message': 'You must accept the latest agreements to continue',
            'required_agreements': required_agreements
        }