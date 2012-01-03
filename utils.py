import httplib
from django.conf import settings

from uw_gws.BeautifulSoup.BeautifulSoup import BeautifulSoup

def get_group_info(group):
    URL = settings.URL + 'group/%s/' % group

    connection = httplib.HTTPSConnection(settings.GWS_HOST,settings.GWS_PORT,settings.KEY_FILE,settings.CERT_FILE)
    connection.request(settings.METHOD,URL)
    
    response = connection.getresponse()
    body = response.read()

    connection.close()

    # Use BeautifulSoup to output the html in a cleaner format.
    body = BeautifulSoup(body).prettify()
    return body


def get_group_members(group):
    URL = settings.URL + 'group/%s/member' % group
    connection = httplib.HTTPSConnection(settings.GWS_HOST,settings.GWS_PORT,settings.KEY_FILE,settings.CERT_FILE)
    connection.request(settings.METHOD,URL)
    

    response = connection.getresponse()
    body = response.read()
    connection.close()
    
    # Use BeautifulSoup to output the html in a cleaner format.
    body = BeautifulSoup(body)

    members = []
    for member in body('a',{'type':'uwnetid'}):
        members.append(member.string)

    return members

