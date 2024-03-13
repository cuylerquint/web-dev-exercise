import django_filters
from board.models import Ticket
from helpdesk.models import Category, Priority, Engineer


class TicketFilter(django_filters.FilterSet):

    class Meta:
        model = Ticket
        fields = []

    ticket_title = django_filters.CharFilter(
        field_name="title",
        label='Title',
        lookup_expr="icontains",
    )

    ticket_category = django_filters.ModelChoiceFilter(
        field_name="category__name",
        label='Category',
        queryset=Category.objects.all().distinct()
    )

    ticket_priority = django_filters.ModelChoiceFilter(
        field_name="priority__name",
        label='Priority',
        queryset=Priority.objects.all().distinct()
    )
    ticket_engineer = django_filters.ModelChoiceFilter(
        field_name="assigned_to__name",
        label='Engineer',
        queryset=Engineer.objects.all().distinct()
    )



