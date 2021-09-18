"""
Keyboard functionality for the library
"""

from aiogram import types


def keyboard(rows, inline=False):
    """ Make keyboard

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
            return types.InlineKeyboardMarkup()

        return types.ReplyKeyboardRemove()

    # Determine mode
    if isinstance(rows[0][0], dict):
        inline = True

    # Base
    if inline:
        buttons = types.InlineKeyboardMarkup()
    else:
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Filling
    for cols in rows:
        if not inline:
            buttons.add(*[types.KeyboardButton(col) for col in cols])
            continue

        buttons.add(
            *[
                types.InlineKeyboardButton(
                    col['name'],
                    **(
                        {'url': col['data']}
                        if col['data'][:4] == 'http'
                        else {'callback_data': col['data']}
                    ),
                ) for col in cols
            ]
        )

    return buttons
