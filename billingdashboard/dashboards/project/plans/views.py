from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'project/plans/index.html'


