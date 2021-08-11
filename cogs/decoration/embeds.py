from discord import Embed


def addFields(embed):

    def wrapper(fields: dict, time, author, author_avatar_url):
        _embed = embed.copy()
        for name, value in fields.items():
            _embed.add_field(name=name, value=value)
        _embed.set_footer(text=f"At {time.strftime('%H:%M:%S, %d.%m.%Y')}")
        _embed.set_author(name=author, icon_url=author_avatar_url)

        return _embed

    return wrapper


HELP_EMBED = Embed(
    title="💁🏻 Помощь по командам",
    color=0x58b9ff
)
HELP_EMBED.description = """
ㅤ
**Виды ивентов**
```cs
[/events create type <название вида ивента> <название роли> <описание вида ивента> <цвет роли> ] - Создание нового вида ивента
[/events enable type <текстовый-канал> <эмодзи>] - Активация вида ивента (отправление сообщения с эмодзи для подписки на этот вид ивентов)
[/events disable] - Деактивирование вида ивентов
[/events list type] - Список всех видов ивентов
[/events delete type] - Удаление вида ивентов
```
**Ивенты**
```cs
[/events create event <название вида ивента> <название роли> <описание вида ивента> <цвет роли> ] - Создание нового ивента
[/events enable event <текстовый-канал> <эмодзи>] - Активация ивента (отправление сообщения с эмодзи для выдачи роли ивента + уведомление по типу ивентов)
[/events disable] - Деактивирование ивента
[/events list event] - Список всех ивентов
[/events delete event] - Удаление ивента
```
**Модерирование**
```cs
[/mods assign eventer <роль>] - Назначение роли ивентеров
```
"""


EVENT_TYPE_CREATED = Embed(
    title="🔜 Создан новый вид ивентов",
    color=0x5AD2F4
)

EVENT_CREATED = Embed(
    title="🔜 Создан новый ивент",
    color=0x02C39A
)

EVENT_TYPE_ENABLED = Embed(
    title="🟢 Активирован новый вид ивентов",
    color=0x5AD2F4
)

EVENT_ENABLED = Embed(
    title="🟢 Активирован новый ивент",
    color=0x02C39A
)

EVENT_TYPE_DISABLED = Embed(
    title="🔴 Деактивирован вид ивентов",
    color=0x5AD2F4
)

EVENT_DISABLED = Embed(
    title="🔴 Деактивирован ивент",
    color=0x02C39A
)

EVENT_TYPE_DELETED = Embed(
    title="🗑️ Удален тип ивентов",
    color=0x5AD2F4
)

EVENT_DELETED = Embed(
    title="🗑️ Удален ивент",
    color=0x02C39A
)


NO_PERM = Embed(
    title="🛡️ У вас нет прав на эту операцию",
    color=0x02C39A
)

NO_ITEMS_IN_DROPDOWN = Embed(
    title="⛔ Количество элементов должно быть в диапазоне от 1 до 25",
    color=0x02C39A
)


INFO = {
    "EVENT_TYPE_CREATED": addFields(EVENT_TYPE_CREATED.copy()),
    "EVENT_TYPE_ENABLED": addFields(EVENT_TYPE_ENABLED.copy()),
    "EVENT_TYPE_DISABLED": addFields(EVENT_TYPE_DISABLED.copy()),
    "EVENT_TYPE_DELETED": addFields(EVENT_TYPE_DELETED.copy()),

    "EVENT_CREATED": addFields(EVENT_CREATED.copy()),
    "EVENT_ENABLED": addFields(EVENT_ENABLED.copy()),
    "EVENT_DISABLED": addFields(EVENT_DISABLED.copy()),
    "EVENT_DELETED": addFields(EVENT_DELETED.copy()),
}

NEW_MOD_ROLE = Embed(
    title="🆕 Установлена роль ивентера",
    color=0x02C39A
)

MODERATE = {
    "NEW_MOD_ROLE": addFields(NEW_MOD_ROLE.copy()),
}

ERRORS = {
    "NO_PERM": NO_PERM,
    "NO_ITEMS_IN_DROPDOWN": NO_ITEMS_IN_DROPDOWN
}