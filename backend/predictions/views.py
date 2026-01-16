from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Prediction
from .serializers import PredictionSerializer
from .utils import predict_yield, generate_recommendations


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

    # Returns all predictions for the logged-in user, newest first, Including recommendations for each prediction.

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
    
    #Returns details for a single prediction, including recommendations.
    
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
