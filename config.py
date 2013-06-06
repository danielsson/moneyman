from os.path import abspath


class Config:
    #CONFIG
    DATABASE = 'moneyman.db'
    DEBUG = False
    SECRET_KEY = 'devkey'
    USERNAME = 'admin'
    PASSWORD = 'default'

    UPLOAD_FOLDER = "uploaded_files"
    ALLOWED_EXTENSIONS = set(['csv'])

    CLF_STORAGE = abspath(UPLOAD_FOLDER + "/clfs")

class DevConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass
