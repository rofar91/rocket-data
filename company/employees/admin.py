from django.contrib import admin
from django.contrib.admin import register

from .models import Employee, SalaryHistory


@register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ('second_name', 'first_name', 'middle_name', 'position', 'employment_date', 'manager', 'salary')
    list_filter = ('position', 'hierarchy_level', )
    actions = ['delete_salary_history']

    def delete_salary_history(self, request, queryset):
        salary = SalaryHistory.objects.filter(employee__in=queryset)
        salary_count = salary.count()
        salary.delete()
        self.message_user(request, f"Успешно удалены истории выплат заработной платы {salary_count}")
    delete_salary_history.short_description = "Удалить всю информацию о выплаченной заработной плате " \
                                              "у выбранных сотрудников"


@register(SalaryHistory)
class SalaryHistoryAdmin(admin.ModelAdmin):
    list_filter = ('add_date', )


admin.site.site_header = 'RocketData'
