from rest_framework import serializers
from auth_app.serializers import UserSerializer
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = (
            'uuid',
            'title',
            'content',
            'owner',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'uuid',
            'owner',
            'created_at',
            'updated_at',
        )


    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Le titre est requis")
        return value

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Le contenu est requis")

        return value