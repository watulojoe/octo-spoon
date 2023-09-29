from django.db import models

# Create your models here.
class ContactInfo(models.Model):
    facility_id = models.CharField(max_length=100)
    facility_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    partner_name = models.CharField(max_length=100)

    def __str__(self):
        return self.facility_name