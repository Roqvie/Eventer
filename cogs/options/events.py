from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.model import SlashCommandOptionType


EVENT_TYPE_CREATE_OPTION = [
    create_option(
        name="title",
        description="Название вида ивентов",
        option_type=SlashCommandOptionType.STRING,
        required=True
    ),
    create_option(
        name="role",
        description="Название роли для подписчиков на вид ивентов",
        option_type=SlashCommandOptionType.STRING,
        required=True
    ),
    create_option(
        name="description",
        description="Описание вида ивентов",
        option_type=SlashCommandOptionType.STRING,
        required=True
    ),
    create_option(
        name="color",
        description="Цвет роли для подписчиков на вид ивентов",
        option_type=SlashCommandOptionType.STRING,
        required=True,
        choices=[
            create_choice(
                name="сине-зелёный",
                value="teal"
            ),
            create_choice(
                name="темно-бирюзовый",
                value="dark_teal"
            ),
            create_choice(
                name="зелёный",
                value="green"
            ),
            create_choice(
                name="темно-зеленый",
                value="dark_green"
            ),
            create_choice(
                name="синий",
                value="blue"
            ),
            create_choice(
                name="темно-синий",
                value="dark_blue"
            ),
            create_choice(
                name="фиолетовый",
                value="purple"
            ),
            create_choice(
                name="темно-фиолетовый",
                value="dark_purple"
            ),
            create_choice(
                name="пурпурный",
                value="magenta"
            ),
            create_choice(
                name="темно-пурпурный",
                value="dark_magenta"
            ),
            create_choice(
                name="золотой",
                value="gold"
            ),
            create_choice(
                name="темно-золотой",
                value="dark_gold"
            ),
            create_choice(
                name="оранжевый",
                value="orange"
            ),
            create_choice(
                name="темно-оранжевый",
                value="dark_orange"
            ),
            create_choice(
                name="красный",
                value="red"
            ),
            create_choice(
                name="темно-красный",
                value="dark_red"
            ),
            create_choice(
                name="светло-серый",
                value="lighter_grey"
            ),
            create_choice(
                name="темно-серый",
                value="dark_grey"
            ),
            create_choice(
                name="сероватый",
                value="light_grey"
            ),
            create_choice(
                name="темно-сероватый",
                value="darker_grey"
            ),
            create_choice(
                name="синий disord",
                value="blurple"
            ),
            create_choice(
                name="серый discord",
                value="greyple"
            ),
            create_choice(
                name="темный discord",
                value="dark_theme"
            ),
        ]
    ),
]

EVENT_TYPE_ENABLE_OPTION = [
    create_option(
        name="channel",
        description="Канал для отправки подписывающего сообщения",
        option_type=SlashCommandOptionType.CHANNEL,
        required=True
    ),
    create_option(
        name="emoji",
        description="Эмодзи для подписывающего сообщения",
        option_type=SlashCommandOptionType.STRING,
        required=False
    )
]

EVENT_CREATE_OPTION = [
    create_option(
        name="title",
        description="Название ивента",
        option_type=SlashCommandOptionType.STRING,
        required=True
    ),
    create_option(
        name="role",
        description="Название роли для участников ивента",
        option_type=SlashCommandOptionType.STRING,
        required=True
    ),
    create_option(
        name="description",
        description="Описание ивента",
        option_type=SlashCommandOptionType.STRING,
        required=True
    ),
    create_option(
        name="color",
        description="Цвет роли для участников ивента",
        option_type=SlashCommandOptionType.STRING,
        required=True,
        choices=[
            create_choice(
                name="сине-зелёный",
                value="teal"
            ),
            create_choice(
                name="темно-бирюзовый",
                value="dark_teal"
            ),
            create_choice(
                name="зелёный",
                value="green"
            ),
            create_choice(
                name="темно-зеленый",
                value="dark_green"
            ),
            create_choice(
                name="синий",
                value="blue"
            ),
            create_choice(
                name="темно-синий",
                value="dark_blue"
            ),
            create_choice(
                name="фиолетовый",
                value="purple"
            ),
            create_choice(
                name="темно-фиолетовый",
                value="dark_purple"
            ),
            create_choice(
                name="пурпурный",
                value="magenta"
            ),
            create_choice(
                name="темно-пурпурный",
                value="dark_magenta"
            ),
            create_choice(
                name="золотой",
                value="gold"
            ),
            create_choice(
                name="темно-золотой",
                value="dark_gold"
            ),
            create_choice(
                name="оранжевый",
                value="orange"
            ),
            create_choice(
                name="темно-оранжевый",
                value="dark_orange"
            ),
            create_choice(
                name="красный",
                value="red"
            ),
            create_choice(
                name="темно-красный",
                value="dark_red"
            ),
            create_choice(
                name="светло-серый",
                value="lighter_grey"
            ),
            create_choice(
                name="темно-серый",
                value="dark_grey"
            ),
            create_choice(
                name="сероватый",
                value="light_grey"
            ),
            create_choice(
                name="темно-сероватый",
                value="darker_grey"
            ),
            create_choice(
                name="синий disord",
                value="blurple"
            ),
            create_choice(
                name="серый discord",
                value="greyple"
            ),
            create_choice(
                name="темный discord",
                value="dark_theme"
            ),
        ]
    ),
]

EVENT_ENABLE_OPTION = [
    create_option(
        name="channel",
        description="Канал для отправки подписывающего сообщения",
        option_type=SlashCommandOptionType.CHANNEL,
        required=True
    ),
    create_option(
        name="emoji",
        description="Эмодзи для подписывающего сообщения",
        option_type=SlashCommandOptionType.STRING,
        required=False
    )
]
