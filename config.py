#здесь крч конфигурации типа чтоб все работало
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #Смотрит откуда всзять БД
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    #отслеживание изменений
    SQLALCHEMY_TRACK_MODIFICATIONS = False