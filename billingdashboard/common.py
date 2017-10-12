import requests as request
from openstack_dashboard.local.local_settings import \
        ASTUTE_BASE_URL

from astutedashboard.common import get_plan, get_plans, get_rab_rate
from openstack_dashboard.usage.quotas import get_tenant_quota_data, get_default_quota_data

def get_user_sub_plans(req, verbose=False):
    """Get all the plans subscribed by the user"""
	
    user_id = req.user.tenant_id
    response = request.get(ASTUTE_BASE_URL + 'plan/mapping/user?id=' + str(user_id))
    data = response.json()
		
    for item in data:
        	plan_id = item['plan_id']
	    	plan_details = get_plan(req, plan_id)
	    	plan_name = plan_details.get('name')
	    	service_name = plan_details.get('service_name')
                description = plan_details.get('description')
	    	item['name'] = plan_name
	        item['service_name'] = service_name
                item['description'] = description
    return data

def get_avbl_user_plans(req, verbose=False):
    """Get all the plans under the current billing type"""

    user_id = req.user.tenant_id
    plan_list = get_plans(req)
    #user_sub_plan_list = get_user_sub_plans(req)
    user_billing_details = get_user_billing_type(req)
        
    if user_billing_details:
        #Billing type code should already be present for a user
        billing_type_code = user_billing_details[0]['type_code']
        
        #Display only additional services for rab billing type
        if billing_type_code == 'rab':
            #print "Entering rab section"
            rab_billing_typeId = user_billing_details[0]['billing_type']
            data = filter(lambda x: (x['billing_type'] == None and x['service_name'] != 'SetupFee'), plan_list)
            
        if billing_type_code == 'payg':
            #print "Entering payg section"
            payg_billing_typeId = user_billing_details[0]['billing_type']
            data = filter(lambda x: ((x['billing_type'] == payg_billing_typeId or x['billing_type'] == None) and (x['service_name'] != 'SetupFee')), plan_list)
        
        for item in data:
            if billing_type_code == 'payg':
                item['billing_type']  = 'Usage Based Billing'
            elif billing_type_code =='rab':
                item['billing_type']  = 'Resource Allocation Based Billing'
            else:
                item['billing_type']  = 'NA'
    else:
        data = []
    """
    for item in data:
        billing_type_id = item['billing_type']
    """
    # filteredList = filter(lambda x: (x['billing_type'] == 1 and x['name'] not in keyVal2List), plan_list)
    return data
        
def get_user_invoices(req, verbose=True):
    """Get all the invoices correspodning to the user"""

    user_id = req.user.tenant_id
    response = request.get(ASTUTE_BASE_URL + 'invoice?user=' + str(user_id))
    data = response.json()

    #Rounding to 2 decimal points
    for item in data:
        item['total_amt']   = format(round(item['total_amt'], 2), '.2f')
        item['balance_amt'] = format(round(item['balance_amt'], 2), '.2f')
        item['amt_paid']    = format(round(item['amt_paid'], 2), '.2f')
    return data

def get_user_billing_type(req, verbose=False):
    """Get the billing type details corresponding to the user"""

    user_id = req.user.tenant_id
    response = request.get(ASTUTE_BASE_URL + 'billing/mapping/user?id=' + str(user_id))
    data = response.json()
    return data
       
def get_user_rab_details(req, verbose=False):
    """Get the rab details corresponding to the user"""

    user_id = req.user.tenant_id
    response = request.get(ASTUTE_BASE_URL + 'rabrate/mapping/user?id=' + str(user_id))
    data = response.json()

    for item in data:
		rab_resource_id = item['rab_resource_id']
		rab_resource_details = get_rab_rate(rab_resource_id)
		resource_name = rab_resource_details.get('name')
		resource_name = resource_name.replace("_"," ")
		resource_rate = rab_resource_details.get('rate')
		item['resource_name'] = resource_name
		item['resource_rate'] = resource_rate
    return data
