from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
import uw_gws.utils as utils

class Command(BaseCommand):
    args = ''
    help = 'Updates all of the auth.groups membership via Groups Web Service'

    def handle(self, *args, **options):
        groups = Group.objects.all()
        
        #Determine how verbose the output should be in the command line.
        verbosity = int(options['verbosity'])

        if verbosity > 0:
            self.stdout.write('Starting update...\n')
            
        #Count how many updates were performed.
        updated_count = 0
        unaffect_count = 0
        failed_count = 0

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
                    unaffect_count += 1
                else:
                    message = 'Successfully updated group "%s". Created: %d, Added:%d, Removed: %d.' % (group.name, len(created),len(added),len(removed))
                    updated_count += 1
            else:
                message = 'Group "%s" cannot be found via Group Web Service. Update failed.' % (group.name)
                failed_count += 1

            if verbosity > 1:
                self.stdout.write('%s\n' % message)

        if verbosity > 0:
            self.stdout.write('Update finished. Updated: %d, Unaffected: %d, Failed: %d\n' % (updated_count, unaffect_count, failed_count) )
