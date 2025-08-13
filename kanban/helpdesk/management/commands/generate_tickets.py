from django.core.management.base import BaseCommand
from helpdesk.models import Status, Engineer, Category, Priority, Ticket
import secrets


THINGS = ["Phone", "Firewall", "Email", "AI model", "Printer", "Laptop", "CRM app"]
PROBLEMS = [
    "has a virus",
    "has smoke coming out",
    "disk is nearly full",
    "needs a software update",
    "needs replacing",
    "got juice spilled on it",
    "is really slow"
]


class Command(BaseCommand):
    help = 'Generate tickets with randomized attributes'

    def handle(self, *args, **kwargs):
        statuses = Status.objects.all()
        categories = Category.objects.all()
        priorities = Priority.objects.all()

        for thing in THINGS:
            for problem in PROBLEMS:
                title = f"{thing} {problem}"

                # Randomly select status, category, and priority
                status = secrets.choice(statuses)
                category = secrets.choice(categories)
                priority = secrets.choice(priorities)

                # Create the ticket
                ticket = Ticket(
                    title=title,
                    status=status,
                    category=category,
                    priority=priority
                )
                ticket.save()

                engineers = list(Engineer.objects.all())  # Ensure the queryset is evaluated.
                # Assign engineer(s) to the ticket
                number_of_assignments = secrets.SystemRandom().choices([0, 1, 2, 3], [1, 5, 2, 1])[0]
                if number_of_assignments > 0:
                    for engineer in secrets.SystemRandom().sample(engineers, number_of_assignments):
                        ticket.assigned_to.add(engineer)
