from discord import emoji
from peewee import *

from settings import DATABASE


database = PostgresqlDatabase(
    database=DATABASE['name'],
    **{'user': DATABASE['user'], 'password': DATABASE['password'], 'host': DATABASE['host'], 'port': DATABASE['potr']}
)


class BaseModel(Model):
    class Meta:
        database = database


class EventType(BaseModel):

    guild_id = BigIntegerField()
    type_id = BigIntegerField()
    title = TextField()
    description = TextField(null=True)
    role_id = BigIntegerField()
    role_color = TextField(null=True)
    created_at = DateTimeField()
    started_at = DateTimeField(null=True)
    disabled_at = DateTimeField(null=True)
    enabled = BooleanField(null=True)
    message_id = BigIntegerField(null=True)
    channel_id = BigIntegerField(null=True)
    emoji = TextField(null=True)

    class Meta:
        table_name = 'event_type'
        primary_key = False


class Event(BaseModel):

    guild_id = BigIntegerField()
    event_id = BigIntegerField()
    type_id = BigIntegerField()
    title = TextField()
    details = TextField(null=True)
    role_id = BigIntegerField()
    role_color = TextField(null=True)
    created_at = DateTimeField()
    started_at = DateTimeField(null=True)
    disabled_at = DateTimeField(null=True)
    enabled = BooleanField(null=True)
    message_id = BigIntegerField(null=True)
    channel_id = BigIntegerField(null=True)
    emoji = TextField(null=True)
    
    class Meta:
        table_name = 'event'
        primary_key = False


class Guild(BaseModel):

    guild_id = BigIntegerField()
    moderator_role_id = BigIntegerField(null=True)
    title = TextField()

    class Meta:
        table_name = 'guild'
        primary_key = False