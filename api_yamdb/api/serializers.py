from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_oject_or_404
from rest_framework.relations import SlugRelatedField
from reviews.models import Comment, Review, Title

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_oject_or_404(Title, pk=title_id)
        # проверяем, хочет ли юзер отправить запрос на создание Отзыва
        if self.context['request'].user.method == 'POST':
            # проверяем есть ли отзыв у этого произведения
            # и принадлежит ли он автору запроса
            if Review.object.filter(title=title, pk=title_id):
                raise serializers.ValidationError(
                    'Нельзя добавить больше одного отзыва'
                )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    reviews = SlugRelatedField(
        slug_field='text', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
