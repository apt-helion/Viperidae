import datetime

from peewee import *
from pymongo import MongoClient
from .config import Config

database = Config.DATABASE

# monkey patch the DateTimeField to add support for the isoformt which is what
# peewee exports as from DataSet
DateTimeField.formats.append('%Y-%m-%dT%H:%M:%S')
DateField.formats.append('%Y-%m-%dT%H:%M:%S')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    # Example usage
    #       doc = AdminDocument.create()
    #       doc.apply(request.form)
    #       doc.apply(request.json)
    #       doc.apply(request.json, required=['filename'], dates=['uploaddate'])
    def apply_request(self, source, ignore = None, required = None, dates = None):

        for field in self._meta.get_sorted_fields():
            data = source.get(field)
            if field == "id": continue
            if field in ignore: continue
            # Verify in required_fields
            if field in required and data == None:
                return {'error': 'Empty required field'}
            if field in dates:
                data = "" # strp==]===
            if data is None or data == "": continue
            self.__dict__[field] = data

        return ""

    class Meta:
        database = database

class User(BaseModel):
    user = CharField(column_name='user_id', null=False, primary_key=True)
    username = CharField(column_name='username', null=False)
    password = CharField(column_name='password', null=False)
    email = CharField(column_name='email', null=False)

    class Meta:
        table_name = 'Users'

class Client(BaseModel):
    client = CharField(column_name='client_id', null=False, primary_key=True)
    secret = CharField(column_name='client_secret', null=False)
    name = CharField(column_name='name', null=False)
    website = CharField(column_name='website', null=False)
    description = CharField(column_name='description', null=False)

    user = ForeignKeyField(
        column_name='user_id',
        field='user',
        model=User,
        null=False)

    @classmethod
    def get_pages(cls):
        mongo_client = MongoClient('localhost', 27017)
        database     = mongo_client.pages
        collection   = database[cls.name]

        return collection

    class Meta:
        table_name = 'Clients'

class Token(BaseModel):
    token = CharField(column_name='token_id', null=False, primary_key=True)
    refresh_token = CharField(column_name='refresh_token', null=False)
    expiry = DateTimeField(column_name='expiry', null=False)

    client = ForeignKeyField(
        column_name='client_id',
        field='client',
        model=Client,
        null=False)

    class Meta:
        table_name = 'Tokens'
