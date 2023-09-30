from rest_framework import serializers

from bot.models import Message


class MessageSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=255)
    message_text = serializers.CharField()


class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user', 'text', 'date_sent']
