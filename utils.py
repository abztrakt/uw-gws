import httplib
from django.conf import settings
import xml.dom.minidom

def get_group_info(group):
    URL = settings.URL + 'group/%s/' % group

    connection = httplib.HTTPSConnection(settings.GWS_HOST,settings.GWS_PORT,settings.KEY_FILE,settings.CERT_FILE)
    connection.request(settings.METHOD,URL)
    
    response = connection.getresponse()
    body = response.read()
    connection.close()

    if response.status == 404:
        return ("Error: The group '%s' was not found in the Groups Web Service, instead a 404 error was returned." % group, False)

    return (body,True)


def get_group_members(group):
    '''
    Returns the members of a group via Groups Web Service.
    @return (status, members)
    '''

    URL = settings.URL + 'group/%s/member' % group
    connection = httplib.HTTPSConnection(settings.GWS_HOST,settings.GWS_PORT,settings.KEY_FILE,settings.CERT_FILE)
    connection.request(settings.METHOD,URL)

    response = connection.getresponse()
    body = response.read()
    connection.close()
     
    if response.status == 404:
        return ("Error: The group '%s' was not found in the Groups Web Service, instead a 404 error was returned." % group, False)

    # Use XHTML parsing to get the group members.
    group_members_array = []
    dom = xml.dom.minidom.parseString(body)

    listitems = dom.getElementsByTagName('li')
    for member in listitems:
        m = member.firstChild
        if (m is not None and m.getAttribute('class') == 'member'):
            group_members_array.append(m.firstChild.data)

    return (group_members_array,True)


def update_members(group):
    '''
    Updates the users of a group for use in the django databases.
    '''
    
    # Grab all of the members of the group from the group web service. If the group doesn't exist, stop further processing.
    result = get_group_members(group)
    
    if result[1]:
        # If the group exists in the web service, get or create the group.
        django_group,django_group_created = Group.objects.get_or_create(name=group)

        # Grab all of the members of the group in django.
        users = sorted([user.username for user in django_group.user_set.all()])
        result = sorted(result[0])

        if users != result:
            # Grab or create the users from the group and add them to the group.
            for member in result:
                user,user_created = User.objects.get_or_create(username=member)
                
                if user_created:
                    # Create the user. Set default permissions.
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                
                # Now add them to the group.
                user.groups.add(django_group)
                user.save()

            #Now check which people weren't in the group and remove them.
            removed_users = [user for user in users if user not in result]
            for member in removed_users:
                user = User.objects.get(username=member)
                user.groups.remove(django_group)

