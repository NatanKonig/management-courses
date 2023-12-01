from peewee import *


class BaseModel(Model):
    
    class Meta:
        database = db


class Usuario(BaseModel):
    