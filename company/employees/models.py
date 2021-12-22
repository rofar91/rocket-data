from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum

MAX_HIERARCHY_LEVEL = 4


class Rank(models.Model):
    title = models.CharField(verbose_name='Должность', max_length=25, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.title


class Employee(AbstractUser):
    first_name = models.CharField(verbose_name='Имя', max_length=150, blank=True)
    second_name = models.CharField(verbose_name='Фамилия', max_length=150, blank=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=150, blank=True)
    position = models.ForeignKey(Rank, verbose_name='Должность', null=True, on_delete=models.SET_NULL)
    employment_date = models.DateField(verbose_name='Дата приёма на работу', null=True, blank=True)
    manager = models.ForeignKey(
        'self', verbose_name='Руководитель', blank=True, null=True, related_name='employee', on_delete=models.SET_NULL,
    )
    hierarchy_level = models.SmallIntegerField(verbose_name='Уровень', default=0)
    salary = models.DecimalField(
        verbose_name='Заработная плата', decimal_places=2, max_digits=10, blank=True, null=True,
    )

    class Meta:
        ordering = ['second_name']
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        position_title = f' - {self.position.title}' if self.position else ''
        return self.display_name + position_title

    def save(self, *args, **kwargs):
        if self.manager:
            if self.manager.hierarchy_level == MAX_HIERARCHY_LEVEL:
                self.hierarchy_level = self.manager.hierarchy_level  # Don't create hierarchy level more than max
            else:
                self.hierarchy_level = self.manager.hierarchy_level + 1

        else:  # Don't create more than one employee with level = 0
            try:
                top_employee = Employee.objects.get(hierarchy_level=0)
            except Employee.DoesNotExist:
                super().save(*args, **kwargs)
                return
            if top_employee.id != self.id:
                return

        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return f'{self.second_name} {self.first_name} {self.middle_name}'

    @property
    def total_paid(self):
        result = self.salary_history.aggregate(total=Sum('amount_of_payment'))
        return result.get('total')
    total_paid.fget.short_description = 'Всего выплачено'


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
