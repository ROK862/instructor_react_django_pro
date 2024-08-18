from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs an endpoint for all flexers to access chats in realtime.'

    def add_arguments(self, parser):
        # Add any arguments your command needs here
        pass

    def handle(self, *args, **options):
        # Your command logic goes here
        self.stdout.write(self.style.SUCCESS('Successfully ran my custom command'))