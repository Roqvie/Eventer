import typing

from . import models, errors


def addNewGuild(guild_id: typing.Union[int], guild_name: typing.Union[str]):
    guild = models.Guild.create(guild_id=guild_id, title=guild_name)


# Getting all records
#
@errors.syncErrorHandler
def getAllGuilds() -> typing.List[models.Guild]:
    guilds = models.Guild.select()

    return guilds[::]


@errors.syncErrorHandler
def getAllEventTypes(guild_id: typing.Union[int], enabled: typing.Optional[bool] = None) -> typing.List[models.EventType]:
    if enabled is None:
        event_types = models.EventType.select().where(
            models.EventType.guild_id == guild_id
        )
    else:
        event_types = models.EventType.select().where(
            (models.EventType.enabled == enabled) & 
            (models.EventType.guild_id == guild_id)
        )

    return event_types[::]


@errors.syncErrorHandler
def getAllEvents(guild_id: typing.Union[int], enabled: typing.Optional[bool] = None) -> typing.List[models.Event]:
    if enabled is None:
        events = models.Event.select().where(
            models.Event.guild_id == guild_id
        )
    else:
        events = models.Event.select().where(
            (models.Event.enabled == enabled) &
            (models.Event.guild_id == guild_id)
        )

    return events[::]

# Getting records by ID
# 

@errors.syncErrorHandler
def getGuildByID(guild_id: typing.Union[int]) -> typing.Union[models.Guild]:
    guild = models.Guild.get(models.Guild.guild_id == guild_id)

    return guild


@errors.syncErrorHandler
def getEventTypeByID(guild_id: typing.Union[int], type_id: typing.Union[int]) -> typing.Union[models.EventType]:
    event_type = models.EventType.get((models.EventType.type_id == type_id) & (models.EventType.guild_id == guild_id))

    return event_type


@errors.syncErrorHandler
def getEventByID(guild_id: typing.Union[int], event_id: typing.Union[int]) -> typing.Union[models.Event]:
    event = models.Event.get((models.Event.event_id == event_id) & (models.Event.guild_id == guild_id))

    return event


# Getting Event's and EventType's by MessageID
# 
@errors.syncErrorHandler
def getEventTypeByMessage(guild_id: typing.Union[int], message_id: typing.Union[int], channel_id: typing.Union[int]) -> typing.Union[models.EventType]:
    event_type = models.EventType.get(
        (models.EventType.message_id == message_id) &
        (models.EventType.channel_id == channel_id) &
        (models.EventType.guild_id == guild_id)
    )

    if isinstance(event_type, models.EventType):
        return event_type
    else:
        return None


@errors.syncErrorHandler
def getEventByMessage(guild_id: typing.Union[int], message_id: typing.Union[int], channel_id: typing.Union[int]) -> typing.Union[models.Event]:
    event = models.Event.get(
        (models.Event.message_id == message_id) &
        (models.Event.channel_id == channel_id) &
        (models.Event.guild_id == guild_id)
    )
    
    if isinstance(event, models.Event):
        return event
    else:
        return None

# Creating records
# 
def createNewEventType(
    guild_id: typing.Union[int],
    title: typing.Union[str],
    description: typing.Union[str],
    role_id: typing.Union[int],
    role_color: typing.Union[str],
    enabled: typing.Union[bool],
    created_at,
):
    event_type = models.EventType.create(title=title,description=description,role_id=role_id,role_color=role_color,enabled=enabled,created_at=created_at,guild_id=guild_id)


def createNewEvent(
    guild_id: typing.Union[int],
    type_id: typing.Union[int],
    title: typing.Union[str],
    description: typing.Union[str],
    role_id: typing.Union[int],
    role_color: typing.Union[str],
    enabled: typing.Union[bool],
    created_at,
):
    event = models.Event.create(type_id=type_id,title=title,description=description,role_id=role_id,role_color=role_color,enabled=enabled,created_at=created_at,guild_id=guild_id)



# Updating records
# 
def enableEventType(guild_id: typing.Union[int], type_id: typing.Union[int], started_at, message_id, channel_id, emoji):
    _event_type = models.EventType.update(
        enabled=True,
        started_at=started_at,
        message_id=message_id,
        channel_id=channel_id,
        emoji=emoji
    ).where(
        (models.EventType.type_id == type_id) &
        (models.EventType.guild_id == guild_id)
    ).execute()


def disableEventType(guild_id: typing.Union[int], type_id: typing.Union[int], disabled_at):
    _event_type = models.EventType.update(
        enabled=False,
        disabled_at=disabled_at
    ).where(
        (models.EventType.type_id == type_id) &
        (models.EventType.guild_id == guild_id)
    ).execute()


def enableEvent(guild_id: typing.Union[int], event_id: typing.Union[int], started_at, message_id, channel_id, emoji):
    _event_type = models.Event.update(
        enabled=True,
        started_at=started_at,
        message_id=message_id,
        channel_id=channel_id,
        emoji=emoji
    ).where(
        (models.Event.event_id == event_id) &
        (models.Event.guild_id == guild_id)
    ).execute()


def disableEvent(guild_id: typing.Union[int], event_id: typing.Union[int], disabled_at):
    _event = models.Event.update(
        enabled=False,
        disabled_at=disabled_at
    ).where(
        (models.Event.event_id == event_id) &
        (models.Event.guild_id == guild_id)
    ).execute()


def setNewModRole(guild_id: typing.Union[int], moderator_role_id: typing.Union[int]):
    _guild = models.Guild.update(
        moderator_role_id=moderator_role_id
    ).where(models.Guild.guild_id == guild_id).execute()

# Deleting records
# 
def deleteEventType(guild_id: typing.Union[int], type_id: typing.Union[int]):
    query =  models.EventType.delete().where(
        (models.EventType.type_id == type_id) &
        (models.EventType.guild_id == guild_id)
    )
    query.execute()


def deleteEvent(guild_id: typing.Union[int], event_id: typing.Union[int]):
    query =  models.Event.delete().where(
        (models.Event.event_id == event_id) &
        (models.Event.guild_id == guild_id)
    )
    query.execute()