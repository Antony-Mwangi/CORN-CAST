from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Prediction
from .serializers import PredictionSerializer
from .utils import predict_yield, generate_recommendations


# ------------------------------
# Prediction CRUD
# ------------------------------

class PredictionCreateView(generics.CreateAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Override create() to calculate yield and recommendations
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


class PredictionListView(APIView):
    """
    Returns all predictions for the logged-in user, newest first,
    including recommendations for each prediction.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
        response_list = []

        for pred in predictions:
            serializer = PredictionSerializer(pred)
            data = serializer.data
            data['recommendations'] = generate_recommendations(
                pred.nitrogen, pred.phosphorus, pred.potassium, pred.ph
            )
            response_list.append(data)

        return Response(response_list)


class PredictionDetailView(APIView):
    """
    Returns details for a single prediction, including recommendations.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            pred = Prediction.objects.get(pk=pk, user=request.user)
        except Prediction.DoesNotExist:
            return Response({"detail": "Prediction not found."}, status=404)

        serializer = PredictionSerializer(pred)
        data = serializer.data
        data['recommendations'] = generate_recommendations(
            pred.nitrogen, pred.phosphorus, pred.potassium, pred.ph
        )
        return Response(data)


class PredictionDeleteView(APIView):
    """
    Delete a prediction by ID
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            pred = Prediction.objects.get(pk=pk, user=request.user)
            pred.delete()
            return Response({"message": "Prediction deleted successfully"})
        except Prediction.DoesNotExist:
            return Response({"detail": "Prediction not found"}, status=404)


class PredictionUpdateView(APIView):
    """
    Update a prediction by ID (inputs only; recalculates yield & recommendations)
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            pred = Prediction.objects.get(pk=pk, user=request.user)
        except Prediction.DoesNotExist:
            return Response({"detail": "Prediction not found"}, status=404)

        data = request.data

        # Update fields if provided
        pred.rainfall = float(data.get('rainfall', pred.rainfall))
        pred.temperature = float(data.get('temperature', pred.temperature))
        pred.nitrogen = float(data.get('nitrogen', pred.nitrogen))
        pred.phosphorus = float(data.get('phosphorus', pred.phosphorus))
        pred.potassium = float(data.get('potassium', pred.potassium))
        pred.ph = float(data.get('ph', pred.ph))
        pred.seed_variety = data.get('seed_variety', pred.seed_variety)

        # Recalculate yield
        pred.yield_prediction = predict_yield(
            pred.rainfall, pred.temperature,
            pred.nitrogen, pred.phosphorus, pred.potassium, pred.ph
        )

        pred.save()

        serializer = PredictionSerializer(pred)
        response_data = serializer.data
        response_data['recommendations'] = generate_recommendations(
            pred.nitrogen, pred.phosphorus, pred.potassium, pred.ph
        )

        return Response(response_data)


# ------------------------------
# Dashboard
# ------------------------------

class DashboardView(APIView):
    """
    Returns user dashboard with profile info, predictions, and stats
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        predictions = Prediction.objects.filter(user=user).order_by('-created_at')

        serialized_predictions = []
        for pred in predictions:
            data = PredictionSerializer(pred).data
            data['recommendations'] = generate_recommendations(
                pred.nitrogen, pred.phosphorus, pred.potassium, pred.ph
            )
            serialized_predictions.append(data)

        latest_prediction = predictions.first()

        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
                "welcome_message": f"Welcome {user.username} 👋"
            },
            "stats": {
                "total_predictions": predictions.count(),
                "latest_yield": latest_prediction.yield_prediction if latest_prediction else None
            },
            "predictions": serialized_predictions
        })
