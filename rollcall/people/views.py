from django.views.generic import DetailView, ListView

from rollcall.people.models import Person


class PersonDetailView(DetailView):
    model = Person
    context_object_name = 'person'

class PersonListView(ListView):
    model = Person
    context_object_name = 'people'
