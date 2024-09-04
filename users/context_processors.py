from main.models import UserProfile

def user_profile_context(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        return {'user_profile': user_profile}
    return {}