from django.views.generic.edit import UpdateView
from django.urls import reverse
from helpdesk import models
from board.models import Column
import json


class TicketUpdateView(UpdateView):
    """
    This offers a very simple view to update the status and rank of a ticket.

    It can be viewed directly from a browser to get a simple editing form, but on success it
    redirects to a view that returns the HTML for that ticket on a Kanban board.

    It can also be used from an XMLHttpRequest request, in which case the client can follow
    the redirect to get updated HTML for the ticket and replace the old ticket HTML
    without refreshing the whole page.
    """
    model = models.Ticket
    fields = ['status', 'rank']

    def get_success_url(self):
        """
        Return the URL where the client can get updated ticket HTML.
        """
        return reverse('board:ticket', kwargs={'pk': self.object.id})

    def get_rank_update(self, updated_ticket_array):
        """
        Approach find this object id in updated ticket array

        - if first make 1000
        - if parent index null make -1
        - if parent index make one less than parent index
        """
        ticket_index = updated_ticket_array.index(str(self.object.id))

        if ticket_index == 0:
            return 1000

        parent_index = ticket_index - 1
        parent_ticket = self.model.objects.get(id=updated_ticket_array[parent_index])

        if parent_ticket.rank is None:
            return -1

        return parent_ticket.rank - 1

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = json.loads(request.POST.get('data'))
        # TODO update from status on frontend choice
        available_status = Column.objects.get(id=data['new_column']).statuses.all()
        self.object.status = available_status.first()
        self.object.rank = self.get_rank_update(data['ticket_array'])
        self.object.save(update_fields=["status", "rank"])
        return super().post(request, *args, **kwargs)

