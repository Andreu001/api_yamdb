from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, signup, TitleViewSet, get_token,
                       UserViewSet)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(
    r'users',
    UserViewSet,
    basename='users'
)
router.register('titles/(?P<title_id>\\d+)/reviews',
                ReviewViewSet,
                basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/'
                r'(?P<review_id>\d+)/comments',
                CommentViewSet,
                basename='comments')
router.register(r'titles', TitleViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
