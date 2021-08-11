import typing
import discord_slash
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow

from database import models


def createEventsDropdown(records, model: typing.Union[models.Event, models.EventType], max_values: typing.Optional[int] = 1):

    try:
        if  model == models.Event:
            options = [ create_select_option(label=event.title, value=event.event_id, description=event.details) for event in records ]
            placeholder = "Ивент"
        elif model == models.EventType:
            options = [ create_select_option(label=event_type.title, value=event_type.type_id, description=event_type.description) for event_type in records ]
            placeholder = "Тип ивента"
        else:
            return None
        select = create_select(
            options=options,
            placeholder=placeholder,
            min_values=1,
            max_values=max_values,
        )
        component = create_actionrow(select)

        return component
        
    except discord_slash.error.IncorrectFormat:
        return None

    
