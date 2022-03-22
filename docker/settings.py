from .base_settings import *
from google.oauth2 import service_account
import os

INSTALLED_APPS += [
    'retention_dashboard.apps.RetentionDashboardConfig',
    'webpack_loader',
    'userservice'
]

MIDDLEWARE += ['userservice.user.UserServiceMiddleware']

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'retention_dashboard/bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'retention_dashboard', 'static', 'webpack-stats.json'),
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':  True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    }
]

if os.getenv('ENV') == 'localdev':
    DEBUG = True
    ALLOWED_USERS_GROUP = 'u_test_group'
    ADMIN_USERS_GROUP = ALLOWED_USERS_GROUP
    PREMAJOR_USERS_GROUP = ALLOWED_USERS_GROUP
    EOP_USERS_GROUP = ALLOWED_USERS_GROUP
    INTERNATIONAL_USERS_GROUP = ALLOWED_USERS_GROUP
    ISS_USERS_GROUP = ALLOWED_USERS_GROUP
    TACOMA_USERS_GROUP = ALLOWED_USERS_GROUP
    ATHLETIC_USERS_GROUP = ALLOWED_USERS_GROUP
    ENGINEERING_USERS_GROUP = ALLOWED_USERS_GROUP
    MOCK_SAML_ATTRIBUTES = {
        'uwnetid': ['javerage'],
        'affiliations': ['student', 'member', 'alum', 'staff', 'employee'],
        'eppn': ['javerage@washington.edu'],
        'scopedAffiliations': ['student@washington.edu',
                               'member@washington.edu'],
        'isMemberOf': ['u_test_group', 'u_admin_group'],
    }
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/app/rad_data')
else:
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_PROJECT_ID = os.getenv('STORAGE_PROJECT_ID', '')
    GS_BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME', '')
    GS_LOCATION = os.getenv('STORAGE_LOCATION', 'rad_data')
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        '/gcs/credentials.json')

    if os.getenv('ENV') == 'prod':
        ALLOWED_USERS_GROUP = 'u_acadev_retention-prod'
        ADMIN_USERS_GROUP = 'u_acadev_retention-prod-admin'
        PREMAJOR_USERS_GROUP = "u_acadev_retention-prod-premajor"
        EOP_USERS_GROUP = "u_acadev_retention-prod-eop"
        INTERNATIONAL_USERS_GROUP = "u_acadev_retention-prod-international"
        ISS_USERS_GROUP = "u_acadev_retention-prod-iss"
        TACOMA_USERS_GROUP = "u_acadev_retention-prod-tacoma"
        ATHLETIC_USERS_GROUP = "u_acadev_retention-prod-athletic"
        ENGINEERING_USERS_GROUP = "u_acadev_retention-prod-engineering"
    else:
        ALLOWED_USERS_GROUP = 'u_acadev_retention-test'
        # ADMIN_USERS_GROUP = 'u_acadev_retention-test-admin'
        ADMIN_USERS_GROUP = ALLOWED_USERS_GROUP
        PREMAJOR_USERS_GROUP = ALLOWED_USERS_GROUP
        EOP_USERS_GROUP = ALLOWED_USERS_GROUP
        INTERNATIONAL_USERS_GROUP = ALLOWED_USERS_GROUP
        ISS_USERS_GROUP = ALLOWED_USERS_GROUP
        TACOMA_USERS_GROUP = ALLOWED_USERS_GROUP
        ATHLETIC_USERS_GROUP = ALLOWED_USERS_GROUP
        ENGINEERING_USERS_GROUP = ALLOWED_USERS_GROUP

    GA_KEY = os.getenv("GA_KEY")
