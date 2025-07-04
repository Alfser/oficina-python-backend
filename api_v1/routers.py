from rest_framework.routers import DefaultRouter
from .viewsets import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
