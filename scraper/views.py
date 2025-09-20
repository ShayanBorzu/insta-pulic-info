from django.http import JsonResponse
import requests
from .utils import get_instagram_profile
import requests, base64


def image_url_to_base64(url):
    response = requests.get(url)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        raise Exception(f"Failed to fetch image: {response.status_code}")

def profile_view(request, username, login_user='"scornfulporpoise', login_pass="@123qweasd"):
    login_user  = request.GET.get("login_user")
    login_pass  = request.GET.get("login_pass")
    data = get_instagram_profile(username)
    data["login"] = True
    
    if "error" in data:
        data = get_instagram_profile(username, login_user, login_pass)
        if "error" in data:
            return JsonResponse(data, status=400)

    # Add base64 version of profile picture
    profile_pic_url = data.get("profile_pic_url")
    if profile_pic_url:
        data["profile_pic_base64"] = image_url_to_base64(profile_pic_url)

    return JsonResponse(data)

def ipapi_view(request, ip=None):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return JsonResponse(data)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)