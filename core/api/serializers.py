from rest_framework import serializers

from culture.models import Exhibit, FeedBack, Review, Route


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        exclude = ('id',)


class ExhibitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exhibit
        exclude = ('id',)


class FeedBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBack
        exclude = ('id',)


class RouteSerializer(serializers.ModelSerializer):
    exhibite = ExhibitSerializer(read_only=True, many=True)

    class Meta:
        model = Route
        fields = ('name', 'description', 'image', 'exhibite',)
