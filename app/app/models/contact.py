from app.models import TimeStampModelMixin
from django.db import models
import uuid

class Contact(TimeStampModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='created_contacts', null=True)
    updated_by = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='updated_contacts', null=True)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        number = self.phone_number.strip().replace(" ", "")
        if not number.startswith("+"):
            number = "+91" + number 
        self.phone_number = number
        super().save(*args, **kwargs)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["phone_number", "created_by"],
                name="unique_phone_number_created_by",
            ),
        ]