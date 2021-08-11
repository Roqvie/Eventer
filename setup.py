import typing
import discord
from discord import embeds
from discord.embeds import Embed
from discord.ext import commands
from discord_slash import SlashCommand

from cogs import events, moderate
from database import connector
from cogs.decoration.embeds import HELP_EMBED
from settings import BOT


intents = discord.Intents().all()

# Initializing bot
bot = commands.Bot(command_prefix='&', help_command=None, intents=intents)
slash = SlashCommand(bot, sync_commands=True)

# Adding Cogs
bot.add_cog(events.EventType(bot))
bot.add_cog(events.Event(bot))
bot.add_cog(moderate.EventsMod(bot))


@bot.event
async def on_guild_join(guild: discord.Guild):
    connector.addNewGuild(guild.id, guild.name)


@bot.command(name="help")
async def help(ctx):
    await ctx.send(embed=HELP_EMBED)

# Run bot
bot.run() 