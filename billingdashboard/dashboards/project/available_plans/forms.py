#
# Copyright 2017 NephoScale
#

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from astutedashboard.common import create_billing_plan_mapping

contract_choices = (('3', '3'),('6','6'),('12', '12'), ('18','18'), ('24', '24'), ('30', '30'), ('36', '36'))

class PlanActivationByUserForm(forms.SelfHandlingForm):

        id               = forms.CharField(label=_("ID"), widget=forms.HiddenInput())
        quantity         = forms.IntegerField(label=_("Quantity"), min_value = 1 ,required = True, widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+', 'title':'Enter numbers Only '}))
        contract_period  = forms.ChoiceField(label=_('Contract Period (in months)'), required = True, choices=contract_choices)

        def handle(self, request, data):
                try:
                    print "try section"
                    print data
                    print "%%%%%%%%%%%%%%%%%%"
                    #plans = {}
                    print type(data)
                    plan_id =  data.get("id", "")
                    quantity = data.get("quantity", "")
                    plans = {plan_id: quantity}
                    print plans
                    print 'plaaans'
                    user_id = self.request.user.id
                    user_id = 'dgdfgdfg234ad'
                    print user_id
                    print 'ussser'
                    data['plans']  = plans
                    data['user'] = user_id
 
                    create_billing_plan_mapping(data)
                    return True

                except ValidationError:
                        raise

                except Exception:
                        exceptions.handle(request, _('Unable to activate the selected Plan.'))

