from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import login


class AutoAuth:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user, c = User.objects.get_or_create(username='admin',
                                             defaults={"password": 'admin@1234', "is_superuser": True,
                                                       "is_staff": True})
        login(request, user)
        return self.get_response(request)
