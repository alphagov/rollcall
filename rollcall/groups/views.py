from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
)
from django.views.generic.edit import UpdateView

from rollcall.groups.models import Group, GroupState


class GroupDetailView(DetailView):
    model = Group
    context_object_name = 'group'


class GroupListView(ListView):
    model = Group
    context_object_name = 'groups'


class GroupStatesView(TemplateView):
    template_name = 'states.html'

    def get_context_data(self):
        context = super(GroupStatesView, self).get_context_data()
        context['states'] = GroupState(
            item=lambda c: {
                'id': c.id,
                'name': c.name,
                'desc': c.desc,
                'count': Group.objects.filter(state=c).count(),
            }
        )
        return context


class GroupStateListView(ListView):
    model = Group
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.filter(state=self.kwargs['state'])


class GroupUpdate(UpdateView):
    model = Group
    fields = [ 'state' ]
