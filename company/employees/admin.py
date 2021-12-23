from django.contrib import admin
from django.contrib.admin import register
from django.urls import reverse
from django.utils.html import format_html

from .models import Employee, SalaryHistory, Rank


@register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'last_name', 'first_name', 'middle_name', 'position', 'employment_date', 'manager', 'salary',
        )}),
        ('Permissions', {'fields': ('username', 'is_staff', 'is_active', 'groups')}),
    )
    list_display = ('get_fio', 'position', 'get_manager_link', 'salary', 'total_paid')
    list_filter = ('position__title', 'hierarchy_level')
    search_fields = ('last_name',)
    search_help_text = 'Поиск по фамилии'
    actions = ['delete_salary_history']

    def delete_salary_history(self, request, queryset):
        salary = SalaryHistory.objects.filter(employee__in=queryset)
        salary_count = salary.count()
        salary.delete()
        self.message_user(request, f'Успешно удалены истории выплат заработной платы {salary_count}')
    delete_salary_history.short_description = 'Удалить всю информацию о выплаченной заработной плате ' \
                                              'у выбранных сотрудников'

    def get_fio(self, obj):
        fio = obj.display_name
        return fio if fio.strip() else ' - '
    get_fio.short_description = 'ФИО'

    def get_manager_link(self, obj):
        if obj.manager:
            manager_id = obj.manager.id
            url = reverse('admin:employees_employee_change', args=(manager_id,))
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.manager)
    get_manager_link.short_description = 'Ссылка на начальника'


@register(SalaryHistory)
class SalaryHistoryAdmin(admin.ModelAdmin):
    list_filter = ('add_date',)


admin.site.register(Rank)
admin.site.site_header = 'RocketData'
