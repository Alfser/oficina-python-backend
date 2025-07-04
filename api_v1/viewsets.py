from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .permissions import IsOwnerOrReadOnly
from .serializers import TaskSerializer
from .filters import TaskFilter
from django.contrib.auth.models import User


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filterset_class = TaskFilter

    def get_queryset(self):
        """
        Filtra as tarefas para mostrar apenas as do usuário logado
        ou as que foram atribuídas a ele.
        """
        user = self.request.user
        return Task.objects.filter(
            Q(owner=user) | Q(assigned_to=user)
        ).distinct()

    def perform_create(self, serializer):
        """Define automaticamente o dono da tarefa como o usuário logado."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Ação customizada para atribuir uma tarefa a outro usuário."""
        task = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {'error': 'user_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuário não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        task.assigned_to = user
        task.save()

        return Response(
            {'status': 'tarefa atribuída'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Ação customizada para alterar o status de uma tarefa."""
        task = self.get_object()
        new_status = request.data.get('status')

        if not new_status:
            return Response(
                {'error': 'status é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in dict(Task.STATUS_CHOICES):
            return Response(
                {'error': 'status inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        task.status = new_status
        task.save()

        return Response(
            {'status': 'status alterado'},
            status=status.HTTP_200_OK
        )
