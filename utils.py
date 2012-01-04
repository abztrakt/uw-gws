import httplib
from django.conf import settings
import xml.dom.minidom

from uw_gws.BeautifulSoup.BeautifulSoup import BeautifulSoup

def get_group_info(group):
    URL = settings.URL + 'group/%s/' % group

    connection = httplib.HTTPSConnection(settings.GWS_HOST,settings.GWS_PORT,settings.KEY_FILE,settings.CERT_FILE)
    connection.request(settings.METHOD,URL)
    
    response = connection.getresponse()
    body = response.read()
    connection.close()

    if response.status == 404:
        return (False,"Error: The group '%s' was not found in the Groups Web Service, instead a 404 error was returned." % group)
    

    # Use BeautifulSoup to output the html in a cleaner format.
    body = BeautifulSoup(body).prettify()
    return (True,body)


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
        return (False,"Error: The group '%s' was not found in the Groups Web Service, instead a 404 error was returned." % group)

    # Use XHTML parsing to get the group members.
    group_members_array = []
    dom = xml.dom.minidom.parseString(body)

    listitems = dom.getElementsByTagName('li')
    for member in listitems:
        m = member.firstChild
        if (m is not None and m.getAttribute('class') == 'member'):
            group_members_array.append(m.firstChild.data)

    return (True,group_members_array)

