import pytest

from . import tg, PATH, USER


@pytest.mark.asyncio
async def test_all():
    # MESSAGE
    # Send message
    mes_ids = await tg.send(USER, "ola")
    assert isinstance(mes_ids, list)
    assert len(mes_ids) == 1

    # Send multiple users
    mes_ids = await tg.send([USER, USER], "ola")
    assert len(mes_ids) == 2
    assert isinstance(mes_ids[0], list)
    assert len(mes_ids[0]) == 1
    assert isinstance(mes_ids[1], list)
    assert len(mes_ids[1]) == 1

    # Send silently
    mes_ids = await tg.send(USER, "ola", silent=True)
    assert len(mes_ids) == 1

    # Send reply
    mes_ids = await tg.send(
        USER,
        "ola",
        reply=(await tg.send(USER, "ola"))[0],
    )
    assert len(mes_ids) == 1

    # Send link
    mes_ids = await tg.send(USER, "https://www.google.ru/")
    assert len(mes_ids) == 1

    # Send link with preview
    mes_ids = await tg.send(USER, "https://www.google.ru/", preview=True)
    assert len(mes_ids) == 1

    # Send too long
    mes_ids = await tg.send(USER, "x" * 4097)
    assert len(mes_ids) == 2

    # MEDIA
    # Send BufferedReader
    with open(f"{PATH}data/test.png", "rb") as file:
        mes_ids = await tg.send(USER, files=file)
    assert len(mes_ids) == 1

    # Send bytes
    with open(f"{PATH}data/test.png", "rb") as file:
        mes_ids = await tg.send(USER, files=file.read())
    assert len(mes_ids) == 1

    # Send path
    mes_ids = await tg.send(USER, files=f"{PATH}data/test.png")
    assert len(mes_ids) == 1

    # Send link
    mes_ids = await tg.send(
        USER, "ola", files="https://s1.1zoom.ru/big0/621/359909-svetik.jpg"
    )
    assert len(mes_ids) == 1

    # Send with caption
    mes_ids = await tg.send(USER, "ola", files=f"{PATH}data/test.png")
    assert len(mes_ids) == 1

    # Send video
    mes_ids = await tg.send(
        USER,
        "ola",
        files={"data": f"{PATH}data/test.mov", "type": "video"},
    )
    assert len(mes_ids) == 1

    # Send BufferedReader video
    with open(f"{PATH}data/test.mov", "rb") as file:
        mes_ids = await tg.send(USER, files={"data": file, "type": "video"})
    assert len(mes_ids) == 1

    # Send link video
    mes_ids = await tg.send(
        USER,
        files={
            "data": "https://github.com/postbird/Mp4ToBlob/blob/master/video/v0-new.mp4?raw=true",
            "type": "video",
        },
    )
    assert len(mes_ids) == 1

    # Send album with caption
    mes_ids = await tg.send(
        USER, "ola", files=[f"{PATH}data/test.png", f"{PATH}data/test.png"]
    )
    assert len(mes_ids) == 2

    # Send mixed types and mixed ways
    with open(f"{PATH}data/test.mov", "rb") as file:
        mes_ids = await tg.send(
            USER,
            "ola",
            files=[
                f"{PATH}data/test.png",
                "https://s1.1zoom.ru/big0/621/359909-svetik.jpg",
                {"data": file, "type": "video"},
            ],
        )
    assert len(mes_ids) == 3

    # Send too many files for album
    mes_ids = await tg.send(
        USER,
        "ola",
        files=[
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
            f"{PATH}data/test.png",
        ],
    )
    assert len(mes_ids) == 20

    # Send bytes video
    with open(f"{PATH}data/test.mov", "rb") as file:
        mes_ids = await tg.send(
            USER,
            "ola",
            files=[f"{PATH}data/test.png", {"data": file.read(), "type": "video"}],
        )
    assert len(mes_ids) == 2

    # Send audio
    mes_ids = await tg.send(
        USER,
        "ola",
        files={"data": f"{PATH}data/test.mp3", "type": "audio"},
    )
    assert len(mes_ids) == 1

    # Send audio with extra info
    mes_ids = await tg.send(
        USER,
        "ola",
        files={
            "data": f"{PATH}data/test.mp3",
            "type": "audio",
            "title": "Название",
            "performer": "Исполнитель",
        },
    )
    assert len(mes_ids) == 1

    # Send animation
    mes_ids = await tg.send(
        USER,
        "ola",
        files={
            "data": "http://techslides.com/demos/sample-videos/small.mp4",
            "type": "animation",
        },
    )
    assert len(mes_ids) == 1

    # Send voice
    mes_ids = await tg.send(
        USER, "ola", files={"data": f"{PATH}data/test.ogg", "type": "voice"}
    )
    assert len(mes_ids) == 1

    # Send video note
    mes_ids = await tg.send(
        USER,
        files={
            "data": f"{PATH}data/test.mp4",
            "type": "video_note",
            "duration": 10,
            "length": 100,
        },
    )
    assert len(mes_ids) == 1

    # Send location
    mes_ids = await tg.send(
        USER,
        files={
            "data": {
                "lat": 59.9392,
                "lng": 30.3165,
            },
            "type": "location",
        },
    )
    assert len(mes_ids) == 1

    # Send document
    mes_ids = await tg.send(
        USER, "ola", files={"data": f"{PATH}data/test.pdf", "type": "document"}
    )
    assert len(mes_ids) == 1

    # Send too long text with file
    mes_ids = await tg.send(USER, "x" * 1025, files=f"{PATH}data/test.png")
    assert len(mes_ids) == 2

    # Send multiple audios
    mes_ids = await tg.send(
        USER,
        "ola",
        files=[
            {"data": f"{PATH}data/test.mp3", "type": "audio"},
            {"data": f"{PATH}data/test.mp3", "type": "audio"},
        ],
    )
    assert len(mes_ids) == 2

    # Send multiple documetns
    mes_ids = await tg.send(
        USER,
        "ola",
        files=[
            {"data": f"{PATH}data/test.pdf", "type": "document"},
            {"data": f"{PATH}data/test.pdf", "type": "document"},
        ],
    )
    assert len(mes_ids) == 2

    # MARKUP
    # Send Markdown
    mes_ids = await tg.send(
        USER,
        "ola *bold* **text** ***bold*** _italic_ __text__ ___italic___ `code` ``text`` ```code```",
        markup="Markdown",
    )
    assert len(mes_ids) == 1

    # Send Markdown 2
    mes_ids = await tg.send(
        USER,
        "ola *bold* _italic_ __underline__ ~strikethrough~ `code`",
    )
    assert len(mes_ids) == 1

    # Send composite Markdown 2
    mes_ids = await tg.send(
        USER,
        "*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*",
    )
    assert len(mes_ids) == 1

    # Send mentions
    mes_ids = await tg.send(
        USER,
        "[mention of a user](tg://user?id=USER) [URL](http://www.example.com/)",
    )
    assert len(mes_ids) == 1

    # Send formatted
    mes_ids = await tg.send(
        USER,
        "```\npre-formatted fixed-width code block\n```",
    )
    assert len(mes_ids) == 1

    # Send code
    mes_ids = await tg.send(
        USER,
        "```python\npre-formatted fixed-width code block written in the Python programming language\n```",
    )
    assert len(mes_ids) == 1

    # Send without markup
    mes_ids = await tg.send(
        USER,
        "ola *ola* _ola_`ola`",
        markup=None,
    )
    assert len(mes_ids) == 1

    # Send HTML
    mes_ids = await tg.send(
        USER,
        "ola <b>bold</b> <strong>bold</strong> <i>italic</i> <em>italic</em> <u>underline</u> <ins>inderline</ins> <s>strikethrough</s> <strike>strikethrough</strike> <del>strikethrough</del> <code>inline fixed-width code</code>",
        markup="HTML",
    )
    assert len(mes_ids) == 1

    # Send composite HTML
    mes_ids = await tg.send(
        USER,
        "<b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>",
        markup="HTML",
    )
    assert len(mes_ids) == 1

    # Send mentions
    mes_ids = await tg.send(
        USER,
        '<a href="tg://user?id=USER">mention of a user</a> <a href="http://www.example.com/">URL</a>',
        markup="HTML",
    )
    assert len(mes_ids) == 1

    # Send formatted
    mes_ids = await tg.send(
        USER,
        "<pre>pre-formatted fixed-width code block</pre>",
        markup="HTML",
    )
    assert len(mes_ids) == 1

    # Send code
    mes_ids = await tg.send(
        USER,
        '<pre><code class="language-pythons">pre-formatted fixed-width code block written in the Python programming language</code></pre>',
        markup="HTML",
    )
    assert len(mes_ids) == 1

    # Send invalid markup
    mes_ids = await tg.send(
        USER,
        "ola <a>ola</b>",
        markup="HTML",
    )
    assert len(mes_ids) == 1

    # Send image with markup
    mes_ids = await tg.send(
        USER,
        "*bold*",
        ["x", "y"],
        files=f"{PATH}data/test.png",
    )
    assert len(mes_ids) == 1

    # Send image with invalid markup
    # NOTE: Recall path after wrong markup
    mes_ids = await tg.send(
        USER,
        "*bold_",
        ["x", "y"],
        files=f"{PATH}data/test.png",
    )
    assert len(mes_ids) == 1

    # Send BufferedReader with invalid markup
    # NOTE: Recall buffer after wrong markup
    with open(f"{PATH}data/test.png", "rb") as file:
        mes_ids = await tg.send(
            USER,
            "*bold_",
            ["x", "y"],
            files=file,
        )
    assert len(mes_ids) == 1

    # BUTTONS
    # Send buttons
    mes_ids = await tg.send(USER, "ola", ["x", "y"])
    assert len(mes_ids) == 1

    # Send table of buttons
    mes_ids = await tg.send(USER, "ola", [["x", "y"], "zo"])
    assert len(mes_ids) == 1

    # Send inline buttons
    mes_ids = await tg.send(
        USER,
        "ola",
        [
            [{"name": "Data", "data": "x"}],
            {"name": "Link", "data": "https://www.google.ru/"},
        ],
    )
    assert len(mes_ids) == 1

    # Send without buttons
    mes_ids = await tg.send(USER, "ola", None)
    assert len(mes_ids) == 1

    # Send with clearing buttons
    mes_ids = await tg.send(USER, "ola", [])
    assert len(mes_ids) == 1

    # EDIT
    # Edit text
    mes_id = await tg.edit(
        USER,
        (
            await tg.send(
                USER,
                "ola",
                [
                    [{"name": "Data", "data": "x"}],
                    {"name": "Link", "data": "https://www.google.ru/"},
                ],
            )
        )[0],
        "ulu",
    )
    assert isinstance(mes_id, int)

    # Edit files
    mes_id = await tg.edit(
        USER,
        (
            await tg.send(
                USER,
                "ola",
                files=f"{PATH}data/test.png",
            )
        )[0],
        "ulu",
        files={"data": f"{PATH}data/test.mov", "type": "video"},
    )
    assert isinstance(mes_id, int)

    # Edit album
    mes_id = await tg.edit(
        USER,
        (
            await tg.send(
                USER,
                "ola",
                files=[f"{PATH}data/test.png", f"{PATH}data/test.png"],
            )
        )[0],
        "ulu",
        files=f"{PATH}data/test.jpeg",
    )
    assert isinstance(mes_id, int)

    # Edit buttons
    mes_id = await tg.edit(
        USER,
        (
            await tg.send(
                USER,
                "ola",
            )
        )[0],
        "ulu",
        [
            [{"name": "Data", "data": "x"}],
            {"name": "Link", "data": "https://www.google.ru/"},
        ],
    )
    assert isinstance(mes_id, int)

    # DELETE
    # Delete message
    res = await tg.rm(
        USER,
        (await tg.send(USER, "ola"))[0],
    )
    assert res == True

    # Delete wrong message
    res = await tg.rm(
        USER,
        [
            (
                (await tg.send(USER, "ola"))[0],
                {123123123},
            ),
        ],
    )
    assert res == [[True, [False]]]

    # CHECK ENTRY
    # Check available chat
    res = await tg.check_entry(-1001142824902, USER)
    assert res == True

    # Check outside user
    res = await tg.check_entry(-1001142824902, 123123123)
    assert res is None

    # Check unavailable chat
    res = await tg.check_entry(0, USER)
    assert res is None

    # FORWARD
    # Forward message
    mes_id = await tg.forward(
        USER,
        USER,
        (await tg.send(USER, "ola"))[0],
    )
    assert isinstance(mes_id, int)

    # MarkdownV2 spec symbols
    # https://core.telegram.org/bots/api#markdownv2-style
    mes_id = await tg.send(USER, ".*test*")
    assert isinstance(mes_id, list)
    assert isinstance(mes_id[0], int)

    mes_id = await tg.send(USER, "Хай! Я помогу тебе 🌴")
    assert isinstance(mes_id, list)
    assert isinstance(mes_id[0], int)
