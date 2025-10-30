from rest_framework import serializers
from app.models.user import User
from app.models.contact import Contact
from app.models.scam import ScamRecord

class SearchOutputSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    spammed_by_count = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(getattr(obj, "id", None))

    def get_name(self, obj):
        if isinstance(obj, (User, Contact)):
            full_name = getattr(obj, "get_full_name", lambda: None)()
            if full_name:
                return full_name
            return f"{getattr(obj, 'first_name', '')} {getattr(obj, 'last_name', '')}".strip()
        return None

    def get_is_registered(self, obj):
        return isinstance(obj, User)

    def get_spammed_by_count(self, obj):
        phone = getattr(obj, "phone_number", None)
        if not phone:
            return 0
        return ScamRecord.objects.filter(phone_number=phone).count()

    def get_phone_number(self, obj):
        return getattr(obj, "phone_number", None)    

class SearchDetailsUserOutputSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    spammed_by_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'full_name', 
            'spammed_by_count',
            'email', 
            'phone_number', 
        )

    def get_spammed_by_count(self, obj: User):
        return ScamRecord.objects.filter(phone_number=obj.phone_number).count()

    def get_full_name(self, obj: User):
        return obj.get_full_name()
