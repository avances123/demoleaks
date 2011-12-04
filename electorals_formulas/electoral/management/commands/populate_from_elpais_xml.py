from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<populate_from_elpais>'
    help = 'Populate database from ElPais.com XML file'

    def handle(self, *args, **options):
        #for poll_id in args:
        #    try:
        #        poll = Poll.objects.get(pk=int(poll_id))
        #    except Poll.DoesNotExist:
        #        raise CommandError('Poll "%s" does not exist' % poll_id)

        self.stdout.write('Successfully populate database from ElPais.com XML "%s"\n')

