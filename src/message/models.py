from django.db import models
from django.contrib.auth import settings
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL

class Message(models.Model):
    user_from = models.ForeignKey(User,related_name='msg_from')
    user_to = models.ForeignKey(User,related_name='msg_to')
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'From: {self.user_from}\nTo: {self.user_to}\nPK: {self.pk}'

    def get_absolute_url(self):
        return reverse('message',kwargs={'username' : self.user_to})