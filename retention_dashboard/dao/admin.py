import logging
from django.conf import settings
from google.cloud import storage
from google.cloud.exceptions import NotFound


class GCSDataDao():

    def __init__(self):
        pass

    def get_gcs_client(self):
        return storage.Client()

    def get_gcs_timeout(self):
        return getattr(settings, "GCS_TIMEOUT", 60)

    def get_gcs_bucket_name(self):
        return getattr(settings, "RAD_DATA_BUCKET_NAME", "")

    def get_files_list(self, path="rad_data/"):
        """
        Returns list of file names in a GCS bucket at the given path.

        :param path: Path to list files at
        :type path: str
        """
        gcs_client = self.get_gcs_client()
        gcs_bucket_name = self.get_gcs_bucket_name()
        bucket = gcs_client.get_bucket(gcs_bucket_name)
        files = []
        for blob in gcs_client.list_blobs(bucket, prefix=path):
            if blob.name.endswith("csv"):
                files.append((blob.name, blob.name))
        return files

    def download_from_gcs_bucket(self, url_key):
        """
        Downloads file a given url_key path from the configured GCS bucket.

        :param url_key: Path of the content to upload
        :type url_key: str
        :param content: Content to upload
        :type content: str or file object
        """
        gcs_client = self.get_gcs_client()
        gcs_bucket_name = self.get_gcs_bucket_name()
        bucket = gcs_client.get_bucket(gcs_bucket_name)
        try:
            blob = bucket.get_blob(
                url_key,
                timeout=self.get_gcs_timeout())
            content = blob.download_as_string(
                timeout=self.get_gcs_timeout())
            if content:
                return content.decode('utf-8')
        except NotFound as ex:
            logging.error(f"gcp {url_key}: {ex}")
            raise