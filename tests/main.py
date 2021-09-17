# For access to TG.io
import sys
import os
sys.path.append(os.getcwd())


import asyncio

from tgio import Telegram


tg = Telegram('123456789:AABBCCDDEEFFaabbccddeeff-1234567890')


async def main():
    # Send message
    print(await tg.send(136563129, 'ola'))
    print(await tg.send([136563129, 136563129], 'ola'))
    print(await tg.send(136563129, 'ola', silent=True))
    print(await tg.send(136563129, 'ola', reply=(await tg.send(136563129, 'ola'))[0]))
    print(await tg.send(136563129, 'https://www.google.ru/'))
    print(await tg.send(136563129, 'https://www.google.ru/', preview=True))
    print(await tg.send(136563129, 'x'*4097))

    # Send media
    ## Buffer
    with open('data/test.png', 'rb') as file:
        print(await tg.send(136563129, files=file))
    ## Bytes
    with open('data/test.png', 'rb') as file:
        print(await tg.send(136563129, files=file.read()))
    ## Path
    print(await tg.send(136563129, files='data/test.png'))
    ## Caption
    print(await tg.send(136563129, 'ola', files='data/test.png'))
    ## URL
    print(await tg.send(136563129, 'ola', files='https://s1.1zoom.ru/big0/621/359909-svetik.jpg'))
    ## Video
    print(await tg.send(136563129, 'ola', files={'data': 'data/test.mov', 'type': 'video'}))
    with open('data/test.mov', 'rb') as file:
        print(await tg.send(136563129, files={'data': file, 'type': 'video'}))
    print(await tg.send(136563129, files={'data': 'https://github.com/postbird/Mp4ToBlob/blob/master/video/v0-new.mp4?raw=true', 'type': 'video'}))
    ## Multi
    print(await tg.send(136563129, 'ola', files=['data/test.png', 'data/test.png']))
    print(await tg.send(136563129, 'ola', files=['data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png', 'data/test.png']))
    with open('data/test.png', 'rb') as file:
        print(await tg.send(136563129, 'ola', files=['data/test.png', 'https://s1.1zoom.ru/big0/621/359909-svetik.jpg', file]))
    print(await tg.send(136563129, 'ola', files=['data/test.png', {'data': 'data/test.mov', 'type': 'video'}]))
    with open('data/test.mov', 'rb') as file:
        print(await tg.send(136563129, 'ola', files=['data/test.png', {'data': file, 'type': 'video'}]))
    with open('data/test.mov', 'rb') as file:
        print(await tg.send(136563129, 'ola', files=['data/test.png', {'data': file.read(), 'type': 'video'}]))
    print(await tg.send(136563129, 'ola', files=[{'data': 'data/test.mp3', 'type': 'audio'}, {'data': 'data/test.mp3', 'type': 'audio'}]))
    print(await tg.send(136563129, 'ola', files=[{'data': 'data/test.pdf', 'type': 'document'}, {'data': 'data/test.pdf', 'type': 'document'}]))
    ## Audio
    print(await tg.send(136563129, 'ola', files={'data': 'data/test.mp3', 'type': 'audio'}))
    print(await tg.send(136563129, 'ola', files={'data': 'data/test.mp3', 'type': 'audio', 'title': 'Название', 'performer': 'Исполнитель'}))
    ## Animation
    print(await tg.send(136563129, 'ola', files={'data': 'http://techslides.com/demos/sample-videos/small.mp4', 'type': 'animation'}))
    ## Voice
    print(await tg.send(136563129, 'ola', files={'data': 'data/test.ogg', 'type': 'voice'}))
    ## Video note
    print(await tg.send(136563129, files={'data': 'data/test.mp4', 'type': 'video_note', 'duration': 10, 'length': 100}))
    ## Location
    print(await tg.send(136563129, files={'data': {'lat': 59.9392, 'lng': 30.3165}, 'type': 'location'}))
    ## Document
    print(await tg.send(136563129, 'ola', files={'data': 'data/test.txt', 'type': 'document'}))
    ## Too long text
    print(await tg.send(136563129, 'x'*1025, files='data/test.png'))

    # Send message with markup
    ## Markdown
    print(await tg.send(136563129, 'ola *bold* **text** ***bold*** _italic_ __text__ ___italic___ `code` ``text`` ```code```', markup='Markdown'))
    ## Markdown 2
    print(await tg.send(136563129, 'ola *bold* _italic_ __underline__ ~strikethrough~ `code`'))
    print(await tg.send(136563129, '*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*'))
    print(await tg.send(136563129, '[mention of a user](tg://user?id=136563129) [URL](http://www.example.com/)'))
    print(await tg.send(136563129, '```\npre-formatted fixed-width code block\n```'))
    print(await tg.send(136563129, '```python\npre-formatted fixed-width code block written in the Python programming language\n```'))
    ## Without markup
    print(await tg.send(136563129, 'ola *ola* _ola_`ola`', markup=None))
    ## HTML
    print(await tg.send(136563129, 'ola <b>bold</b> <strong>bold</strong> <i>italic</i> <em>italic</em> <u>underline</u> <ins>inderline</ins> <s>strikethrough</s> <strike>strikethrough</strike> <del>strikethrough</del> <code>inline fixed-width code</code>', markup='HTML'))
    print(await tg.send(136563129, '<b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>', markup='HTML'))
    print(await tg.send(136563129, '<a href="tg://user?id=136563129">mention of a user</a> <a href="http://www.example.com/">URL</a>', markup='HTML'))
    print(await tg.send(136563129, '<pre>pre-formatted fixed-width code block</pre>', markup='HTML'))
    print(await tg.send(136563129, '<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>', markup='HTML'))
    ## Invalid markup
    print(await tg.send(136563129, 'ola <a>ola</b>', markup='HTML'))
    ## Image & markup
    print(await tg.send(136563129, '*bold*', ['x', 'y'], files='data/test.png'))
    ## Recall path after wrong markup
    print(await tg.send(136563129, '*bold_', ['x', 'y'], files='data/test.png'))
    ## Recall buffer after wrong markup
    with open('data/test.png', 'rb') as file:
        print(await tg.send(136563129, '*bold_', ['x', 'y'], files=file))

    # Send buttons
    print(await tg.send(136563129, 'ola', ['x', 'y']))
    print(await tg.send(136563129, 'ola', [['x', 'y'], 'zo']))
    print(await tg.send(136563129, 'ola', [[{'name': 'Data', 'data': 'x'}], {'name': 'Link', 'data': 'https://www.google.ru/'}]))
    print(await tg.send(136563129, 'ola', None))
    print(await tg.send(136563129, 'ola', []))

    # Edit
    print(await tg.edit(
        136563129,
        (await tg.send(136563129, 'ola', [[{'name': 'Data', 'data': 'x'}], {'name': 'Link', 'data': 'https://www.google.ru/'}]))[0],
        'ulu',
    ))
    print(await tg.edit(
        136563129,
        (await tg.send(136563129, 'ola', files='data/test.png'))[0],
        'ulu',
        files={'data': 'data/test.mov', 'type': 'video'},
    ))
    print(await tg.edit(
        136563129,
        (await tg.send(136563129, 'ola', files=['data/test.png', 'data/test.png']))[0],
        'ulu',
        files='data/test.jpg',
    ))
    print(await tg.edit(
        136563129,
        (await tg.send(136563129, 'ola'))[0],
        'ulu',
        [[{'name': 'Data', 'data': 'x'}], {'name': 'Link', 'data': 'https://www.google.ru/'}],
    ))

    # Delete
    print(await tg.delete(
        136563129,
        (await tg.send(136563129, 'ola'))[0],
    ))
    print(await tg.delete(
        136563129,
        [((await tg.send(136563129, 'ola'))[0], {123123123})],
    ))

    # Check entry
    print(await tg.check_entry(-1001142824902, 136563129))
    print(await tg.check_entry(0, 136563129))

    # Forward
    print(await tg.forward(
        136563129,
        136563129,
        (await tg.send(136563129, 'ola'))[0],
    ))


if __name__ == '__main__':
    asyncio.run(main())
