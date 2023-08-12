from django.shortcuts import get_object_or_404
from culture.models import Exhibit, FeedBack, Route
from rest_framework import viewsets

from .serializers import (
    ReviewSerializer,
    ReviewReadSerializer,
    ExhibitSerializer,
    ExhibitReadSerializer,
    FeedBackSerializer,
    RouteSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        exhibit = get_object_or_404(Exhibit, pk=self.kwargs.get('exhibit_id'))
        return exhibit.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            exhibit=get_object_or_404(
                Exhibit, id=self.kwargs.get('exhibit_id')
            )
        )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReviewReadSerializer
        return ReviewSerializer


class ExhibitViewSet(viewsets.ModelViewSet):
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ExhibitReadSerializer
        return ExhibitSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class FeedBackViewSet(viewsets.ModelViewSet):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer
