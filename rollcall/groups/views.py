from django.views.generic import DetailView, ListView

from rollcall.groups.models import Group


class GroupDetailView(DetailView):
    model = Group
    context_object_name = 'group'

class GroupListView(ListView):
    model = Group
    context_object_name = 'groups'
