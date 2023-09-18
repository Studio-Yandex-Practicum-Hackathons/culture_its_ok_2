from django.urls import include, path
from rest_framework import routers

from api.views import (ExhibitViewSet, FeedBackViewSet, ReviewViewSet,
                       RouteViewSet)

router = routers.DefaultRouter()
router.register('feedbacks', FeedBackViewSet, basename='feedbacks')
router.register('routes', RouteViewSet, basename='routes')
router.register('exhibits', ExhibitViewSet, basename='exhibits')
router.register(
    r'exhibits/(?P<exhibit_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
