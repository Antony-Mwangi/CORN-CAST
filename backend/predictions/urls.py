from django.urls import path
from .views import PredictionCreateView, PredictionListView, PredictionDetailView

urlpatterns = [
    path('create/', PredictionCreateView.as_view(), name='prediction-create'),
    path('history/', PredictionListView.as_view(), name='prediction-history'),
    path('<int:pk>/', PredictionDetailView.as_view(), name='prediction-detail'),
]
