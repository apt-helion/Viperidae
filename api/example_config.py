import os
from peewee import MySQLDatabase, SqliteDatabase

"""
    CHANGE PLACEHOLDER VALUES AND RENAME TO config.py
"""

class ConfigBase(object):
    """MySQL Database handler"""
    DATABASE = MySQLDatabase('<database>',
                             **{'charset': 'utf8',
                                'use_unicode': True,
                                'user': '<user>',
                                'passwd': '<password>'})

if 'DEVBOX' in os.environ:
    # Dev Box
    if os.environ['DEVBOX'] == '<devboxname>':
        class Config(ConfigBase):
            DATABASE = MySQLDatabase(
                '<database>',
                user='<user>',
                password='<password>',
            )

else:
    class Config(ConfigBase): pass
