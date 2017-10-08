import requests as request
from openstack_dashboard.local.local_settings import \
        ASTUTE_BASE_URL

from astutedashboard.common import get_plan, get_plans

def get_user_sub_plans(req, verbose=False):
        user_id = req.user.id
        user_id = 'dgdfgdfg234ad'
        response = request.get(ASTUTE_BASE_URL + 'plan/mapping/user?id=' + str(user_id))
        data = response.json()
        print data
        for item in data:
            plan_id = item['plan_id']
            plan_details = get_plan(plan_id)
            plan_name = plan_details.get('name')
            item['name'] = plan_name
        return data

def get_avbl_user_plans(req, verbose=False):
        user_id = req.user.id
        user_id = 'dgdfgdfg234ad'
        user_billing_details = get_user_billing_type(req, verbose=False)
        billing_type_id = user_billing_details[0]['billing_type']
        """
        for item in data:
            billing_type_id = item['billing_type']
        """
        plan_list = get_plans()
        user_sub_plan_list = get_user_sub_plans(req)
        print '%%%%%%%%%%%%%%%%'
        print user_sub_plan_list
        """        
        results = []
        for item in user_sub_plan_list:
            results.append(item['name'])
    
        print '%%%%%%%%%%%%%%%%%%%%%%%%'
        print results
        """
        user_sub_list = [ item['name'] for item in  user_sub_plan_list ]
        
        print '#############################'
        print user_sub_list
        #filteredList = filter(lambda x: (x['billing_type'] == 1 and x['name'] not in keyVal2List), plan_list)
        filteredList  = filter(lambda x: (x['billing_type'] == billing_type_id), plan_list)
        print '@@@@@@@@@@@@@@@@@@@@@2'
        data = filteredList
        return data
        
        
def get_user_invoices(req, verbose=True):
        user_id = req.user.id
        user_id = 'df93528ba1014db6863ea47724990575'
        response = request.get(ASTUTE_BASE_URL + 'invoice?user=' + str(user_id))
        data = response.json()
        return data

def get_user_billing_type(req, verbose=False):
        user_id = req.user.id
        user_id = 'e4c3c7214087459dbda4122307d88075'
        response = request.get(ASTUTE_BASE_URL + 'billing/mapping/user?id=' + str(user_id))
        data = response.json()
        return data
    
        # for item in data:
        # print item
        # print item['billing_type']



 
