from django.db.models import TextChoices


class TaskStatus(TextChoices):
    TODO = 'TODO', 'A fazer'
    IN_PROGRESS = 'IN_PROGRESS', 'Em progresso'
    DONE = 'DONE', 'Concluído'
