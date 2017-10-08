from django.views import generic

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon import tables

from billingdashboard.common import get_user_sub_plans, get_avbl_user_plans
from astutedashboard.common import get_plan

from billingdashboard.dashboards.project.available_plans \
    import tables as avbl_plan_tables
    
from billingdashboard.dashboards.project.available_plans \
    import forms as avbl_plan_forms
    
    
class IndexView(tables.DataTableView):
    table_class = avbl_plan_tables.AvailablePlansTable
    template_name = 'project/available_plans/index.html'
    page_title = _("Available Plans")

    def get_data(self):
                print 'Avbl'
                return get_avbl_user_plans(self.request, verbose=True)

class UserAvblPlanDetailsView(generic.TemplateView):
    template_name  = 'project/available_plans/plan.html'
    
    def get_context_data(self, **kwargs):
        context = super(UserAvblPlanDetailsView, self).get_context_data(**kwargs)
        print self.kwargs
        id = self.kwargs['id']
        context['plan_details'] = get_plan(id, verbose=True)
        return context
    
class PlanActivationByUserView(forms.ModalFormView):
    form_class = avbl_plan_forms.PlanActivationByUserForm
    template_name ='project/available_plans/modal_form.html'
    success_url = reverse_lazy("horizon:project:customer_available_plans:index")
    modal_id = "plan_activation_user_modal"
    modal_header =_("Activate Plan")
    submit_label = _("Activate")
    submit_url = "horizon:project:customer_available_plans:activate_user_plan"

    def get_initial(self):
        return get_plan(self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(PlanActivationByUserView, self).get_context_data(**kwargs)
        id = self.kwargs.get('id')
        context['submit_url'] = reverse(self.submit_url, args=[id])
        return context


