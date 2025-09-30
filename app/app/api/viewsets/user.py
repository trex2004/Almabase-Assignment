from rest_framework.response import Response
from app.serializers import input, output
from app.models.user import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from django.utils import timezone


class CreateUser(APIView):
    permission_classes = (AllowAny,)
    input_serializer_class = input.CreateUserInputSerializer
    output_serializer_class = output.UserOutputSerializer

    def post(self, request, *args, **kwargs):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = User.objects.create(**input_serializer.validated_data)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            output_serializer = self.output_serializer_class(user)
            return Response(
                {
                    'user': output_serializer.data,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 
                status=status.HTTP_201_CREATED
            )
        

class LoginUser(APIView):
    permission_classes = (AllowAny,)
    input_serializer_class = input.LoginUserInputSerializer
    output_serializer_class = output.UserOutputSerializer

    def post(self, request, *args, **kwargs):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = User.objects.get(phone_number=input_serializer.validated_data['phone_number'])
            if not user.check_password(input_serializer.validated_data['password']):
                return Response(
                    {
                        'error': 'Invalid password.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            user.last_login = timezone.now()
            user.save()
            
            output_serializer = self.output_serializer_class(user)
            return Response(
                {
                    'user': output_serializer.data,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 
                status=status.HTTP_200_OK
            )