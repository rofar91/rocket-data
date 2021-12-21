from rest_framework import serializers

from employees.models import Employee, SalaryHistory


class SalaryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryHistory
        fields = ['add_date', 'amount_of_payment']


class EmployeeSerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField()
    salary_history = SalaryHistorySerializer(many=True)

    class Meta:
        model = Employee
        fields = ['second_name', 'first_name', 'second_name', 'middle_name', 'position', 'employment_date', 'manager',
                  'hierarchy_level', 'salary', 'total_paid', 'salary_history']
