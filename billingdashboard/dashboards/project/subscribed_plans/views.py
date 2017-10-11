from django.views import generic

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon import tables

from billingdashboard.common import get_user_sub_plans, get_user_billing_type, get_user_rab_details
from astutedashboard.common import get_plan

from billingdashboard.dashboards.project.subscribed_plans \
    import tables as sub_plan_tables
    
class IndexView(generic.TemplateView):
    #table_class = sub_plan_tables.SubscribedPlansTable
    template_name = 'project/subscribed_plans/index.html'
    page_title = _("Subscribed Plans")

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        billing_details = get_user_billing_type(self.request)
        
        #At-least all users must be having payg plan by default
        #Also a user will be having only 1 active billing plan at a time

        if not billing_details:
        	billing_code = 'NA'
        else:
            billing_code = billing_details[0]['type_code']

        context['user_billing_code'] = billing_code
        
        if billing_code =='rab':
        	rab_details = get_user_rab_details(self.request)
        	context['rab_details'] = get_user_rab_details(self.request)
        
        context['plans'] = get_user_sub_plans(self.request)
        return context

class UserSubPlanDetailsView(generic.TemplateView):
    template_name = 'project/subscribed_plans/plan.html'
    
    def get_context_data(self, **kwargs):
        context = super(UserSubPlanDetailsView, self).get_context_data(**kwargs)
        id = self.kwargs['id']
        context['plan_details'] = get_plan(self.request, id)
        return context

