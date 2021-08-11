import typing
from datetime import datetime

import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, create_button
from discord_slash.utils.manage_components import wait_for_component

from . import options
from . import decoration
from database import connector


class EventsMod(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    def _have_permission(self, user: discord.User, in_guild: discord.Guild) -> bool:
        """Checks if user has "eventer" or server-owner permission
        """
        guild = connector.getGuildByID(in_guild.id)
        
        return (guild.moderator_role_id in [role.id for role in user.roles]) or (in_guild.owner == user)


    @cog_ext.cog_subcommand(
        base="mods",
        subcommand_group="assign",
        name="eventer",
        description="Добавление модераторской роли с полными правами ивентера",
        options=options.moderate.ADD_MODS_ROLE
        )
    async def add(
        self,
        ctx,
        role: discord.Role
    ):
        # Skipping non-eventer users
        if not self._have_permission(ctx.author, ctx.guild):
            return 
        
        # Getting guild and old role
        guild =connector.getGuildByID(ctx.guild.id)
        old_role = ctx.guild.get_role(guild.moderator_role_id) if guild.moderator_role_id else None
        
        # Set new role
        set_at = datetime.now()
        connector.setNewModRole(ctx.guild.id, role.id)
       
        # Send back info message
        payload = {"Новая роль": role.name}
        if old_role:
            payload["Старая роль"] = old_role.name 
        message_payload = [
            payload,
            set_at,
            ctx.author.name,
            ctx.author.avatar_url
        ]
        await ctx.send(embed=decoration.embeds.MODERATE["NEW_MOD_ROLE"](*message_payload), components=None)
