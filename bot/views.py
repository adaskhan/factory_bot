import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from telegram import Bot

from bot.models import Message
from bot.serializers import MessageSerializer, MessageDetailSerializer
from users.models import CustomUser

TELEGRAM_TOKEN = '6299555354:AAFpmXhuEqFcSVaOAkfutakIz0S72ZZu6sU'
TELEGRAM_CHAT_ID = '@factory_baglan_bot'


def send_telegram_message(chat_id, message_text):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=chat_id, text=message_text)


def generate_token():
    return str(uuid.uuid4())


@api_view(['POST'])
def telegram_webhook(request):
    data = request.data
    chat_id = data['message']['chat']['id']
    user_message = data['message']['text']

    user = None
    try:
        user = CustomUser.objects.get(login=user_message)  # предполагаем, что пользователь отправил свой логин
        user.chat_id = chat_id
        user.token = generate_token()
        user.save()

        token_message = f"Ваш уникальный токен: {user.token}"
        send_telegram_message(chat_id, token_message)
    except CustomUser.DoesNotExist:
        error_message = "Извините, мы не смогли найти ваш логин в нашей системе. Пожалуйста, убедитесь, что вы отправили правильный логин и попробуйте снова."
        send_telegram_message(chat_id, error_message)

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def send_message(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        login = serializer.validated_data["login"]
        message_text = serializer.validated_data["message_text"]

        try:
            user = CustomUser.objects.get(login=login)
            if user.chat_id:
                send_telegram_message(user.chat_id, message_text)
                Message.objects.create(user=user, text=message_text)
                return Response({"message": "Сообщение успешно отправлено!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Пользователь не связан с Telegram."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_messages(request):
    messages = Message.objects.all().order_by('-date_sent')
    serializer = MessageDetailSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
