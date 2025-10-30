from rest_framework.response import Response
from app.models.user import User
from app.models.contact import Contact
from django.db.models import Q, Value
from app.serializers import output
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F
from django.db.models.functions import Greatest
from itertools import groupby
from rest_framework.pagination import LimitOffsetPagination


def get_query_type(query):
    query_type_map = {
        'phone_number': lambda q: q[0].isdigit(),
        'full_name': lambda q: not q[0].isdigit()
    }
    try:
        for query_type, condition in query_type_map.items():
            if condition(query):
                return query_type
    except Exception:
        return None



class SearchView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    output_serializer_class = output.SearchOutputSerializer

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response({"error": "Search query is required."}, status=400)

        results = []

        if query.isdigit():
            users = User.objects.filter(phone_number__icontains=query)
            contacts = Contact.objects.filter(phone_number__icontains=query)
            results = list(users) + list(contacts)

        else:
            user_qs = User.objects.annotate(
                sim_first=TrigramSimilarity("first_name", query),
                sim_last=TrigramSimilarity("last_name", query),
            ).annotate(
                similarity=Greatest(F("sim_first"), F("sim_last"))
            ).filter(similarity__gt=0.2)

            contact_qs = Contact.objects.annotate(
                sim_first=TrigramSimilarity("first_name", query),
                sim_last=TrigramSimilarity("last_name", query),
            ).annotate(
                similarity=Greatest(F("sim_first"), F("sim_last"))
            ).filter(similarity__gt=0.2)

            results = list(user_qs.order_by("-similarity")) + list(contact_qs.order_by("-similarity"))

        print("Total results before deduplication:", results)

        unique = {}
        for r in results:
            phone = getattr(r, "phone_number", None)
            if phone and phone not in unique:
                unique[phone] = r
        results = list(unique.values())

        paginator = LimitOffsetPagination()
        paginated = paginator.paginate_queryset(results, request)
        serializer = self.output_serializer_class(paginated, many=True)

        return Response({
            "count": len(results),
            "results": serializer.data,
        })
        

class SearchDetailsView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    output_user_serializer_class = output.SearchDetailsUserOutputSerializer
    output_contact_serializer_class = output.ContactOutputSerializer

    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        if user:
            is_contact_of_user = user.created_contacts.filter(created_by=request.user).exists()
            if is_contact_of_user:
                user.email = None
            output_serializer = self.output_user_serializer_class(user)
            return Response(output_serializer.data)

        contact = Contact.objects.filter(id=id).first()
        if contact:
            output_serializer = self.output_contact_serializer_class(contact)
            return Response(output_serializer.data)

        return Response({'error': 'Not found'}, status=404)