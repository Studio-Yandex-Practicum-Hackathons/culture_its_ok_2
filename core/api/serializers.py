from rest_framework import serializers

from culture.models import Comment, Exhibit, FeedBack, Route


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class CommentReadSerializer(CommentSerializer):
    exhibit = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Comment
        fields = ('exhibit', 'username', 'userage', 'userhobby', 'text')


class ExhibitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exhibit
        exclude = ('id',)


class ExhibitReadSerializer(CommentSerializer):
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
