# config.py

class Config(object):
    """
    Global configuration
    """

    # environment configuration below here


class DevelopmentConfig(Config):
    """
    Development
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
