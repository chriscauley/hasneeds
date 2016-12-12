import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '8d&j_3zjc^4!)+3_s0!waya72jhx8j=3iryhexz=uq)9t)vbcs'

DEBUG = False

ALLOWED_HOSTS = ["*"]

MIDDLEWARE_CLASSES = [
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
  { 
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.request',
        'django.template.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'lablackey.context.public_settings',
        #'social.apps.django_app.context_processors.backends',
        #'social.apps.django_app.context_processors.login_redirect',
      ],
    },
  },
]

AUTHENTICATION_BACKENDS = (
  #'social.backends.google.GoogleOAuth2',
  #'social.backends.twitter.TwitterOAuth',
  'social.backends.slack.SlackOAuth2',
  'lablackey.auth.EmailOrUsernameModelBackend',
  'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_SLACK_SCOPE = ['team:read']

# Above comments are useful for social auth. Requires these keys in a private file
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""

SOCIAL_AUTH_TWITTER_SECRET = ""
SOCIAL_AUTH_TWITTER_KEY = ""

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = USE_L10N = USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../.static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../.media')
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = "/"

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  # other finders..
  'compressor.finders.CompressorFinder',
)

LESS_EXECUTABLE = 'lessc'
COMPRESS_PRECOMPILERS = [
  ('text/less', "lessc {infile} {outfile} --line-numbers=comments;autoprefixer-cli {outfile} -o {outfile}"),
  ('riot/tag', 'riot {infile} {outfile}'),
]

FAVICON = '/static/favicon.ico'

SOCIAL_AUTH_PIPELINE = (
  'social.pipeline.social_auth.social_details',
  'social.pipeline.social_auth.social_uid',
  'social.pipeline.social_auth.auth_allowed',
  'social.pipeline.social_auth.social_user',
  'social.pipeline.user.get_username',
  'slackauth.views.get_team',
  'social.pipeline.user.create_user',
  'social.pipeline.social_auth.associate_user',
  'social.pipeline.social_auth.load_extra_data',
  'social.pipeline.user.user_details',
)

ALLOWED_SLACK_DOMAINS = [
  'indyhall',
  #'txrxlabs',
]

PUBLIC_SETTINGS = ['DEBUG','ALLOWED_SLACK_DOMAINS']

#GRAPHENE = {
#    'SCHEMA': 'board.schema.schema',
#}
