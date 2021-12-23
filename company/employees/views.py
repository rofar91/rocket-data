from rest_framework import generics

from employees.models import Employee
from employees.serializers import EmployeeSerializer


class Employees(generics.ListAPIView):
    """
    API endpoint that users can viewed information about himself.
    """
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        user = self.request.user

        # get all employees for staff users
        if user.is_staff:
            return Employee.objects.all()

        # or get information about himself
        return Employee.objects.filter(id=user.id)


class Hierarchy(generics.ListAPIView):
    """
    API endpoint that users can viewed employees by hierarchy level.
    """
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        level = self.kwargs['level']
        user = self.request.user

        # get all employees for staff users
        if user.is_staff:
            return Employee.objects.filter(hierarchy_level=level)

        # or get information about himself
        return Employee.objects.filter(hierarchy_level=level, id=user.id)
