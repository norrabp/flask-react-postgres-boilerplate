from enum import Enum
from backend.config.development import DevelopmentConfig
from backend.config.production import ProductionConfig
from backend.config.testing import TestConfig
import os

class Environment(str, Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    TESTING = 'testing'

ENVIRONMENT: Environment = Environment(os.environ.get('ENVIRONMENT', 'development'))

CONFIG_MAP = {
    Environment.DEVELOPMENT: DevelopmentConfig,
    Environment.PRODUCTION: ProductionConfig,
    Environment.TESTING: TestConfig
}

CONFIG = CONFIG_MAP[ENVIRONMENT]