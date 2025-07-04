from django.db import models
from django.contrib.auth.models import User
from . import choices


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=choices.TaskStatus.choices,
        default='TODO'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(
        User, related_name='tasks',
        on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        User,
        related_name='assigned_tasks',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title
