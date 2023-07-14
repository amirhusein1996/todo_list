from django.http import HttpRequest
from .models import UserExtraInfo

def user_profile_picture(request:HttpRequest):
    """
    if user is authenticated and has avatar , it will return avatar to template as a context
    otherwise None
    """
    if request.user.is_authenticated:

        user_avatar = UserExtraInfo.objects.filter(
                user=request.user,
                avatar__isnull=False
            ).only('avatar').first()
        if user_avatar:
            return {
                    'avatar' : user_avatar.avatar
                }

        "alternative way: to use get instead of filter"
        # try:
        #     user_extra_info = UserExtraInfo.objects.get(
        #         user=request.user,
        #         avatar__isnull=False
        #     )
        #
        #     return {
        #         'avatar' : user_extra_info.avatar
        #     }
        # except UserExtraInfo.DoesNotExist:
        #     pass

    return {}