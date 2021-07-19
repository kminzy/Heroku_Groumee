from django.urls import path
from groupmeet import views
from .views import *

urlpatterns = [
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="signup"),
]