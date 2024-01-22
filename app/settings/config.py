import logging
import os

logger = logging.getLogger("azent")

mongo_db_password = os.environ.get("mongo_db_password", default=None)
jwt_secret_key = os.environ.get("jwt_secret_key", default=None)
redis_url = os.environ.get("redis_url", default=None)


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    NAME = "development"  # change it to APP_ENV
    SQLALCHEMY_DATABASE_URI = 'sqlite:///logisticsnow.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'logisticsnow1234567'
    JWT_SECRET_KEY = 'logisticsnow12345'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_TYPE = 'Bearer'
    MAX_PER_PAGE = 20


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class DockerConfig(DevelopmentConfig):
    DEBUG = True


class UnitTestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    NAME = "unit_testing"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///logisticsnow.db'


class TestingConfig(Config):
    """Configurations for UAT."""

    DEBUG = True
    NAME = "testing"


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
    NAME = "staging"


class ProductionConfig(Config):
    """Configurations for Production."""

    DEBUG = False
    TESTING = False
    NAME = "production"


app_config = {"development": DevelopmentConfig, "docker": DockerConfig, "testing": TestingConfig,
    "unit_testing": UnitTestingConfig, "staging": StagingConfig, "production": ProductionConfig, }
