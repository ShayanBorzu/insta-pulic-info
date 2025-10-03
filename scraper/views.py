from django.http import JsonResponse, HttpResponseBadRequest
import requests
from .utils import get_instagram_profile , image_url_to_base64



def profile_view(request, username):
    # Call the utility that tries multiple session files, then optional login fallback
    data = get_instagram_profile(username)

    # Surface utility errors as HTTP 400 for clarity
    if isinstance(data, dict) and "error" in data:
        return HttpResponseBadRequest(data["error"])

    # Optionally embed profile picture as base64 to keep a single JSON payload
    profile_pic_url = data.get("profile_pic_url")
    if profile_pic_url:
        try:
            data["profile_pic_base64"] = image_url_to_base64(str(profile_pic_url))
        except Exception as e:
            # Do not fail the entire request if image fetch fails; just report the issue
            data["profile_pic_base64_error"] = str(e)

    return JsonResponse(data)


def ipapi_view(request, ip=None):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return JsonResponse(data)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)