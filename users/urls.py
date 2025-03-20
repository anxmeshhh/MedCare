from django.urls import path
from .views import login_view, dashboard_view, redirect_to_login

urlpatterns = [
    path('', redirect_to_login, name='root'),  # ✅ Redirect root to login
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
