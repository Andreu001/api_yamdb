from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""

    class Meta:
        model = User
        fields = '__all__'
