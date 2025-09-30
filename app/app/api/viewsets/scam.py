from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.serializers import input, output
from app.models.scam import ScamRecord
from django.db import transaction

class CreateScamRecord(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    input_serializer_class = input.CreateScamRecordInputSerializer
    output_serializer_class = output.ScamRecordOutputSerializer

    def post(self, request):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        with transaction.atomic():
            try:
                scam = ScamRecord.objects.create(
                    reported_by=user,
                    created_by=user,
                    updated_by=user,
                    **input_serializer.validated_data
                )
                output_serializer = self.output_serializer_class(scam)
            except Exception as e:
                return Response({'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)