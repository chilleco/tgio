"""
Files functionality for the library
"""

import io
from copy import deepcopy

from aiogram import types


def prepare_files(files):
    """ Prepare a file for single sending """

    if isinstance(files, (list, tuple, set)):
        data, reserv = zip(*[prepare_files(file) for file in files])
        return list(data), list(reserv)

    if not isinstance(files, dict):
        files = {'data': files, 'type': 'image'}

    if files['type'] in {'location',}:
        return files, files

    if isinstance(files['data'], dict):
        reserv = deepcopy(files)
        files['data'] = types.InputFile(
            io.BytesIO(files['data']['data']),
            files['data']['name'],
        )
        return files, reserv

    if not (
        isinstance(files['data'], io.BufferedReader)
        or (isinstance(files['data'], str) and files['data'][:4] != 'http')
    ):
        return files, files

    file = types.InputFile(files['data'])

    if files['type'] in {'video',}:
        files['data'] = file.file.read()
        return files, files

    file = {'name': file.filename, 'data': file.file.read()}
    files['data'] = types.InputFile(io.BytesIO(file['data']), file['name'])

    return files, {'data': file, 'type': files['type']}

def make_attachment(file, text=None, markup='MarkdownV2'):
    """ Prepare a file for multiple sending """

    if isinstance(file['data'], str) and file['data'][:4] == 'http':
        return file['data']

    if isinstance(file['data'], bytes):
        file['data'] = io.BytesIO(file['data'])

    if file['type'] == 'image':
        return types.InputMediaPhoto(
            file['data'],
            caption=text,
            parse_mode=markup,
        )

    if file['type'] == 'video':
        return types.InputMediaVideo(
            file['data'],
            caption=text,
            parse_mode=markup,
        )

    if file['type'] == 'audio':
        return types.InputMediaAudio(
            file['data'],
            caption=text,
            title=file.get('title'),
            performer=file.get('performer'),
            parse_mode=markup,
        )

    return types.InputMediaDocument(
        file['data'],
        caption=text,
        parse_mode=markup,
    )
