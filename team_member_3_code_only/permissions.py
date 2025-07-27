
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from .auth_utils import decode_access_token

class IsAuthenticatedWithRole(BasePermission):
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request: Request, view):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return False
        token = auth_header.split(" ")[1]
        payload = decode_access_token(token)
        if not payload or payload.get("role") not in self.allowed_roles:
            return False
        request.user_payload = payload
        return True
