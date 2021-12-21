from rest_framework import generics, permissions

from employees.models import Employee
from employees.serializers import EmployeeSerializer


class Employees(generics.ListAPIView):
    """
    API endpoint that allows staff users viewed employees.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class Hierarchy(generics.ListAPIView):
    """
    API endpoint that allows staff users viewed employees by hierarchy level.
    """
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        level = self.kwargs['level']
        return Employee.objects.filter(hierarchy_level=level)
