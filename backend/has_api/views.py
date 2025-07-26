from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime


class BaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def success_response(self, message="", data=None, status_code=200):
        return Response(
            {"success": True, "message": message, "data": data}, status=status_code
        )

    def error_response(self, message="", data=None, status_code=400):
        return Response(
            {"success": False, "message": message, "data": data}, status=status_code
        )


class TestAPI(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        current_time = datetime.now().isoformat()
        return self.success_response(message="API is okay", data={"time": current_time})
