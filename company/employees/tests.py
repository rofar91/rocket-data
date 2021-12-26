from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from employees.models import Employee


class EmployeesEndpointsTests(APITestCase):
    fixtures = ['ranks.json', 'groups_permission.json', 'employees.json']

    def setUp(self):
        user_in_group_api_customers_and_is_staff = Employee.objects.get(id=1)
        self.token_user_is_staff = Token.objects.create(user=user_in_group_api_customers_and_is_staff).key

        user_in_group_api_customers = Employee.objects.get(id=2)
        self.token_user_in_group_api_customers = Token.objects.create(user=user_in_group_api_customers).key

        user_not_in_group_api_customers = Employee.objects.get(id=3)
        self.token_user_not_in_group_api_customers = Token.objects.create(user=user_not_in_group_api_customers).key

    def test_get_employees_for_user_in_group_api_customers_and_is_staff(self):
        """
        Тестируем получение информации о сотрудниках
        пользователем который имеет статус персонала и состоит в группе 'api_customers'
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user_is_staff}')
        r = self.client.get('/api/employees/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get('count'), 5)  # получил информацию о всех 5 сотрудниках

    def test_get_employees_for_user_in_group_api_customers(self):
        """
        Тестируем получение информации о сотрудниках
        пользователем который состоит в группе 'api_customers', но не имеет статуса персонала
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user_in_group_api_customers}')
        r = self.client.get('/api/employees/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        expected_result = {
            'count': 1, 'next': None, 'previous': None,
            'results':
                [
                    {
                        'last_name': 'Лашкевич', 'first_name': 'Сергей', 'middle_name': '', 'position': 'руководитель',
                        'employment_date': '2021-12-22', 'manager': 'Абрамович Дмитрий Иванович - генеральный директор',
                        'hierarchy_level': 1, 'salary': '50000.00', 'total_paid': None, 'salary_history': [],
                    }
                ]
        }
        self.assertEqual(r.json().get('count'), 1)  # получил информацию только о себе
        self.assertEqual(r.json(), expected_result)

    def test_get_employees_for_user_not_in_group_api_customers(self):
        """
        Тестируем получение информации о сотрудниках
        пользователем который не имеет на это прав (не состоит в группе 'api_customers')
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_user_not_in_group_api_customers}')
        r = self.client.get('/api/employees/')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(r.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})
