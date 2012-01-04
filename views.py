from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.models import User,Group

# Import the models.py to grab the group model.
from uw_gws.models import UWGWSGroup 

# Utils.py contains the get request needed to process the information.
import utils

def home_page(request):

    args = {
        'title': 'Home',
    }
    return render_to_response('home.html',args,context_instance=RequestContext(request))


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

# TODO: Possibly move this code to a backend for django.
def update_members(request,group):
    '''
    Updates the users of a group for use in the django databases.
    '''
    
    # First, get or create the group.
    django_group,django_group_created = Group.objects.get_or_create(name=group)

    # Grab all of the members of the group in django and via group web service.
    users = sorted([user.username for user in django_group.user_set.all()])
    result = utils.get_group_members(group)
    
    if not result[0]:
        # No group was found. Return a error message. 
        args = {
            'title':'Group: %s - Update members' % group,
            'group': group,
            'error': result[1],
        }
        return render_to_response('update.html',args,context_instance=RequestContext(request))
    else:
        result = sorted(result[1])

    # Primarily used for testing, these lists will be populated with any updates to the database regarding groups.
    current_users = []
    created_users = []
    removed_users = []

    if users == result:
        # We have nothing to update.
        current_users = users
    else:
        # Grab or create the users from the group and add them to the group.
        for member in result:
            user,user_created = User.objects.get_or_create(username=member)
            
            if user_created:
                # TODO: Check to see how to deal with default permissions.
                # Create the user. Set default permissions.
                user.is_staff = False
                user.is_superuser = False
                user.save()
                created_users.append(user)
            else:
                current_users.append(user)

            # Now add them to the group.
            user.groups.add(django_group)
            user.save()

        #Now check which people weren't in the group and remove them.
        removed_users = [user for user in users if user not in result]
        for member in removed_users:
            user = User.objects.get(username=member)
            user.groups.remove(django_group)

    args = {
        'title':'Group: %s - Update members' % group,
        'group': group,
        'current_users': current_users,
        'created_users': created_users,
        'removed_users': removed_users,
    }

    return render_to_response('update.html',args,context_instance=RequestContext(request))
    
