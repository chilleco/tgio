"""
Telegram bot Endpoints (Transport level)
"""

from tgio import Telegram


TG_TOKEN = "123456789:AABBCCDDEEFFaabbccddeeff-1234567890"
WEBHOOK_URL = "https://example.com/"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 80


tg = Telegram(TG_TOKEN)


@tg.dp.message_handler()
async def echo(message: tg.types.Message):
    """Main handler"""

    chat = message.chat.id
    text = message.text

    await tg.send(chat, text)


# pylint: disable=unused-argument
async def on_start(dp):
    """Handler on the bot start"""
    await tg.set(WEBHOOK_URL)


if __name__ == "__main__":
    tg.start(
        dispatcher=tg.dp,
        webhook_path="",
        on_startup=on_start,
        # on_shutdown=on_stop,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
