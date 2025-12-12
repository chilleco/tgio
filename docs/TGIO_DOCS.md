# tgio usage guide

This is a concise, copy-pasteable reference for working with the `tgio` wrapper around `aiogram`. Drop this file into `docs/` of any project that depends on `tgio` so AI/code assistants follow the same conventions.

## What tgio is
- Thin convenience layer over `aiogram` focusing on sending/editing messages with minimal boilerplate.
- Uses `aiogram.Bot` and `aiogram.Dispatcher` internally; you interact through a single `Telegram` class.
- Handles message splitting, keyboard creation, and file preparation automatically.
- Targets Python `>=3.9,<4` and requires `aiogram>=3.23.0`.

## Installation
```bash
pip install tgio
# or, in a repo with a local checkout
pip install .
# dev/test tooling (pytest, pylint, build, twine)
pip install ".[dev]"
```

## Core class
```python
from tgio import Telegram, types

tg = Telegram("<bot_token>")
```

### tg.start
- `await tg.start(on_startup, skip_updates, host, port)` wraps `Dispatcher.start_polling`.
- Does not configure routers/webhooks for you; add them on the dispatcher/bot if needed before calling `start`.

### tg.send
Signature (simplified):
```python
await tg.send(
    chat,                       # int | str | iterable of chats
    text="",                    # optional message text
    buttons=None,               # reply/inline buttons (see "Keyboards")
    inline=False,               # force inline buttons for non-dict input
    files=None,                 # single or multiple files (see below)
    markup="MarkdownV2",        # parse mode; auto-fallback on errors
    preview=False,              # disable link preview by default
    reply=None,                 # message id to reply to
    silent=False,               # disable_notification
)
```
- Returns a list of message IDs (or `None` on fatal API errors). When sending to multiple chats, returns a list per chat.
- Text longer than `4096` is split across multiple messages.
- When sending media, caption text longer than `1024` is split: the first chunk is captioned on the media, the rest are plain messages.
- Multiple media items use `send_media_group`; hard limit of `10` items per call, chunks automatically.
- On `TelegramBadRequest` parse errors, `MarkdownV2` falls back to `Markdown`, then to `None`.

#### Files input
- Single file: pass a dict `{"data": <payload>, "type": "<kind>"}` or just `<payload>` (defaults to type `"image"`).
- Multiple files: pass list/tuple/set of the above.
- Supported `type` values and behavior:
  - `"image"` → photo
  - `"video"` → video
  - `"audio"` → audio (title/performer optional keys)
  - `"animation"` → animation (GIF)
  - `"voice"` → voice
  - `"video_note"` → video note (duration/length optional keys)
  - `"location"` → expects `{"data": {"lat": <float>, "lng": <float>}, "type": "location"}`
  - any other type → document
- Payload shapes:
  - `str` path → `FSInputFile`
  - `str` URL (`http...`) → `URLInputFile`
  - `bytes` → `BufferedInputFile` (auto filename `"file"`)
  - `{"data": <bytes>, "name": "<filename>"}` → named `BufferedInputFile`
  - `io.BufferedReader` → read into bytes buffer

### tg.edit
```python
await tg.edit(chat, message_id, text="", buttons=None, inline=False, files=None, markup="MarkdownV2", preview=False)
```
- For media edits: pass `files` (single or list) and optional `text` as caption. Returns edited message ID or `None`.
- For text-only edits: returns edited message ID.

### tg.rm
```python
await tg.rm(chat, message_or_iterable)
```
- Deletes one or many messages. Returns `False` on known deletion errors; otherwise awaits the bot result.

### tg.check_entry
```python
await tg.check_entry(chat, user)
```
- Returns `True` if the user is `creator/administrator/member`, `False` for other statuses, `None` on errors (e.g., chat not found).

### tg.forward
```python
await tg.forward(chat, from_chat, message_id, silent=False)
```
- Forwards a message; returns forwarded message ID or `0` on API errors like bot blocked.

## Keyboards
Use `buttons` and `inline` in `send`/`edit`:
- `None` → no keyboard change.
- `[]` or `[[]]` → clears keyboard (`ReplyKeyboardRemove` or empty inline).
- Strings / flat list → reply keyboard rows auto-shaped.
- Nested list (e.g., `[[ "Yes", "No" ], ["Maybe"]]`) → reply keyboard grid.
- Inline buttons: pass list(s) of dicts `{"name": "<text>", "data": "<callback or url>"}`; URLs auto-detected if starting with `http` or `tg://`.
- Special inline `"type": "app"` uses `WebAppInfo(url=<data>)`.

## Behavior differences vs using aiogram directly
- One-call convenience: keyboards, parse modes, and file objects are prepared for you.
- Message splitting is automatic for overlong text/captions.
- Returns message IDs (not full aiogram `Message` objects) for easier storage.
- Parse errors auto-downgrade parse mode instead of raising.
- Media groups auto-chunk to Telegram’s 10-item limit.
- Defaults to `disable_web_page_preview=True` unless `preview=True`.

## Practical patterns
```python
# Simple text
await tg.send(123456789, "Hello")

# Inline buttons
await tg.send(
    123456789,
    "Choose:",
    buttons=[[{"name": "Site", "data": "https://example.com"}, {"name": "Ping", "data": "ping"}]],
)

# Multiple photos with a long caption
await tg.send(
    123456789,
    text="Long caption ..." * 2000,           # will be split; first chunk stays as caption
    files=[{"data": "a.jpg", "type": "image"}, {"data": "b.jpg", "type": "image"}],
)

# Edit text with new inline keyboard
await tg.edit(123456789, 42, text="Updated", buttons=[{"name": "OK", "data": "ok"}], inline=True)

# Delete many
await tg.rm(123456789, [10, 11, 12])
```

## Operational notes
- `tgio` currently uses polling; webhooks need manual setup on the underlying `Bot`/`Dispatcher`.
- Logging is minimal; parse failures fall back silently and print to stdout for some API errors.
- Respect Telegram limits: 4096 chars per text message, 1024 chars per caption, 10 items per media group.
- When handling binary data, prefer providing filenames to preserve user-visible names.***
