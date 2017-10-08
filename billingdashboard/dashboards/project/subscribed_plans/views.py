from django.views import generic

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon import tables

from billingdashboard.common import get_user_sub_plans
from astutedashboard.common import get_plan

from billingdashboard.dashboards.project.subscribed_plans \
    import tables as sub_plan_tables
    
    
class IndexView(tables.DataTableView):
    table_class = sub_plan_tables.SubscribedPlansTable
    template_name = 'project/subscribed_plans/index.html'
    page_title = _("Subscribed Plans")

    def get_data(self):
                return get_user_sub_plans(self.request, verbose=True)

class UserSubPlanDetailsView(generic.TemplateView):
    template_name  = 'project/subscribed_plans/plan.html'
    
    def get_context_data(self, **kwargs):
        context = super(UserSubPlanDetailsView, self).get_context_data(**kwargs)
        print self.kwargs
        id = self.kwargs['id']
        context['plan_details'] = get_plan(id, verbose=True)
        return context

