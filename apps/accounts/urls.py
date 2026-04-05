from django.urls import path
from .views import RegisterView, DashboardView

app_name = 'accounts'

urlpatterns = [
    # AC-04: path /register/ per registrazione
    path('register/', RegisterView.as_view(), name='register'),
    # Dashboard post-registrazione
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]