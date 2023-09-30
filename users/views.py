from rest_framework import status
from rest_framework.decorators import api_view
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomAuthTokenSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            bot_link = f"https://t.me/factory_baglan_bot"
            return Response(
                {"message": "Успешная регистрация. Подпишитесь на нашего бота по ссылке:", "bot_link": bot_link},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'login': user.login,
            'name': user.name
        })
