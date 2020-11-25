from django.core.management.base import BaseCommand, CommandError
import unittest

class Command(BaseCommand):
    help = 'Run all unit tests'

    def handle(self, *args, **options):
        loader = unittest.TestLoader()
        start_dir = 'tests/'
        suite = loader.discover(start_dir)

        runner = unittest.TextTestRunner()
        runner.run(suite)
