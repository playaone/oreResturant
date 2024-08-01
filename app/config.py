import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ENGINE_OPTIONS={
        "pool_pre_ping": True,
        "pool_recycle": 3600
    }
    PAYSTACK_KEY = os.environ.get('PAYSTACK_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')