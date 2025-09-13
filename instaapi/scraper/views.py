from django.http import JsonResponse
import requests
from .utils import get_instagram_profile


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         # May contain multiple IPs if behind multiple proxies
#         ip = x_forwarded_for.split(',')[0].strip()
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


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

def ipapi_view(request, ip=None):


    try:
        if ip == None:
            ip = request.META.get('REMOTE_ADDR')

        response = requests.get(f"https://ipapi.co/{ip}/json/")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return JsonResponse(data)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)