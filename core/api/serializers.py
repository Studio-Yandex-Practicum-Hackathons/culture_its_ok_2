from rest_framework import serializers

from culture.models import Review, Exhibit, FeedBack, Route


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class ReviewReadSerializer(ReviewSerializer):
    exhibit = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Review
        fields = ('exhibit', 'username', 'userage', 'userhobby', 'text')


class ExhibitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exhibit
        exclude = ('id',)


class ExhibitReadSerializer(ReviewSerializer):
    route = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Exhibit
        fields = ('name', 'description', 'image', 'route')


class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        exclude = ('id',)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        exclude = ('id',)
