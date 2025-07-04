from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .factories import TaskFactory, UserFactory
from .choices import TaskStatus


class TaskAPITestCase(APITestCase):
    def setUp(self):
        # users
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        
        # tasks
        self.task1 = TaskFactory(
            status=TaskStatus.TODO,
            owner=self.user1,
        )
        
        self.task2 = TaskFactory(
            status=TaskStatus.IN_PROGRESS,
            owner=self.user1,
            assigned_to=self.user2,
        )
        
        self.task3 = TaskFactory(
            status=TaskStatus.DONE,
            owner=self.user2,
        )
        
        self.client.force_authenticate(user=self.user1)

    def test_deveria_listar_todas_tasks_cadastradas_quando_consultado_via_get(self):
        url = reverse('tasks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User1 should see their own tasks and tasks assigned to them
        self.assertEqual(len(response.data), 2)

    def test_deveria_filtrar_tasks_quando_usado_filtro_por_status(self):
        url = reverse('tasks-list')
        
        response = self.client.get(url, {'status': 'TODO'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'TODO')
        
        response = self.client.get(url, {'status': 'IN_PROGRESS'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'IN_PROGRESS')
        
        response = self.client.get(url, {'status': 'DONE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_deveria_listare_tasks_do_usuario_atribuido_quando_consultar_endpoint_listagem_via_filtro(self):
        url = reverse('tasks-list')
        
        response = self.client.get(url, {'assigned_to': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['assigned_to']['id'], self.user2.id)
        self.assertEqual(response.data[0]['id'], self.task2.id)

    def test_deveria_permitir_listar_tasks_do_dono_quando_consultado_suas_tasks(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('tasks-list')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        response = self.client.get(url, {'status': 'DONE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.task3.id)

    def test_usuario_pode_modificar_task_quando_eh_dono(self):
        detail_url = reverse('tasks-detail', kwargs={'pk': self.task1.pk})
        update_data = {'title': 'Updated Title 1'}
        
        response = self.client.put(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.patch(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
