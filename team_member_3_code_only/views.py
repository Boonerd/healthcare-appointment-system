
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAuthenticatedWithRole

@api_view(["GET"])
@permission_classes([IsAuthenticatedWithRole(["patient"])])
def patient_dashboard(request):
    return Response({"message": f"Welcome, {request.user_payload['sub']}! You are a patient."})
