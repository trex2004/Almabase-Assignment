from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from app.models.interaction import Interaction
from app.serializers.output.interaction import InteractionSerializer
from app.models.user import User
from rest_framework.pagination import LimitOffsetPagination
from django.utils.dateparse import parse_datetime

class CreateInteractionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        initiator = request.user
        receiver_id = request.data.get("receiver_id")
        interaction_type = request.data.get("interaction_type")
        metadata = request.data.get("metadata", {})

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=404)

        interaction = Interaction.objects.create(
            initiator=initiator,
            receiver=receiver,
            interaction_type=interaction_type,
            metadata=metadata,
        )
        return Response({"id": interaction.id, "status": "created"})


class RecentInteractionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        interaction_type = request.query_params.get("type")

        qs = Interaction.objects.filter(initiator_id=user_id) | Interaction.objects.filter(receiver_id=user_id)
        if interaction_type:
            qs = qs.filter(interaction_type=interaction_type)
        qs = qs.order_by("-timestamp")

        paginator = LimitOffsetPagination()
        paginated_qs = paginator.paginate_queryset(qs, request)

        serializer = InteractionSerializer(paginated_qs, many=True)
        
        count = qs.count()

        return Response({
            'count': count,
            'results': serializer.data
        })

class TopContactsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        limit = int(request.query_params.get("limit", 5)) 
        qs = (
            Interaction.objects.filter(initiator_id=user_id)
            .values("receiver__id", "receiver__first_name", "receiver__phone_number")
            .annotate(interaction_count=Count("id"))
            .order_by("-interaction_count")[:limit]
        )
        return Response(qs)


class SpamReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get("start")
        end_date = request.query_params.get("end")

        qs = Interaction.objects.filter(interaction_type=Interaction.SPAM_REPORT)

        # filter by date range if provided
        if start_date:
            qs = qs.filter(timestamp__gte=parse_datetime(start_date))
        if end_date:
            qs = qs.filter(timestamp__lte=parse_datetime(end_date))

        qs = (
            qs.values("receiver__phone_number")
            .annotate(report_count=Count("id"))
            .order_by("-report_count")
        )
        return Response(qs)
