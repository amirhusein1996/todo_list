from django.db import models
from django.conf import settings

class ContactUsMessage (models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL , on_delete=models.PROTECT, blank=True ,null=True)
    email = models.EmailField(blank=True , null=True) # if user is not logged in, must enter email
    subject = models.CharField(max_length=200)
    message = models.TextField()
    response = models.TextField(blank=True , null=True)
    is_read_by_admin = models.BooleanField(blank=True , null=True)
    has_responded = models.BooleanField(blank=True , null=True , editable=False)

    def save(self, *args , **kwargs):
        if self.response:
            self.has_responded = True

        super().save(*args , **kwargs)

    def __str__(self):
        return self.subject