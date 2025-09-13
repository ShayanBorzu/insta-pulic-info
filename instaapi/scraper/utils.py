import instaloader
from instaloader.exceptions import LoginRequiredException, BadCredentialsException

def get_instagram_profile(username, login_user=None, login_pass=None):
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        save_metadata=False,
        compress_json=False
    )

    # Perform login only if credentials are provided
    if login_user and login_pass:
        try:
            L.login(login_user, login_pass)
        except BadCredentialsException:
            return {"error": "Invalid login credentials"}

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "profile_pic_url": profile.profile_pic_url
        }

    except LoginRequiredException:
        return {"error": "Login required to access this profile"}
    except Exception as e:
        return {"error": str(e)}