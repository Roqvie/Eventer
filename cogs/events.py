import typing
from datetime import datetime

import discord
from discord import Embed
from discord import message
from discord import colour
from discord import embeds
from discord import emoji
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.utils.manage_components import wait_for_component
from peewee import Desc

from . import options
from . import decoration
from . import utils
from database import connector, models



class EventType(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    def _have_permission(self, user: discord.User, in_guild: discord.Guild) -> bool:
        """Checks if user has "eventer" or server-owner permission
        """
        guild = connector.getGuildByID(in_guild.id)

        return (guild.moderator_role_id in [role.id for role in user.roles]) or (in_guild.owner == user)
    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Adding event-role to user on reaction.
        """

        # Skipping bot reactions
        if payload.member.bot:
            return

        # Search the event by message id
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id
        event_type = connector.getEventTypeByMessage(guild_id, message_id, channel_id)
        if event_type is None:
            return

        role = discord.utils.get(payload.member.guild.roles, id=event_type.role_id)

        if (payload.event_type == "REACTION_ADD") and (event_type.emoji == str(payload.emoji)):
            # Adding role to user
            await payload.member.add_roles(role)

    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removing event-role to user on reaction.
        """

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        # Skipping bot reactions
        if user.bot:
            return

        # Search the event by message id
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id
        event_type = connector.getEventTypeByMessage(guild_id, message_id, channel_id)
        if event_type is None:
            return

        emoji_id = str(payload.emoji).split(':')[2][:-1]
        role = discord.utils.get(guild.roles, id=event_type.role_id)
        if (payload.event_type == "REACTION_REMOVE") and (event_type.emoji.split(':')[2][:-1] == emoji_id) and (role in user.roles):
            # Remove role from user
            await user.remove_roles(role)


    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="create",
        name="type",
        description="Создание нового вида ивентов",
        options=options.events.EVENT_TYPE_CREATE_OPTION
        )
    async def create(
        self,
        ctx,
        title: typing.Union[str],
        role: typing.Union[str],
        description: typing.Union[str],
        color: typing.Union[str]
    ):
        """Creating new type of events.

        Args:
            title (typing.Union[str]): Title of the new type of events
            role (typing.Union[str]): Role for notifications of new event of this type
            description (typing.Union[str]): Description of the new type of events
            color (typing.Union[str]): Color for notification role
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Creating role
        event_role = await ctx.guild.create_role(name=role, colour=decoration.colors.NAMED[color])

        # Save new event-type in database
        created_at = datetime.now()
        connector.createNewEventType(title=title, role_id=event_role.id, created_at=created_at, description=description, role_color=color, enabled=False, guild_id=ctx.guild.id)

        # Send back info message
        message_payload = [
            {"Название": title, "Описание": description, "Роль": event_role},
            created_at,
            ctx.author.name,
            ctx.author.avatar_url
        ]
        await ctx.send(embed=decoration.embeds.INFO["EVENT_TYPE_CREATED"](*message_payload))


    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="enable",
        name="type",
        description="Активировать новый вид ивентов",
        options=options.events.EVENT_TYPE_ENABLE_OPTION
        )
    async def enable(
        self,
        ctx,
        channel: typing.Union[discord.TextChannel],
        emoji: typing.Optional[str] = "<:bell:874724105037951046>"
    ):
        """Enabling new type of events

        Args:
            channel (typing.Union[discord.TextChannel]): Discord Text Channel for sending notification message
            emoji (typing.Optional[str], optional): Reaction emoji for subscribing to notification of this type of events. Defaults to "<:bell:874724105037951046>".
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Getting events
        event_types = connector.getAllEventTypes(guild_id=ctx.guild.id, enabled=False)

        # Send message with select dropdown for selecting event to activate
        dropdown = utils.createEventsDropdown(records=event_types, model=models.EventType)
        if dropdown is None:
            await ctx.send(embed=decoration.embeds.ERRORS["NO_ITEMS_IN_DROPDOWN"])
            return

        await ctx.send("Выбери тип ивента для активации:", components=[dropdown])
        # Wait for selection
        select_ctx = await wait_for_component(self.bot, components=dropdown)
        selected_event_type_id = int(select_ctx.selected_options[0])
        event_type = connector.getEventTypeByID(guild_id=ctx.guild.id, type_id=selected_event_type_id)

        # Send notification message
        started_at = datetime.now()
        NEW_EVENT = Embed(
            title=event_type.title,
            description=event_type.description,
            color=0x7EBC89
        )
        message = await channel.send(content="@everyone 🟢 Запущен новый тип ивентов!\nДля подписки жми на реакцию", embed=NEW_EVENT)
        await message.add_reaction(emoji)
        
        # Update event type data
        connector.enableEventType(ctx.guild.id, selected_event_type_id, started_at, message.id, channel.id, emoji)

        # Send back info message
        message_payload = [
            {"ID Вида ивента": selected_event_type_id, "Название вида ивента": event_type.title},
            started_at,
            ctx.author.name,
            ctx.author.avatar_url
        ]
        await select_ctx.edit_origin(content="", embed=decoration.embeds.INFO["EVENT_TYPE_ENABLED"](*message_payload), components=None)

    
    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="disable",
        name="type",
        description="Деактивировать вид ивентов"
        )
    async def disable(
        self,
        ctx
    ):
        """Disabling type of events
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Getting events
        event_types = connector.getAllEventTypes(guild_id=ctx.guild.id, enabled=True)

        # Send message with select dropdown for selecting event to activate
        dropdown = utils.createEventsDropdown(event_types, models.EventType, len(event_types[::]))
        if dropdown is None:
            await ctx.send(embed=decoration.embeds.ERRORS["NO_ITEMS_IN_DROPDOWN"])
            return

        await ctx.send("Выбери тип ивента для деактивации:", components=[dropdown])
        # Wait for selection
        select_ctx = await wait_for_component(self.bot, components=dropdown)
        selected_event_type_id = int(select_ctx.selected_options[0])

        disabled_at = datetime.now()
        # Update event type data
        connector.disableEventType(ctx.guild.id, selected_event_type_id, disabled_at)
        event_type = connector.getEventTypeByID(guild_id=ctx.guild.id, type_id=selected_event_type_id)
        
        # Delete message and role
        try:
            channel = ctx.guild.get_channel(event_type.channel_id)
            message = await channel.fetch_message(event_type.message_id)
            await message.delete()
        except:
            pass

        # Send back info message
        message_payload = [
            {"ID Вида ивента": selected_event_type_id, "Название вида ивента": event_type.title},
            disabled_at,
            ctx.author.name,
            ctx.author.avatar_url
        ]
        await select_ctx.edit_origin(content="", embed=decoration.embeds.INFO["EVENT_TYPE_DISABLED"](*message_payload), components=None)


    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="list",
        name="type",
        description="Просмотреть список видов ивентов"
        )
    async def list(
        self,
        ctx
    ):
        """Prints event types list
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Getting events
        event_types = connector.getAllEventTypes(guild_id=ctx.guild.id)
        if len(event_types[::]) == 0:
            await ctx.send(content="```md\nВ данный момент не создано никаких видов ивентов```")
            return

        await ctx.send(content=f"Типы ивентов ({len(event_types)}):")

        for event_type in event_types:
            url = f'https://discord.com/channels/{event_type.guild_id}/{event_type.channel_id}/{event_type.message_id}'
            _message = Embed(
                title=f"**{event_type.title}**ㅤ{event_type.emoji}",
                description=f"Описание: {event_type.description}\nСообщение: [click]({url})\nID Вида ивента: {str(event_type.type_id)}\nАктивирован: {'да' if event_type.enabled else 'нет'}",
                color=0x58b9ff
            )
            await ctx.channel.send(embed=_message)

        
    

    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="delete",
        name="type",
        description="Удалить вид ивентов"
        )
    async def delete(
        self,
        ctx
    ):
        """Deleting type of events
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Getting events
        event_types = connector.getAllEventTypes(guild_id=ctx.guild.id)

        # Send message with select dropdown for selecting event to delete
        dropdown = utils.createEventsDropdown(event_types, models.EventType)
        if dropdown is None:
            await ctx.send(embed=decoration.embeds.ERRORS["NO_ITEMS_IN_DROPDOWN"])
            return

        await ctx.send("Выбери тип ивента(ов) для удаления:", components=[dropdown])
        select_ctx = await wait_for_component(self.bot, components=dropdown)
        await select_ctx.edit_origin(content="Начинаем удаление", embed=None, components=None)

        for event_type_id in list(map(int, select_ctx.selected_options)):
            deleted_at = datetime.now()
            event_type = connector.getEventTypeByID(guild_id=ctx.guild.id, type_id=event_type_id)
            connector.deleteEventType(ctx.guild.id, event_type_id)

            try:
                channel = ctx.guild.get_channel(event_type.channel_id)
                role = ctx.guild.get_role(event_type.role_id)
                message = await channel.fetch_message(event_type.message_id)
                await message.delete()
                await role.delete()
            except:
                pass

            # Send back info message
            message_payload = [
                {"ID Вида ивента": event_type_id, "Название вида ивента": event_type.title},
                deleted_at,
                ctx.author.name,
                ctx.author.avatar_url
            ]
            await ctx.channel.send(content="", embed=decoration.embeds.INFO["EVENT_TYPE_DELETED"](*message_payload), components=None)


class Event(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    def _have_permission(self, user: discord.User, in_guild: discord.Guild) -> bool:
        """Checks if user has "eventer" or server-owner permission
        """
        guild = connector.getGuildByID(in_guild.id)

        return (guild.moderator_role_id in [role.id for role in user.roles]) or (in_guild.owner == user)

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Adding event-role to user on reaction.
        """
 
        guild = self.bot.get_guild(payload.guild_id)
        user = discord.utils.get(guild.members, id=payload.user_id)
        # Skipping bot reactions
        if user.bot:
            return

        # Search the event by message id
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id
        event = connector.getEventByMessage(guild_id, message_id, channel_id)
        if event is None:
            return

        role = discord.utils.get(payload.member.guild.roles, id=event.role_id)

        if (payload.event_type == "REACTION_ADD") and (event.emoji == str(payload.emoji)):
            # Adding role to user
            await payload.member.add_roles(role)
        elif (payload.event_type == "REACTION_REMOVE") and (event.emoji == str(payload.emoji)) and (role in payload.member.roles):
            # Remove role from user
            await payload.member.remove_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Adding event-role to user on reaction.
        """

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        # Skipping bot reactions
        if user.bot:
            return

        # Search the event by message id
        message_id = payload.message_id
        channel_id = payload.channel_id
        guild_id = payload.guild_id
        event = connector.getEventByMessage(guild_id, message_id, channel_id)
        if event is None:
            return

        emoji_id = str(payload.emoji).split(':')[2][:-1]
        role = discord.utils.get(guild.roles, id=event.role_id)
        if (payload.event_type == "REACTION_REMOVE") and (event.emoji.split(':')[2][:-1] == emoji_id) and (role in user.roles):
            # Remove role from user
            await user.remove_roles(role)



    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="create",
        name="event",
        description="Создание нового ивента",
        options=options.events.EVENT_CREATE_OPTION
        )
    async def create(
        self,
        ctx,
        title: typing.Union[str],
        role: typing.Union[str],
        description: typing.Union[str],
        color: typing.Union[str]
    ):
        """Creating new event.

        Args:
            title (typing.Union[str]): Title of the new event
            role (typing.Union[str]): Role for notifications
            description (typing.Union[str]): Description of the new event
            color (typing.Union[str]): Color for notification role
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Getting events
        event_types = connector.getAllEventTypes(guild_id=ctx.guild.id, enabled=True)

        # Send message with select dropdown for selecting event to activate
        dropdown = utils.createEventsDropdown(event_types, models.EventType)
        if dropdown is None:
            await ctx.send(embed=decoration.embeds.ERRORS["NO_ITEMS_IN_DROPDOWN"])
            return

        await ctx.send("Выбери вид, к которому будет относится ивент:", components=[dropdown])
        select_ctx = await wait_for_component(self.bot, components=dropdown)
        selected_event_type_id = int(select_ctx.selected_options[0])

        # Creating role
        event_role = await ctx.guild.create_role(name=role, colour=decoration.colors.NAMED[color])

        # Save new type in database
        created_at = datetime.now()
        connector.createNewEvent(type_id=selected_event_type_id, title=title, description=description, role_id=event_role.id, role_color=color, enabled=False, created_at=created_at, guild_id=ctx.guild.id)

        # Send back info message
        message_payload = [
            {"Название": title,"Описание": description,"Роль": event_role},
            created_at,
            ctx.author.name,
            ctx.author.avatar_url
        ]
        await select_ctx.edit_origin(content="", embed=decoration.embeds.INFO["EVENT_CREATED"](*message_payload), components=None)


    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="enable",
        name="event",
        description="Активировать новый ивент",
        options=options.events.EVENT_ENABLE_OPTION
        )
    async def enable(
        self,
        ctx,
        channel: typing.Union[discord.TextChannel],
        emoji: typing.Optional[str] = "<:bell:874724105037951046>"
    ):
        """Enabling new event

        Args:
            channel (typing.Union[discord.TextChannel]): Discord Text Channel for sending notification message
            emoji (typing.Optional[str], optional): Reaction emoji for subscribing to notifications of this events. Defaults to "<:bell:874724105037951046>".
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Getting events
        events = connector.getAllEvents(guild_id=ctx.guild.id, enabled=False)

        # Send message with select dropdown for selecting event to activate
        dropdown = utils.createEventsDropdown(events, models.Event)
        if dropdown is None:
            await ctx.send(embed=decoration.embeds.ERRORS["NO_ITEMS_IN_DROPDOWN"])
            return

        await ctx.send("Выбери ивент для активации:", components=[dropdown])
        select_ctx = await wait_for_component(self.bot, components=dropdown)
        selected_event_id = int(select_ctx.selected_options[0])
        
        event = connector.getEventByID(guild_id=ctx.guild.id, event_id=selected_event_id)
        event_type = connector.getEventTypeByID(guild_id=ctx.guild.id, type_id=event.type_id)
        event_type_role = discord.utils.get(ctx.guild.roles, id=event_type.role_id)
        started_at = datetime.now()

        # Send notification message
        NEW_EVENT = Embed(
            title=event.title,
            description=event.description,
            color=0x7EBC89
        )
        message = await channel.send(content=f"{event_type_role.mention}, 🟢 Запущен новый ивент!\nДля участия жми на реакцию", embed=NEW_EVENT)
        if emoji is None:
            emoji = "🔔"
        await message.add_reaction(emoji)
        
        # Update event type data
        connector.enableEvent(ctx.guild.id, selected_event_id, started_at, message.id, channel.id, emoji)

        # Send back info message
        message_payload = [
            {"ID ивента": selected_event_id, "Название ивента": event.title, "Тип ивента": event_type.title},
            started_at,
            ctx.author.name,
            ctx.author.avatar_url
        ]
        await select_ctx.edit_origin(content="", embed=decoration.embeds.INFO["EVENT_ENABLED"](*message_payload), components=None)


    
    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="disable",
        name="event",
        description="Деактивировать ивент"
        )
    async def disable(
        self,
        ctx
    ):
        """Disabling event
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Getting events
        events = connector.getAllEvents(guild_id=ctx.guild.id, enabled=True)

        # Send message with select dropdown for selecting event to deactivate
        dropdown = utils.createEventsDropdown(events, models.Event)
        if dropdown is None:
            await ctx.send(embed=decoration.embeds.ERRORS["NO_ITEMS_IN_DROPDOWN"])
            return

        await ctx.send("Выбери ивент для деактивации:", components=[dropdown])
        select_ctx = await wait_for_component(self.bot, components=dropdown)
        selected_event_id = int(select_ctx.selected_options[0])

        # Update event type data
        disabled_at = datetime.now()
        connector.disableEvent(ctx.guild.id, selected_event_id, disabled_at)

        event = connector.getEventByID(guild_id=ctx.guild.id, event_id=selected_event_id)
        # Delete message and role
        try:
            channel = ctx.guild.get_channel(event.channel_id)
            message = await channel.fetch_message(event.message_id)
            await message.delete()
        except:
            pass

        # Send back info message
        message_payload = [
            {"ID ивента": selected_event_id,"Название ивента": event.title},
            disabled_at,
            ctx.author.name,
            ctx.author.avatar_url
        ]
        await select_ctx.edit_origin(content="", embed=decoration.embeds.INFO["EVENT_DISABLED"](*message_payload), components=None)


    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="list",
        name="event",
        description="Просмотреть список ивентов"
        )
    async def list(
        self,
        ctx
    ):
        """Prints events list
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Getting events
        events = connector.getAllEvents(guild_id=ctx.guild.id)
        if len(events) == 0:
            await ctx.send(content="```md\nВ данный момент не создано никаких видов ивентов```")
            return
        
        await ctx.send(content=f"Ивенты ({len(events)}):")

        for event in events:
            url = f'https://discord.com/channels/{event.guild_id}/{event.channel_id}/{event.message_id}'
            _message = Embed(
                title=f"**{event.title}**ㅤ{event.emoji}",
                description=f"Описание: {event.description}\nСообщение: [click]({url})\nID Вида ивента: {event.event_id}\nАктивирован: {'да' if event.enabled else 'нет'}",
                color=0x58b9ff
            )
            await ctx.channel.send(embed=_message)


    @cog_ext.cog_subcommand(
        base="events",
        subcommand_group="delete",
        name="event",
        description="Удалить ивент"
        )
    async def delete(
        self,
        ctx
    ):
        """Deleting events
        """

        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            await ctx.send(embed=decoration.embeds.ERRORS["NO_PERM"])
            return

        # Getting events
        events = connector.getAllEvents(guild_id=ctx.guild.id)

        # Send message with select dropdown for selecting event to activate
        dropdown = utils.createEventsDropdown(events, models.Event, len(events[::]))
        if dropdown is None:
            await ctx.send(embed=decoration.embeds.ERRORS["NO_ITEMS_IN_DROPDOWN"])
            return
            
        await ctx.send("Выбери ивент(ы) для удаления:", components=[dropdown])
        select_ctx = await wait_for_component(self.bot, components=dropdown)
        await select_ctx.edit_origin(content="Начинаем удаление", embed=None, components=None)

        for event_id in list(map(int, select_ctx.selected_options)):
            deleted_at = datetime.now()
            event = connector.getEventByID(guild_id=ctx.guild.id, event_id=event_id)
            connector.deleteEvent(ctx.guild.id, event_id)

            try:
                channel = ctx.guild.get_channel(event.channel_id)
                role = ctx.guild.get_role(event.role_id)
                message = await channel.fetch_message(event.message_id)
                await message.delete()
                await role.delete()
            except:
                pass

            # Send back info message
            message_payload = [
                {"ID ивента": event_id,"Название ивента": event.title},
                deleted_at,
                ctx.author.name,
                ctx.author.avatar_url
            ]
            await ctx.channel.send(content="", embed=decoration.embeds.INFO["EVENT_DELETED"](*message_payload), components=None)
