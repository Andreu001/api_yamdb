from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

router = DefaultRouter()

router.register('titles/(?P<title_id>\\d+)/rewiews',
                ReviewViewSet,
                basename='rewiews')
router.register(r'titles/(?P<title_id>\\d+)/rewiews/'
                r'(?P<title_id>\\d+)/comments',
                CommentViewSet,
                basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
