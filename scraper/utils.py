import os
import instaloader
from instaloader.exceptions import LoginRequiredException, BadCredentialsException
from typing import List, Dict, Optional
import requests
import base64


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(PROJECT_ROOT, "ig_sessions")

# Define sessions stored inside ./ig_sessions/
SESSION_ROTATION: List[Dict[str, str]] = [
    {"username": "ali.jfry7", "sessionfile": os.path.join(SESSIONS_DIR, "session-ali.jfry7")},
    {"username": "candyandif", "sessionfile": os.path.join(SESSIONS_DIR, "session-candyandif")},
    {"username": "kurdingc", "sessionfile": os.path.join(SESSIONS_DIR, "session-kurdingc")},
]

def _new_loader() -> instaloader.Instaloader:
    return instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        save_metadata=False,
        compress_json=False,
    )

def _try_with_session(target_username: str, session_user: str, sessionfile: str) -> Optional[dict]:
    L = _new_loader()
    try:
        L.load_session_from_file(session_user, sessionfile)
        profile = instaloader.Profile.from_username(L.context, target_username)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "profile_pic_url": profile.profile_pic_url,
        }
    except Exception:
        return None
    finally:
        try:
            L.close()
        except Exception:
            pass

def get_instagram_profile(username, login_user=None, login_pass=None):
    # won't create files, just the folder
    os.makedirs(SESSIONS_DIR, exist_ok=True)

    # 1) Try rotating pre-saved session files in ./ig_sessions/
    for cred in SESSION_ROTATION:
        data = _try_with_session(username, cred["username"], cred["sessionfile"])
        if data is not None:
            return data

    # 2) Optional fallback to live login if credentials provided
    L = _new_loader()
    if login_user and login_pass:
        try:
            L.login(login_user, login_pass)
        except BadCredentialsException:
            return {"error": "Invalid login credentials"}
        except Exception as e:
            return {"error": f"Login failed: {e}"}

        try:
            profile = instaloader.Profile.from_username(L.context, username)
            return {
                "username": profile.username,
                "full_name": profile.full_name,
                "bio": profile.biography,
                "followers": profile.followers,
                "following": profile.followees,
                "posts": profile.mediacount,
                "profile_pic_url": profile.profile_pic_url,
            }
        except LoginRequiredException:
            return {"error": "Login required to access this profile"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            try:
                L.close()
            except Exception:
                pass

    # 3) No working session and no credentials provided
    return {"error": "All sessions failed and no credentials provided"}


def image_url_to_base64(url: str) -> str:
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        return base64.b64encode(resp.content).decode("utf-8")
    raise Exception(f"Failed to fetch image: {resp.status_code}")