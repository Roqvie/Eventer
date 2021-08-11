from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType


ADD_MODS_ROLE = [
    create_option(
        name="role",
        description="Роль для модераторов",
        option_type=SlashCommandOptionType.ROLE,
        required=True
    ),
]