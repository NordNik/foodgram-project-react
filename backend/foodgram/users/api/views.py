from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from .serializers import (
    UsersSerializer, MyTokenObtainPairSerializer, RegisterSerializer)
from .paginator import UsersPagination
from .permissions import IsAutheticatedOrRegistration

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = UsersPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RegisterSerializer
        return UsersSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


'''class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny, )'''


'''
Настроил токен, теперь нужно доработать пермишен. Сейчас он дает тру только если метод пост. В остальных запросах ВСЕГДА фальш'''