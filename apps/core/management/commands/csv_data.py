import csv
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email

from apps.core.models import FoodPrice, GovernmentSubsidy, MonthlyPayment
from apps.kids.models import Child
from apps.users.models import Parent


class Command(BaseCommand):
    help = """Creates children instances from csv file containing:
    column1: child's full name,
    column2: mother's full name,
    column3: father's full name,
    column4: admission date in DD.MM.YYYY format,
    column5: parent's email (otionally),
    column6: login to parent's account,
    column7: password to parent's account
    """

    def add_arguments(self, parser):
        parser.add_argument("csv_file_name", type=str, help="Provide csv file name")

    def handle(self, *args, **kwargs):
        file_name = kwargs["csv_file_name"]
        base_food_price = FoodPrice.objects.filter(price=10).last()
        base_gov_subsidy = GovernmentSubsidy.objects.filter(amount=1500).last()
        base_monthly_payment = MonthlyPayment.objects.filter(price=2336).last()

        try:
            with open(file_name) as data:
                for row in csv.reader(data, delimiter=","):
                    name = row[0].split()
                    first_name = name[0]
                    last_name = name[1]
                    admission_date = datetime.strptime(row[3], "%d.%m.%Y").date()

                    email = row[4]
                    if email:
                        try:
                            validate_email(email)
                        except ValidationError:
                            email = None

                    username = row[5]
                    psw = row[6]

                    child = Child(
                        first_name=first_name,
                        last_name=last_name,
                        admission_date=admission_date,
                        food_price=base_food_price,
                        payment_month=base_monthly_payment,
                        local_subsidy=True,
                        gov_subsidy=base_gov_subsidy,
                    )

                    if len(username) > 2 and len(psw) > 5:
                        parent = Parent(username=username, email=email)
                        parent.set_password(psw)
                        parent.save()
                        child.parent = parent
                    child.save()

        except Exception as e:
            raise CommandError("Error:", e)
