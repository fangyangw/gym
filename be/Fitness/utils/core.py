from rest_framework.authentication import BaseAuthentication
from Fitness.models import UserProfile
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.permissions import BasePermission


class OpenIDAuthentication(BaseAuthentication):

    def authenticate(self, request):
        open_id = request.data.get("open_id")
        user = UserProfile.objects.filter(open_id=open_id).first()
        if not user:
            raise exceptions.AuthenticationFailed(_('Invalid open_id.'))
        return user, None


class IsOpenIDAuthentication(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        open_id = request.data.get("open_id")
        user = UserProfile.objects.filter(openid=open_id).first()
        return bool(user)
