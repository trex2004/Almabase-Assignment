from django.db import models
from django.utils import timezone
from app.models.user import User
import uuid

class Interaction(models.Model):
    CALL = "call"
    MESSAGE = "message"
    SPAM_REPORT = "spam_report"

    INTERACTION_TYPES = [
        (CALL, "Call"),
        (MESSAGE, "Message"),
        (SPAM_REPORT, "Spam Report"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    initiator = models.ForeignKey(User, related_name="initiated_interactions", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_interactions", on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["initiator", "timestamp"]),
            models.Index(fields=["receiver", "timestamp"]),
            models.Index(fields=["interaction_type"]),
        ]
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.initiator} -> {self.receiver} ({self.interaction_type})"
