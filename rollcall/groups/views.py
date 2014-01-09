from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
)

from rollcall.groups.models import Group


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
        context['states'] = {
            'un': Group.objects.filter(state='un').count(),
            'kn': Group.objects.filter(state='kn').count(),
            'of': Group.objects.filter(state='of').count(),
            'f1': Group.objects.filter(state='f1').count(),
        }
        return context


class GroupStateListView(ListView):
    model = Group
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.filter(state=self.kwargs['state'])
