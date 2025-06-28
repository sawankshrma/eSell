from django.core.management.base import BaseCommand
from django.core.management import call_command
from auctions.models import Listing  # replace with a model that must exist

class Command(BaseCommand):
    help = 'Seeds initial data if DB is empty'

    def handle(self, *args, **kwargs):
        if Listing.objects.exists():
            self.stdout.write(self.style.NOTICE("Database already has data, skipping seed."))
        else:
            self.stdout.write(self.style.SUCCESS("Seeding initial data..."))
            call_command('loaddata', 'fixtures/mydata.json')
