# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import unittest

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run all unit tests'

    def handle(self, *args, **options):
        loader = unittest.TestLoader()
        start_dir = 'retention_dashboard/tests/'
        suite = loader.discover(start_dir)
        runner = unittest.TextTestRunner()
        runner.run(suite)
