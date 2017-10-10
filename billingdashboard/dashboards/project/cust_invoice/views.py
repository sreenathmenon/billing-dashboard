from django.views import generic

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon import tables

from billingdashboard.common import get_user_invoices

from billingdashboard.dashboards.project.cust_invoice \
    import tables as invoice_table
from astutedashboard.common import get_invoices, get_invoice
    
    
class IndexView(tables.DataTableView):
    table_class = invoice_table.UserInvoiceListingTable
    template_name = 'project/cust_invoice/index.html'
    page_title = _("Invoices")

    def get_data(self):
        return get_user_invoices(self.request, verbose=True)

class UserInvoiceDetailsView(generic.TemplateView):
    template_name = 'project/cust_invoice/invoice.html'
    
    def get_context_data(self, **kwargs):
        context = super(UserInvoiceDetailsView, self).get_context_data(**kwargs)
        id = self.kwargs['invoice_id']
        context['invoice'] = get_invoice(id, verbose=True)
        return context
