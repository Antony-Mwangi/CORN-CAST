from django.urls import path
from .views import (
    PredictionCreateView,
    PredictionListView,
    PredictionDetailView,
    PredictionDeleteView,
    PredictionUpdateView,
    DashboardView,
)

urlpatterns = [
    path('create/', PredictionCreateView.as_view(), name='prediction-create'),
    path('history/', PredictionListView.as_view(), name='prediction-history'),
    path('<int:pk>/', PredictionDetailView.as_view(), name='prediction-detail'),
    path('<int:pk>/update/', PredictionUpdateView.as_view(), name='prediction-update'),
    path('<int:pk>/delete/', PredictionDeleteView.as_view(), name='prediction-delete'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
