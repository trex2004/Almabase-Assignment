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
            user = User.objects.create_user(
                phone_number=input_serializer.validated_data['phone_number'],
                password=input_serializer.validated_data['password'],
                first_name=input_serializer.validated_data.get('first_name', ''),
                last_name=input_serializer.validated_data.get('last_name', ''),
                email=input_serializer.validated_data.get('email', None),
            )
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
            phone = input_serializer.validated_data['phone_number']
            password = input_serializer.validated_data['password']

            user, created = User.objects.get_or_create(
                phone_number=phone,
                defaults={'first_name': '', 'password': password}
            )
            if not created and not user.check_password(password):
                return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)

            if created:
                user.set_password(password)
                user.save()

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