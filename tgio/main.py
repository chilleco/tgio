"""
Library for working with Telegram
"""

import io
from typing import Union, Optional

from aiogram import Bot, Dispatcher, types

# from aiogram.dispatcher.webhook import configure_webhook, StartWebhook
from aiogram.exceptions import AiogramError, TelegramAPIError, TelegramBadRequest
from aiogram.utils.exceptions import ChatNotFound

from ._files import prepare_files, make_attachment
from ._keyboard import keyboard


TEXT_LIMIT = 4096
CAPTION_LIMIT = 1024
FILES_LIMIT = 10


class Telegram:
    def __init__(self, token):
        self.types = types
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        # self.dp.include_router(self.bot.router)  # TODO: need?
        # self.set = self.bot.set_webhook
        # self.start = StartWebhook
        # self.stop = self.bot.delete_webhook

    # pylint: disable=too-many-arguments,too-many-locals,
    # pylint: disable=too-many-return-statements,too-many-branches
    # pylint: disable=too-many-statements
    async def send(
        self,
        chat: Union[int, str, list, tuple, set],
        text: Optional[str] = "",
        buttons: Optional[Union[list, tuple, set, str]] = None,
        inline: Optional[bool] = False,
        files: Optional[
            Union[
                str,
                list,
                tuple,
                set,
                bytes,
                io.BufferedReader,
            ]
        ] = None,
        markup: Optional[str] = "MarkdownV2",
        preview: Optional[bool] = False,
        reply: Optional[Union[int, str]] = None,
        silent: Optional[bool] = False,
    ):
        """Send message"""

        # NOTE: Markup: https://core.telegram.org/bots/api#formatting-options
        # NOTE: ` reply ` doesn't work with multiple images / videos
        # TODO: next_message

        if isinstance(chat, (list, tuple, set)):
            return [
                await self.send(
                    el,
                    text,
                    buttons,
                    inline,
                    files,
                    markup,
                    preview,
                    reply,
                    silent,
                )
                for el in chat
            ]

        try:
            if files:
                files, reserv = prepare_files(files)

                if isinstance(files, list | tuple | set) and len(files) > FILES_LIMIT:
                    messages = []

                    for i in range((len(files) - 1) // FILES_LIMIT + 1):
                        message = await self.send(
                            chat,
                            text,
                            buttons,
                            inline,
                            files[i * FILES_LIMIT : (i + 1) * FILES_LIMIT],
                            markup,
                            preview,
                            reply,
                            silent,
                        )

                        if message is None:
                            return None

                        messages.extend(message)

                    return messages

                if text and len(text) > CAPTION_LIMIT:
                    messages = []

                    message = await self.send(
                        chat,
                        text[:CAPTION_LIMIT],
                        buttons,
                        inline,
                        reserv,
                        markup,
                        preview,
                        reply,
                        silent,
                    )

                    if message is None:
                        return None

                    messages.extend(message)

                    for i in range(1, (len(text) - 1) // CAPTION_LIMIT + 1):
                        message = await self.send(
                            chat,
                            text[i * CAPTION_LIMIT : (i + 1) * CAPTION_LIMIT],
                            buttons,
                            inline,
                            None,
                            markup,
                            preview,
                            reply,
                            silent,
                        )

                        if message is None:
                            return None

                        messages.extend(message)

                    return messages

                if isinstance(files, list):
                    media = [make_attachment(files[0], text, markup)]
                    for el in files[1:]:
                        media.append(make_attachment(el))

                    message = await self.bot.send_media_group(
                        chat,
                        media,
                        disable_notification=silent,
                        reply_to_message_id=reply,
                        allow_sending_without_reply=True,
                    )

                elif files["type"] == "image":
                    message = await self.bot.send_photo(
                        chat,
                        files["data"],
                        caption=text,
                        reply_markup=keyboard(buttons, inline),
                        parse_mode=markup,
                        disable_notification=silent,
                        reply_to_message_id=reply,
                        allow_sending_without_reply=True,
                    )

                elif files["type"] == "video":
                    message = await self.bot.send_video(
                        chat,
                        files["data"],
                        caption=text,
                        reply_markup=keyboard(buttons, inline),
                        parse_mode=markup,
                        disable_notification=silent,
                        reply_to_message_id=reply,
                        allow_sending_without_reply=True,
                    )

                elif files["type"] == "audio":
                    message = await self.bot.send_audio(
                        chat,
                        files["data"],
                        caption=text,
                        title=files.get("title"),
                        performer=files.get("performer"),
                        reply_markup=keyboard(buttons, inline),
                        parse_mode=markup,
                        disable_notification=silent,
                        reply_to_message_id=reply,
                        allow_sending_without_reply=True,
                    )

                elif files["type"] == "animation":
                    message = await self.bot.send_animation(
                        chat,
                        files["data"],
                        caption=text,
                        reply_markup=keyboard(buttons, inline),
                        parse_mode=markup,
                        disable_notification=silent,
                        reply_to_message_id=reply,
                        allow_sending_without_reply=True,
                    )

                elif files["type"] == "voice":
                    message = await self.bot.send_voice(
                        chat,
                        files["data"],
                        caption=text,
                        reply_markup=keyboard(buttons, inline),
                        parse_mode=markup,
                        disable_notification=silent,
                        reply_to_message_id=reply,
                        allow_sending_without_reply=True,
                    )

                elif files["type"] == "video_note":
                    message = await self.bot.send_video_note(
                        chat,
                        files["data"],
                        duration=files.get("duration"),
                        length=files.get("length"),
                        reply_markup=keyboard(buttons, inline),
                        disable_notification=silent,
                        reply_to_message_id=reply,
                        allow_sending_without_reply=True,
                    )

                elif files["type"] == "location":
                    message = await self.bot.send_location(
                        chat,
                        files["data"]["lat"],
                        files["data"]["lng"],
                        reply_markup=keyboard(buttons, inline),
                        disable_notification=silent,
                        reply_to_message_id=reply,
                        allow_sending_without_reply=True,
                    )

                else:
                    message = await self.bot.send_document(
                        chat,
                        files["data"],
                        caption=text,
                        reply_markup=keyboard(buttons, inline),
                        parse_mode=markup,
                        disable_notification=silent,
                        reply_to_message_id=reply,
                        allow_sending_without_reply=True,
                    )

            else:
                reserv = None

                if text and len(text) > TEXT_LIMIT:
                    messages = []

                    for i in range((len(text) - 1) // TEXT_LIMIT + 1):
                        message = await self.send(
                            chat,
                            text[i * TEXT_LIMIT : (i + 1) * TEXT_LIMIT],
                            buttons,
                            inline,
                            reserv,
                            markup,
                            preview,
                            reply,
                            silent,
                        )

                        if message is None:
                            return None

                        messages.extend(message)

                    return messages

                message = await self.bot.send_message(
                    chat,
                    text,
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                    disable_web_page_preview=not preview,
                    disable_notification=silent,
                    reply_to_message_id=reply,
                    allow_sending_without_reply=True,
                )

        except TelegramAPIError as e:
            # CantParseEntities
            if isinstance(e, TelegramBadRequest) and "can't parse entities" in str(e):
                if markup == "MarkdownV2":
                    return await self.send(
                        chat,
                        text,
                        buttons,
                        inline,
                        reserv,
                        "Markdown",
                        preview,
                        reply,
                        silent,
                    )

                return await self.send(
                    chat,
                    text,
                    buttons,
                    inline,
                    reserv,
                    None,
                    preview,
                    reply,
                    silent,
                )

            # (BotBlocked, UserDeactivated, GroupDeactivated)
            print(type(e), str(e))  # FIXME
            return None

        if isinstance(message, (list, tuple)):
            return [el.message_id for el in message]

        return [message.message_id]

    async def edit(
        self,
        chat: Union[int, str],
        message: Union[int, str],
        text: Optional[str] = "",
        buttons: Optional[Union[list, tuple, set, str]] = None,
        inline: Optional[bool] = False,
        files: Optional[
            Union[
                str,
                list,
                tuple,
                set,
                bytes,
                io.BufferedReader,
            ]
        ] = None,
        markup: Optional[str] = "MarkdownV2",
        preview: Optional[bool] = False,
    ):
        """Edit message"""

        # NOTE: 1 file per 1 message

        if files is not None:
            res = None

            if files:
                files, _ = prepare_files(files)

                if isinstance(files, (list, tuple, set)):
                    media = [make_attachment(el) for el in files]
                else:
                    media = make_attachment(files)

                res = await self.bot.edit_message_media(
                    media=media,
                    chat_id=chat,
                    message_id=message,
                    reply_markup=keyboard(buttons, inline),
                )

            if text is not None:
                res = await self.bot.edit_message_caption(
                    chat_id=chat,
                    message_id=message,
                    caption=text,
                    reply_markup=keyboard(buttons, inline),
                    parse_mode=markup,
                )

            return res.message_id if res is not None else None

        message = await self.bot.edit_message_text(
            text=text,
            chat_id=chat,
            message_id=message,
            reply_markup=keyboard(buttons, inline),
            parse_mode=markup,
            disable_web_page_preview=not preview,
        )

        return message.message_id

    async def rm(
        self,
        chat: Union[int, str],
        message: Union[int, str, list, tuple, set],
    ):
        """Delete message"""

        if isinstance(message, (list, tuple, set)):
            return [await self.rm(chat, el) for el in message]

        try:
            return await self.bot.delete_message(chat, message)
        except AiogramError:  # (MessageToDeleteNotFound, MessageCantBeDeleted)
            return False

    async def check_entry(
        self,
        chat: Union[int, str],
        user: Union[int, str],
    ):
        """Check a user entry into a chat"""

        try:
            user_type = await self.bot.get_chat_member(chat, user)
            return user_type.status in ("creator", "administrator", "member")
        except (AiogramError, ChatNotFound):  # (ChatNotFound, BadRequest)
            return None

    async def forward(
        self,
        chat: Union[int, str],
        from_chat: Union[int, str],
        message: Union[int, str],
        silent: Optional[bool] = False,
    ):
        """Forward message"""

        message = await self.bot.forward_message(
            chat,
            from_chat,
            message,
            disable_notification=silent,
        )

        try:
            return message.message_id
        except AiogramError:  # (BotBlocked, UserDeactivated, GroupDeactivated)
            return 0
