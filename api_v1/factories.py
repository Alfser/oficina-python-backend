from datetime import date, timedelta
import random
import factory
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Task
from . import choices


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Sequence(lambda n: f'Task {n}')
    description = factory.Faker('paragraph', nb_sentences=3)
    status = factory.Iterator(
        [status[0] for status in choices.TaskStatus.choices]
    )
    due_date = factory.LazyFunction(
        lambda: date.today() + timedelta(days=random.randint(1, 30))
    )
    owner = factory.SubFactory(UserFactory)
    assigned_to = factory.SubFactory(UserFactory)
