from django.urls import path
from .views import RegisterView, DashboardView, LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    # AC-04: path /register/ per registrazione
    path('register/', RegisterView.as_view(), name='register'),
    # Story 1.3: Login e Logout
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Dashboard post-registrazione
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
