from django.urls import path
from .views import profile_view

urlpatterns = [
    path('profile/<str:username>/', profile_view),
]

# GET  http://localhost:8000/api/profile/private_user/?login_user=  &login_pass=@1234@5678  -- private profile: if there is login infos
# GET  http://localhost:8000/api/profile/natgeo -- public profile: without login info