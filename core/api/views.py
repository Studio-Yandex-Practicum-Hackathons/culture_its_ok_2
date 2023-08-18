from culture.models import Exhibit, FeedBack, Route
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .serializers import (ExhibitSerializer, FeedBackSerializer,
                          ReviewSerializer, RouteSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        exhibit = get_object_or_404(Exhibit, pk=self.kwargs.get('exhibit_id'))
        return exhibit.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            exhibit=get_object_or_404(
                Exhibit, id=self.kwargs.get('exhibit_id')
            )
        )


class ExhibitViewSet(viewsets.ModelViewSet):
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class FeedBackViewSet(viewsets.ModelViewSet):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer
