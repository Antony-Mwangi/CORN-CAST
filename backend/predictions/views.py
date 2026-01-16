from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Prediction
from .serializers import PredictionSerializer
from .utils import predict_yield


class PredictionCreateView(generics.CreateAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Calculate AI yield and save the prediction.
        data = self.request.data

        # Ensure we convert inputs to float
        rainfall = float(data.get('rainfall', 0))
        temperature = float(data.get('temperature', 0))
        nitrogen = float(data.get('nitrogen', 0))
        phosphorus = float(data.get('phosphorus', 0))
        potassium = float(data.get('potassium', 0))
        ph = float(data.get('ph', 0))

        # Get predicted yield
        predicted_yield = predict_yield(
            rainfall=rainfall,
            temperature=temperature,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            ph=ph
        )

        # Save prediction with user
        serializer.save(user=self.request.user, yield_prediction=predicted_yield)


class PredictionListView(generics.ListAPIView):
    """
    Returns all predictions for the logged-in user, newest first.
    """
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user).order_by('-created_at')


class PredictionDetailView(generics.RetrieveAPIView):
    """
    Returns details for a single prediction.
    """
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)
