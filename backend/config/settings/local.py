from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS += ["*"]

CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "DB_NAME",
#         "USER": "DB_USER",
#         "PASSWORD": "PASSWORD",
#         "HOST": "DB_HOST",
#         "PORT": "5432",
#     }
# }


# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "app_formatter": {
            "format": "[{levelname}] [{name}:{lineno} {funcName}] {message}",
            "style": "{",
        },
        "simple_formatter": {
            "format": "{message}",
            "style": "{",
        },
    },
    "handlers": {
        "app_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "app_formatter",
        },
        "simple_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple_formatter",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["app_console"],
            "level": "DEBUG",
        },
        "request": {
            "handlers": ["simple_console"],
            "level": "INFO",
        },
        "django.request": {
            "level": "ERROR",
        },
        # 'django.db.backends': {
        #     'handlers': ['simple_console'],
        #     'level': 'DEBUG',
        # },
    },
}
