from .commit import Commit, Snippet, Activity

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation


class Tracking(models.Model):
    user = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    commit = models.ForeignKey(Commit, related_name='comments', on_delete=models.CASCADE)
    snippet = models.ForeignKey(Snippet, related_name='comments', on_delete=models.CASCADE)
    code = models.CharField(max_length=1000)
    description = models.CharField(max_length=500)
    upvote = GenericRelation(Activity)
    resolved = models.OneToOneField(
        Commit, related_name='resolved', on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    latest_update = models.DateTimeField(auto_now_add=True)
