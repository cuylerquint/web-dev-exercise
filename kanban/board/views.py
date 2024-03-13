from django.views.generic import ListView
from board.models import Ticket, KanbanBoard
from django.views.generic import DetailView
from board.filters import TicketFilter


class DashboardView(ListView):
    model = KanbanBoard
    template_name = 'board/dashboard.html'


class BoardView(DetailView):
    model = KanbanBoard
    template_name = 'board/board.html'

    def get_object(self, queryset=None):
        return self.model.objects.filter(
            pk=self.kwargs.get('pk', None)
        ).prefetch_related(
            "column_set",
            "column_set__statuses",
            "column_set__statuses__ticket_set",
            "column_set__statuses__ticket_set__assigned_to",
            "column_set__statuses__ticket_set__category",
            "column_set__statuses__ticket_set__priority",
        ).first()

    def get_tickets_filter(self, board):
        return TicketFilter(
            self.request.GET,
            queryset=Ticket.objects.all()
        )

    def get_columns_context(self, board, filtered_tickets):
        columns = dict()
        for column in board.column_set.all():
            columns[column.id] = {
                "name": column.name,
                "tickets": filtered_tickets.filter(status__in=column.statuses.all()).order_by('-rank', 'id'),
                "statues": column.statuses.all(),
            }

        return columns

    def get_context_data(self, **kwargs):
        context_data = super(BoardView, self).get_context_data()
        board = self.get_object()
        # fetch all filtered tickets at once they select again for each column
        filtered_tickets = self.get_tickets_filter(board)
        context_data['columns'] = self.get_columns_context(board, filtered_tickets.qs)
        context_data['filter'] = filtered_tickets
        return context_data


class TicketView(DetailView):
    model = Ticket
    template_name = 'board/ticket.html'
