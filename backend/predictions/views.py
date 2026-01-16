from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Prediction
from .serializers import PredictionSerializer
from .utils import predict_yield, generate_recommendations


class PredictionCreateView(generics.CreateAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Override create() to calculate yield and recommendations
        """
        data = request.data

        # Convert inputs to float
        rainfall = float(data.get('rainfall', 0))
        temperature = float(data.get('temperature', 0))
        nitrogen = float(data.get('nitrogen', 0))
        phosphorus = float(data.get('phosphorus', 0))
        potassium = float(data.get('potassium', 0))
        ph = float(data.get('ph', 0))
        seed_variety = data.get('seed_variety', '')

        # Calculate yield
        predicted_yield = predict_yield(
            rainfall=rainfall,
            temperature=temperature,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            ph=ph
        )

        # Generate recommendations
        recommendations = generate_recommendations(nitrogen, phosphorus, potassium, ph)

        # Save prediction
        prediction = Prediction.objects.create(
            user=request.user,
            rainfall=rainfall,
            temperature=temperature,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            ph=ph,
            seed_variety=seed_variety,
            yield_prediction=predicted_yield
        )

        # Serialize and return data with recommendations
        serializer = self.get_serializer(prediction)
        response_data = serializer.data
        response_data['recommendations'] = recommendations

        return Response(response_data)


class PredictionListView(generics.ListAPIView):
    # Returns all predictions for the logged-in user, newest first.
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user).order_by('-created_at')


class PredictionDetailView(generics.RetrieveAPIView):

    # Returns details for a single prediction.

    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)
