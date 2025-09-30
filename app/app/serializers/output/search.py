from rest_framework import serializers
from app.models.user import User
from app.models.contact import Contact
from app.models.scam import ScamRecord

class SearchOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    spammed_by_count = serializers.SerializerMethodField()
    phone_number = serializers.CharField()

    def get_name(self, obj):
        if isinstance(obj, User) or isinstance(obj, Contact):
            return obj.get_full_name()

    def get_is_registered(self, obj):
        return isinstance(obj, User)

    def get_spammed_by_count(self, obj):
        if isinstance(obj, User) or isinstance(obj, Contact):
            phone_number = obj.phone_number
        else:
            return 0
        
        return ScamRecord.objects.filter(phone_number=phone_number).count()
    

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
