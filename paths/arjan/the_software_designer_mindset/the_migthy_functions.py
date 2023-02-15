from dataclasses import dataclass
from typing import Callable
@dataclass
class User:
    id: int
    account_id: int
    shareable_profile_image_thumb: str


def check_diff_key_name(whh_key_name: str, user: User) -> bool:
    core_key_name = ""
    if user.shareable_profile_image_thumb:
        core_key_name = user.shareable_profile_image_thumb.split("/")[-1]
    return core_key_name != whh_key_name


def create_and_upload_profile_thumbnail(user, key_name):
    user.shareable_profile_image_thumb = 'https://thumbnail.cloudfront.net/' + key_name


def recreate_thumbs(check_diff_key_name: Callable[[User, str], bool], user=None, whh_key_name=None,
                    fix=False, ):
    if whh_key_name:
        whh_thumb = 'https://d2ncuau78u5vie.cloudfront.net/' + whh_key_name
    try:

        if not check_diff_key_name(whh_key_name, user) and not fix:
            return
        else:
            create_and_upload_profile_thumbnail(user, key_name=whh_key_name)
            thumbs_recreated = {"user_id": user.id, "core_thumb": user.shareable_profile_image_thumb,
                                "whh_thumb": whh_thumb}
            return thumbs_recreated
    except Exception as exc:
        return {"user_id": user.id, "thumb": exc, "key_name": whh_key_name}

if __name__ == "_main__":
    user = User(1, 1, "http://unadir/un_keyname")
    import ipdb;ipdb.set_trace()
    whh_key_name = "otro_keyname"
    thumb_creation = recreate_thumbs(check_diff_key_name, user, whh_key_name, fix=True)
    print("test")
