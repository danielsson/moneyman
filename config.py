class Config:
    #CONFIG
    DATABASE = 'moneyman.db'
    DEBUG = True
    SECRET_KEY = 'devkey'
    USERNAME = 'admin'
    PASSWORD = 'default'

    UPLOAD_FOLDER = "uploaded_files"
    ALLOWED_EXTENSIONS = set(['csv'])

class DevConfig(Config):
    pass

class ProductionConfig(Config):
    pass
