from rest_framework.serializers import ModelSerializer
from .models import News, NewsTopic
from rest_framework import serializers


class NewsSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = News
        # fields = '__all__'
        
        fields = [
            'pk',
            'title',
            'slug',
            'description',
            'image',
            'publication_date',
            'updated_date',
            'newstopic',
            'user',
        ]
        extra_kwargs = {
            'slug': {'read_only': True},
            'publication_date': {'read_only': True},
            'updated_date': {'read_only': True},
        }

    def create(self, validated_data):
      validated_data['user'] = self.context['request'].user
      return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('user', None)
        return super().update(instance, validated_data)


class NewsTopicSerializer(ModelSerializer):
    class Meta:
        model = NewsTopic
        
        fields = [
            'pk',
            'name',
            'slug',
        ]