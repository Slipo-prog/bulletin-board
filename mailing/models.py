from django.db import models
from accounts.models import User


class Mailing(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    recipients = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.subject