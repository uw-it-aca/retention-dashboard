import json
from django.test import TestCase, Client
from retention_dashboard.tests import TestViewApi
from retention_dashboard.dao.data import get_filtered_data, get_weeks_with_data
from retention_dashboard.tests import create_upload
from retention_dashboard.models import DataPoint
from retention_dashboard.dao.auth import get_type_authorizations


class AuthTest(TestViewApi):
    def test_get_auth_list(self):
        request = self.get_request('/', 'javerage', 'u_test_group')
        types = get_type_authorizations(request)
        self.assertCountEqual(types, ["Premajor", "EOP", "International"])

        with self.settings(PREMAJOR_USERS_GROUP='foo'):
            types = get_type_authorizations(request)
            self.assertCountEqual(types, ["EOP", "International"])
        with self.settings(INTERNATIONAL_USERS_GROUP='foo'):
            types = get_type_authorizations(request)
            self.assertCountEqual(types, ["Premajor", "EOP"])
        with self.settings(EOP_USERS_GROUP='foo'):
            types = get_type_authorizations(request)
            self.assertCountEqual(types, ["Premajor", "International"])
