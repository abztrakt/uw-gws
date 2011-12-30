from django.shortcuts import render_to_response

# Import the models.py to grab the group model.
from uw_gws.models import UWGWSGroup 

# Utils.py contains the get request needed to process the information.
import utils

def view_group_info(request,group):
    '''
    Returns all of the HTML information associated with that group. 
    '''
    #result = UWGWSGroup.objects.get(name=group)
    args = {}
    return render_to_response('group.html',args)
