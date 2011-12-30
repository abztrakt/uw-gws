import httplib
from django.conf import settings

def get_group_info(group):
    URL = settings.URL + 'group/%s/members' % group

    connection = httplib.HTTPSConnection(settings.GWS_HOST,settings.GWS_PORT,settings.KEY_FILE,settings.CERT_FILE)
    connection.request(settings.METHOD,URL)
    
    response = connection.getresponse()
    body = response.read()

    connection.close()

    return body

