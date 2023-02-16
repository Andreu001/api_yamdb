from django.urls import include, path
from rest_framework import routers
from api.views import UserViewSet, SignUpView, TokenView

v1_router = routers.DefaultRouter()
v1_router.register(
    r'users',
    UserViewSet,
    basename='users'
)
router.register('titles/(?P<title_id>\\d+)/rewiews',
                ReviewViewSet,
                basename='rewiews')
router.register(r'titles/(?P<title_id>\\d+)/rewiews/'
                r'(?P<title_id>\\d+)/comments',
                CommentViewSet,
                basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignUpView, name='signup'),
    path('v1/auth/token/', TokenView, name='token'),
