from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User,Group

# Utils.py contains the get request needed to process the information.
import utils

def home_page(request):

    args = {
        'title': 'Home',
    }
    return render_to_response('home.html',args,context_instance=RequestContext(request))

@login_required(login_url='/admin/')
def view_group_info(request,group):
    '''
    Returns all of the HTML information associated with that group. 
    '''
    result, group_exists = utils.get_group_info(group)
    args = {
        'title': 'Group: %s' % group, 
        'group': group,
    }

    if not group_exists:
        args['error'] = result['error']+ " No group info can be provided." 
    else:
        args['result'] = result['group_info']

    return render_to_response('group.html',args,context_instance=RequestContext(request))

def view_group_list(request):
    '''
    Returns a list of all the groups registered in the django database.
    '''
    object_list = Group.objects.all()

    args = {
        'title': 'Groups',
        'object_list': object_list,   
    }

    return render_to_response('list.html',args,context_instance=RequestContext(request))

@login_required(login_url='/admin/')
def view_group_members(request,group):
    '''
    Returns a list of all of the members of the group using the Groups Web Service.
    '''

    result,group_exists = utils.get_group_members(group)
    
    args = {
        'title': 'Group: %s - Members' % group, 
        'group': group,
    }

    if not group_exists:
        args['error'] = result['error'] + " No members to list." 
    else:
        args['result'] = result['group_members']

    return render_to_response('members.html',args,context_instance=RequestContext(request))


@permission_required('auth.change_group', login_url='/admin/')
def update_members(request,group):
    '''
    Updates the users of a group for use in the django databases.
    '''
    # Call the update_group_members method in utils.py to update the groups.
    result = utils.update_group_members(group)

    # Grab all of the members of the group from the group web service. If the group doesn't exist, stop further processing.
    #result, group_exists = utils.get_group_members(group)
    
    if not result['is_updated']:
        # No group was found. Return a error message. 
        args = {
            'title':'Group: %s - Update members' % group,
            'group': group,
            'error': result['error'] + " No group update was performed.",
        }
        return render_to_response('update.html',args,context_instance=RequestContext(request))

    args = result
    args['group'] = group
    args['title'] = 'Group: %s - Update members' % group,
 
    return render_to_response('update.html',args,context_instance=RequestContext(request))
    
