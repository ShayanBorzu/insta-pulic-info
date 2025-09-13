from django.http import JsonResponse
import requests
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

def ipapi_view(request, ip=None):

        response = requests.get(f"https://ipapi.co/{ip}/json/")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return JsonResponse(data)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)