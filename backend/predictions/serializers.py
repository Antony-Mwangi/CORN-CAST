from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'
        read_only_fields = ['user', 'yield_prediction', 'created_at']