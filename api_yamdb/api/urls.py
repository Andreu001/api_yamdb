from django.urls import include, path
from rest_framework import routers
from api.views import UserViewSet, SignUpViewSet

v1_router = routers.DefaultRouter()
v1_router.register(
    r'users',
    UserViewSet,
    basename='users'
)
v1_router.register(
    r'auth/signup',
    SignUpViewSet
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
