import typing
import discord
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow

from database import models
from discord_slash.error import IncorrectFormat


def syncErrorHandler(func):

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except IncorrectFormat:
            return None

    return wrapper


@syncErrorHandler
def createEventsDropdown(
        events: typing.Union[typing.List[models.Event], typing.List[models.Event]],
        model: typing.Union[models.Event, models.EventType],
        max_values: typing.Optional[int] = 1
    ):
    """"Creates select options dropdown component for message.

    Args:
        events (typing.Union[typing.List[models.Event], typing.List[models.Event]]): Events or Event types lsit
        model (typing.Union[models.Event, models.EventType]): Type of event model
        max_values (typing.Optional[int], optional): Maximum count of values to be selected. Defaults to 1.

    Returns:
        message component
    """

    if len(events) > 25:
        events = events[len(events)-25:]

    if  model == models.Event:
        placeholder = "Ивент"
    elif model == models.EventType:
        placeholder = "Тип ивента"

    select = create_select(
        options=_createEventSelectOptions(events),
        placeholder=placeholder,
        min_values=1,
        max_values=max_values,
    )
    component = create_actionrow(select)

    return component


def _createEventSelectOptions(events: typing.Union[typing.List[models.Event], typing.List[models.Event]]) -> list:
    """Creates options for dropdown component

    Args:
        events (typing.Union[typing.List[models.Event], typing.List[models.Event]]): List of events or event types

    Returns:
        list: List with the generated options
    """
    
    options = []
    for event in events:
        label = f"{event.title[:45]}.." if len(event.title) > 45 else f"{event.title}"
        value = event.event_id if isinstance(event, models.Event) else event.type_id
        description = f"{event.description[:45]}.." if len(event.description) > 45 else f"{event.description}"

        # Getting partial emoji
        if ":" in event.emoji and "<" in event.emoji:
            # Discord emoji
            emoji = discord.PartialEmoji(
                name=event.emoji[1:-1].split(':')[1],
                animated=True if event.emoji[1:-1].split(':')[0] == "a" else False,
                id=int(event.emoji[1:-1].split(':')[2])
            )
        else:
            # Unicode emoji
            emoji = event.emoji

        options.append(
            create_select_option(label, value, emoji, description)
        )

    return options



    
