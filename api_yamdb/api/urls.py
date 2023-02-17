from api.views import (CommentViewSet, ReviewViewSet, SignUpView, TokenView,
                       UserViewSet)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(
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
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView, name='signup'),
    path('v1/auth/token/', TokenView, name='token'),
]
