import typing
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow

from database import models
from .errors import syncErrorHandler


@syncErrorHandler
def createEventsDropdown(records, model: typing.Union[models.Event, models.EventType], max_values: typing.Optional[int] = 1):
    """Creates select options dropdown component for message
    """

    if len(records) > 25:
        records = records[len(records)-25:]

    if  model == models.Event:
        options = [ create_select_option(
            label=f"{event.title[:45]}..",
            value=event.event_id,
            description=f"{event.details[:45]}..",
            emoji=event.emoji
            ) for event in records ]
        placeholder = "Ивент"
    elif model == models.EventType:
        options = [ create_select_option(
            label=f"{event_type.title[:45]}..",
            value=event_type.type_id,
            description=f"{event_type.description[:45]}..",
            emoji=event_type.emoji
            ) for event_type in records ]
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

    
