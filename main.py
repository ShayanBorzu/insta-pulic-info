import instaloader

# Initialize Instaloader with media download disabled
L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    save_metadata=False,
    compress_json=False
)

# Optional: Log in for private profiles
# L.login("your_username", "your_password")

# Target profile
username = "instagram_username"
profile = instaloader.Profile.from_username(L.context, 'itsnimaprs')

# Extract desired info
print("Username:", profile.username)
print("Full Name:", profile.full_name)
print("Bio:", profile.biography)
print("Followers:", profile.followers)
print("Following:", profile.followees)
print("Posts:", profile.mediacount)
print("Profile Picture URL:", profile.profile_pic_url)