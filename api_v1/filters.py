from django_filters import rest_framework as filters
from .models import Task
from .choices import TaskStatus
from django.contrib.auth.models import User


class TaskFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=TaskStatus)
    assigned_to = filters.ModelChoiceFilter(
        field_name='assigned_to',
        queryset=User.objects.all()
    )
    due_date_before = filters.DateFilter(
        field_name='due_date',
        lookup_expr='lte'
    )
    due_date_after = filters.DateFilter(
        field_name='due_date',
        lookup_expr='gte'
    )

    class Meta:
        model = Task
        fields = ['status', 'assigned_to']
