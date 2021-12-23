from company.celery import app
from employees.models import Employee, SalaryHistory


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls pay_salary() every 2 hours.
    sender.add_periodic_task(60*60*2, pay_salary.s(), name='add payment every 2 hours')


@app.task
def pay_salary():
    for employee in Employee.objects.all():
        if employee.salary:
            SalaryHistory.objects.create(employee=employee, amount_of_payment=employee.salary)
