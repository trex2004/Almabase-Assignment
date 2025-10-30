from rest_framework import serializers
from app.models.interaction import Interaction

class InteractionSerializer(serializers.ModelSerializer):
    initiator_name = serializers.CharField(source="initiator.first_name", read_only=True)
    receiver_name = serializers.CharField(source="receiver.first_name", read_only=True)

    class Meta:
        model = Interaction
        fields = [
            "id",
            "initiator",
            "receiver",
            "initiator_name",
            "receiver_name",
            "interaction_type",
            "timestamp",
            "metadata",
        ]
