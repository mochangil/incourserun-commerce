import datetime
from pathlib import Path
import os
from dotenv import load_dotenv
# from iamport import Iamport

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "pj%2ze09(g)i^joilp-f8gvs)6ou_m036u3ejs^ky&9nse5k92"

ALLOWED_HOSTS = [".elasticbeanstalk.com"]

LOCAL_APPS = [
    "app.staticfile",
    "app.user.apps.UserConfig",
    "app.cart.apps.CartConfig",
    "app.product.apps.ProductConfig",
    "app.order.apps.OrderConfig",
    "app.review.apps.ReviewConfig"
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "django_filters",
    "django_hosts",
    "drf_spectacular",
    "multiselectfield",
    "storages",
    "import_export",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS


MIDDLEWARE = [
    "django_hosts.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.RequestLogMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "ko"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

SITE_NAME = "인코스런"
SITE_LOGO = "img/logo.png"  # static/img/logo.png 변경
SITE_URL = os.getenv("SITE_URL") # 프론트엔드 url

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_ROOT = BASE_DIR / "media"
# MEDIA_URL = "/media/"

# AUTH_USER_MODEL
AUTH_USER_MODEL = "user.User"

# APPLICATION
WSGI_APPLICATION = "config.wsgi.application"

# HOST
DEFAULT_HOST = "api"
ROOT_HOSTCONF = "config.hosts"
ROOT_URLCONF = "config.urls.api"


# MODEL ID
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}


# DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "config.authentication.Authentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": (
        # "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.AllowAny",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# SPECTACULAR
SPECTACULAR_SETTINGS = {
    "TITLE": f"{SITE_NAME} API",
    "DESCRIPTION": f"{SITE_NAME}의 API입니다.",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/v[0-9]",
    "DISABLE_ERRORS_AND_WARNINGS": True,
    "SORT_OPERATIONS": False,
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "none",
        "defaultModelRendering": "example",  # example, model
        "defaultModelsExpandDepth": 0,
        "deepLinking": True,
        "displayRequestDuration": True,
        "persistAuthorization": True,
        "syntaxHighlight.activate": True,
        "syntaxHighlight.theme": "agate",
        # 'preauthorizeApiKey': False,
    },
    "PREPROCESSING_HOOKS": [],  # pre hook 추가
    "SERVE_INCLUDE_SCHEMA": False,
    "APPEND_COMPONENTS": {"securitySchemes": {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}},
    "SECURITY": [
        {
            "Bearer": [],
        }
    ],
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
}

# S3
AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = "incourserun-commerce"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=864000"}
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = "public-read"
AWS_LOCATION = "media"
AWS_S3_SECURE_URLS = True
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
MEDIAFILES_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"

# File Upload
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]
MAX_UPLOAD_SIZE = 5242880
DATA_UPLOAD_MAX_MEMORY_SIZE = None
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# KAKAO
KAKAO_CLIENT_ID = os.getenv('KAKAO_CLIENT_ID')
KAKAO_CLIENT_SECRET = os.getenv('KAKAO_CLIENT_SECRET')
KAKAO_REDIRECT_URI = SITE_URL + "/login/kakao/callback"

'''
KAKAO LOGIN URL
https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=${KAKAO_CLIENT_ID}&redirect_uri=${SOCIAL_REDIRECT_URL}&state=kakao
https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=29bebceec427c5cb9e5a35627b29036e&redirect_uri=http://localhost:3000/login/social/callback&state=kakao
'''

# Postgre
DB_USERNAME = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Iamport
IMP_KEY = os.getenv('IAMPORT_KEY')
IMP_SECRET = os.getenv('IAMPORT_SECRET')
ORDER_ROOT = "http://127.0.0.1:8000/v1/orders"

# iamport = Iamport(
#     imp_key=IMP_KEY,
#     imp_secret=(
#         IMP_SECRET
#     )
# )