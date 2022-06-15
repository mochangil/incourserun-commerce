from rest_framework import serializers

from app.example.models import Example


class ExampleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        Example.objects.create(**validated_data)
        return validated_data
