"""
Keyboard functionality for the library
"""

from aiogram import types


def _is_link(data):
    if not data:
        return False
    return data[:4] == "http" or data[:5] == "tg://"


def _get_data(col):
    if col.get("type") == "app":
        return {"web_app": types.WebAppInfo(url=col["data"])}
    if _is_link(col["data"]):
        return {"url": col["data"]}
    return {"callback_data": col["data"]}


def keyboard(rows, inline=False):
    """Make keyboard

    None                → No changes
    [] / [[]]           → Clear keyboard
    [x, y]              → Button column
    [[x, y], [z]]       → Button table
    [[{'data': 'x'}]]   → Inline buttons
    """

    # Empty queries
    if rows is None:
        return None

    # Type formation
    if isinstance(rows, (tuple, set)):
        rows = list(rows)
    elif not isinstance(rows, list):
        rows = [rows]

    # Inner elements formation
    for i, el in enumerate(rows):
        if not isinstance(el, (list, tuple)):
            rows[i] = [el]

    # Clear
    if rows in ([], [[]]):
        if inline:
            return types.InlineKeyboardMarkup(inline_keyboard=[])
        return types.ReplyKeyboardRemove()

    # Determine mode
    if isinstance(rows[0][0], dict):
        inline = True

    # Filling
    buttons = []
    for cols in rows:
        if not inline:
            buttons.append([types.KeyboardButton(text=col) for col in cols])
            continue

        buttons.append(
            [
                types.InlineKeyboardButton(
                    text=col["name"],
                    **_get_data(col),
                )
                for col in cols
            ]
        )

    # Base
    if inline:
        buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    else:
        buttons = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return buttons
