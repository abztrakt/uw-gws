from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
import uw_gws.utils as utils

class Command(BaseCommand):
    args = ''
    help = 'Updates all of the auth.groups via Groups Web Service'

    def handle(self, *args, **options):
        groups = Group.objects.all()
        self.stdout.write('Starting update...\n')
        for group in groups:
            result = utils.update_group_members(group.name)

            # Write a helpful message regarding the update status.
            message = ''

            if result['is_updated']:
                current = result['current_users']
                created = result['created_users']
                removed = result['removed_users']
                added = result['added_users']
                
                if not created and not removed and not added:
                    message = 'No updated needed for group "%s".' % (group.name) 
                else:
                    message = 'Successfully updated group "%s". Created: %d, Added:%d, Removed: %d.' % (group.name, len(created),len(added),len(removed))
            else:
                message = 'Group "%s" cannot be found via Group Web Service. Update failed.' % (group.name)

            self.stdout.write('%s\n' % message)
        
        self.stdout.write('Update finished.\n')
