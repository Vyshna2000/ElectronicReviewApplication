from social_core.exceptions import AuthAlreadyAssociated
from social_django.models import UserSocialAuth

def prevent_duplicate_social_account(backend, uid, user=None, *args, **kwargs):
    if user:
        existing_user = UserSocialAuth.objects.filter(provider=backend.name, uid=uid).exclude(user=user).first()
        if existing_user:
            raise AuthAlreadyAssociated(backend, "This Google account is already linked to another user.")
