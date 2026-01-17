from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

# ------------------------------
# Registration
# ------------------------------

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# ------------------------------
# Profile Retrieval & Update
# ------------------------------

class ProfileView(APIView):
    """
    Get logged-in user's profile info
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "welcome_message": f"Welcome {user.username} 👋"
        })


class UpdateProfileView(APIView):
    """
    Update logged-in user's profile info (username, email)
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.save()

        return Response({
            "username": user.username,
            "email": user.email,
            "message": "Profile updated successfully"
        })
