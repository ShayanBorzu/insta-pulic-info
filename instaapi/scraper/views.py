from django.http import JsonResponse
from .utils import get_instagram_profile

def profile_view(request, username):
    # Read credentials from GET or POST
    login_user = (
        request.GET.get("login_user")
        or request.POST.get("login_user")
    )
    login_pass = (
        request.GET.get("login_pass")
        or request.POST.get("login_pass")
    )
    
    data = get_instagram_profile(username, login_user, login_pass)

    if "error" in data:
        return JsonResponse(data, status=400)
    return JsonResponse(data)