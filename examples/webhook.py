"""
Telegram bot Endpoints (Transport level)
"""

from tgio import Telegram, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

TG_TOKEN = "123456789:AABBCCDDEEFFaabbccddeeff-1234567890"
WEBHOOK_URL = "https://example.com/"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 80


tg = Telegram(TG_TOKEN)


async def on_startup(dp):
    """Handler on the bot start"""
    await tg.bot.set_webhook(WEBHOOK_URL)


@tg.dp.message_handler()
async def echo(message: types.Message):
    """Main handler"""

    chat = message.chat.id
    text = message.text

    await tg.send(chat, text)


if __name__ == "__main__":
    app = web.Application()
    handler = SimpleRequestHandler(dispatcher=tg.dp, bot=tg.bot)
    handler.register(app, path="")
    setup_application(app, tg.dp, on_startup=on_startup)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
