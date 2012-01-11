import httplib
from django.conf import settings
from django.contrib.auth.models import User,Group
import xml.dom.minidom

def get_group_info(group):
    '''
    Returns the information of a group via Groups Web Service in XHTML.
    @return (dictionary,boolean)
    '''
    URL = settings.URL + 'group/%s/' % group

    connection = httplib.HTTPSConnection(settings.GWS_HOST,settings.GWS_PORT,settings.KEY_FILE,settings.CERT_FILE)
    connection.request(settings.METHOD,URL)
    
    response = connection.getresponse()
    body = response.read()
    connection.close()

    
    if response.status == 404:
        return ({'error':"Error: The group '%s' was not found in the Groups Web Service, instead a 404 error was returned." % group}, False)

    return ({'group_info':body},True)


def get_group_members(group):
    '''
    Returns the members of a group via Groups Web Service.
    @return (dictionary,boolean)
    '''

    URL = settings.URL + 'group/%s/member' % group
    connection = httplib.HTTPSConnection(settings.GWS_HOST,settings.GWS_PORT,settings.KEY_FILE,settings.CERT_FILE)
    connection.request(settings.METHOD,URL)

    response = connection.getresponse()
    body = response.read()
    connection.close()
     
    if response.status == 404:
        return ({'error':"Error: The group '%s' was not found in the Groups Web Service, instead a 404 error was returned." % group}, False)

    # Use XHTML parsing to get the group members.
    group_members_array = []
    dom = xml.dom.minidom.parseString(body)

    listitems = dom.getElementsByTagName('li')
    for member in listitems:
        m = member.firstChild
        if (m is not None and m.getAttribute('class') == 'member'):
            group_members_array.append(m.firstChild.data)

    return ({'group_members':group_members_array},True)


def update_group_members(group):
    '''
    Updates the users of a group for use in the django databases.
    '''
    
    # Grab all of the members of the group from the group web service. If the group doesn't exist, stop further processing.
    result, group_exists = get_group_members(group)
    
    if group_exists:
        # If the group exists in the web service, get or create the group.
        django_group,django_group_created = Group.objects.get_or_create(name=group)

        # Grab all of the members of the group in django.
        users = sorted([user.username for user in django_group.user_set.all()])
        result = sorted(result['group_members'])

        # Primarily used for testing, these lists will be populated with any updates to the database regarding groups.
        current_users = []
        created_users = []
        removed_users = []
        added_users = []

        if users == result:
            current_users = users
        else:
            # Grab or create the users from the group and add them to the group.
            for member in result:
                user,user_created = User.objects.get_or_create(username=member)
                
                if user_created:
                    # Create the user. Set default permissions.
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    created_users.append(user)

                if user.username in users:
                    current_users.append(user)
                elif not user_created and user.username not in users:
                    added_users.append(user)

                # Now add them to the group.
                user.groups.add(django_group)
                user.save()

            #Now check which people weren't in the group and remove them.
            removed_users = [user for user in users if user not in result]
            for member in removed_users:
                user = User.objects.get(username=member)
                user.groups.remove(django_group)

        result = {
            'current_users': current_users,
            'created_users': created_users,
            'removed_users': removed_users,
            'added_users': added_users,
            'is_updated': True,
        }

        return result
    else:
        result['is_updated'] = False
        return result
