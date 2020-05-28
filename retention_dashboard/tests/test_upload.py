from django.test import TestCase
from retention_dashboard.tests import create_upload
from retention_dashboard.models import DataPoint
from retention_dashboard.utilities.upload import process_upload


class UploadTest(TestCase):

    def test_process_upload(self):
        upload = create_upload()
        process_upload(upload)
        data_points = DataPoint.objects.all()
        self.assertEqual(data_points.count(), 5961)
