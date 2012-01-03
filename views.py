from django.shortcuts import render_to_response
from django.template import RequestContext

# Import the models.py to grab the group model.
from uw_gws.models import UWGWSGroup 

# Utils.py contains the get request needed to process the information.
import utils

def view_group_info(request,group):
    '''
    Returns all of the HTML information associated with that group. 
    '''
    result = utils.get_group_info(group)
    
    args = {
        'title': 'Group: %s' % group, 
        'result': result,
    }
    return render_to_response('group.html',args,context_instance=RequestContext(request))

def view_group_list(request):
    '''
    Returns a list of all the groups registered in the django database.
    '''
    object_list = UWGWSGroup.objects.all()

    args = {
        'title': 'Groups',
        'object_list': object_list,   
    }

    return render_to_response('list.html',args,context_instance=RequestContext(request))

def view_group_members(request,group):
    '''
    Returns a list of all of the members of the group using the Groups Web Service.
    '''

    result = utils.get_group_members(group)
    
    args = {
        'title': 'Group: %s - Members' % group, 
        'result': result,
    }
    
    return render_to_response('members.html',args,context_instance=RequestContext(request))
