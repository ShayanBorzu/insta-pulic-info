from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<str:username>/', profile_view),
    path('ipapi/<str:ip>/', ipapi_view),
    path('ipapi/', ipapi_view),
    
]

# GET  http://localhost:8000/api/profile/private_user/?login_user=username&login_pass=password  -- private profile: if there is login infos (doesn't work, yet.)
# GET  http://localhost:8000/api/profile/natgeo -- public profile: without login info