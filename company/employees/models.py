from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum


class Employee(AbstractUser):
    EMPLOYEE_TYPES = (
        ('Генеральный директор', 'Генеральный директор'),
        ('Руководитель', 'Руководитель'),
        ('Менеджер среднего звена', 'Менеджер среднего звена'),
        ('Менеджер', 'Менеджер'),
        ('Работник', 'Работник'),
    )
    first_name = models.CharField(verbose_name='Имя', max_length=150, blank=True)
    second_name = models.CharField(verbose_name='Фамилия', max_length=150, blank=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=150, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=25, choices=EMPLOYEE_TYPES)
    employment_date = models.DateField(verbose_name='Дата приёма на работу', null=True, blank=True)
    manager = models.ForeignKey(
        'self', verbose_name='Руководитель', blank=True, null=True, related_name='employee', on_delete=models.SET_NULL,
    )
    hierarchy_level = models.SmallIntegerField(verbose_name='Уровень', default=0)
    salary = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.second_name} {self.first_name} {self.middle_name} - {self.position}'

    def save(self, *args, **kwargs):
        if self.manager:
            self.hierarchy_level = self.manager.hierarchy_level + 1

        # do not create more than one employee with level = 0
        if self.hierarchy_level == 0:
            try:
                top_employee = Employee.objects.get(hierarchy_level=0)
            except Employee.DoesNotExist:
                super().save(*args, **kwargs)
                return
            if top_employee.id != self.id:
                return

        # do not create more than 4 levels hierarchy
        if self.hierarchy_level > 4:
            return

        super().save(*args, **kwargs)

    @property
    def total_paid(self):
        result = self.salary_history.aggregate(total=Sum('amount_of_payment'))
        return result.get('total')
    total_paid.fget.short_description = "Всего выплачено"


class SalaryHistory(models.Model):
    employee = models.ForeignKey(
        Employee, verbose_name='Работник', related_name='salary_history', on_delete=models.CASCADE,
    )
    add_date = models.DateField(verbose_name='Дата выплаты', auto_now=True)
    amount_of_payment = models.FloatField(verbose_name='Размер выплаты')

    class Meta:
        verbose_name = 'информация о выплаченной зарплате'
        verbose_name_plural = 'Информация о выплаченной зарплате'

    def __str__(self):
        return f'{self.employee} {self.amount_of_payment}'
