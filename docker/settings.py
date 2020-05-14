from .base_settings import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'webpack_loader',
    'retention_dashboard',
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
if os.getenv('ENV') == 'prod':
    ALLOWED_USERS_GROUP = 'u_acadev_retention-prod'
    ADMIN_USERS_GROUP = 'u_acadev_retention-prod-admin'
    PREMAJOR_USERS_GROUP = "u_acadev_retention-prod-premajor"
    EOP_USERS_GROUP = "	u_acadev_retention-prod-eop"
    INTERNATIONAL_USERS_GROUP = "u_acadev_retention-prod-international"
elif os.getenv('ENV') == 'eval':
    ALLOWED_USERS_GROUP = 'u_acadev_retention-test'
    # ADMIN_USERS_GROUP = 'u_acadev_retention-test-admin'
    ADMIN_USERS_GROUP = ALLOWED_USERS_GROUP
    PREMAJOR_USERS_GROUP = ALLOWED_USERS_GROUP
    EOP_USERS_GROUP = ALLOWED_USERS_GROUP
    INTERNATIONAL_USERS_GROUP = ALLOWED_USERS_GROUP
elif os.getenv("ENV") == "localdev":
    DEBUG = True
    ALLOWED_USERS_GROUP = 'u_test_group'
    ADMIN_USERS_GROUP = ALLOWED_USERS_GROUP
    PREMAJOR_USERS_GROUP = ALLOWED_USERS_GROUP
    EOP_USERS_GROUP = ALLOWED_USERS_GROUP
    INTERNATIONAL_USERS_GROUP = ALLOWED_USERS_GROUP
    MOCK_SAML_ATTRIBUTES = {
        'uwnetid': ['javerage'],
        'affiliations': ['student', 'member', 'alum', 'staff', 'employee'],
        'eppn': ['javerage@washington.edu'],
        'scopedAffiliations': ['student@washington.edu',
                               'member@washington.edu'],
        'isMemberOf': ['u_test_group', 'u_admin_group'],
    }


from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy('saml_login')
LOGOUT_URL = reverse_lazy('saml_logout')
