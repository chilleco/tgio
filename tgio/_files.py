"""
Files functionality for the library
"""

import io
from copy import deepcopy

from aiogram import types


def prepare_files(files):
    """Prepare a file for single sending"""

    # Multiple files → recursion
    if isinstance(files, (list, tuple, set)):
        data, reserv = zip(*[prepare_files(file) for file in files])
        return list(data), list(reserv)

    # Default type
    if not isinstance(files, dict):
        files = {"data": files, "type": "image"}

    # Without preprocessing
    if files["type"] in {
        "location",
    }:
        return files, files

    # Read stream & cache
    if isinstance(files["data"], io.BufferedReader):
        # if files["type"] in {"video"}:
        #     files["data"] = files["data"].file
        files["data"] = files["data"].read()
    reserv = deepcopy(files)

    # Bytes with custom name
    if isinstance(files["data"], dict):
        files["data"] = types.BufferedInputFile(
            files["data"]["data"], files["data"]["name"]
        )
        return files, reserv

    if isinstance(files["data"], bytes):
        files["data"] = types.BufferedInputFile(
            files["data"], filename="file"
        )  # FIXME: filename
    elif isinstance(files["data"], str) and files["data"][:4] == "http":
        files["data"] = types.URLInputFile(files["data"])
    elif isinstance(files["data"], str):
        files["data"] = types.FSInputFile(files["data"])
    return files, reserv


def make_attachment(file, text=None, markup="MarkdownV2"):
    """Prepare a file for multiple sending"""

    if isinstance(file["data"], str) and file["data"][:4] == "http":
        return file["data"]

    if isinstance(file["data"], bytes):
        file["data"] = io.BytesIO(file["data"])

    if file["type"] == "image":
        return types.InputMediaPhoto(
            media=file["data"],
            caption=text,
            parse_mode=markup,
        )

    if file["type"] == "video":
        return types.InputMediaVideo(
            media=file["data"],
            caption=text,
            parse_mode=markup,
        )

    if file["type"] == "audio":
        return types.InputMediaAudio(
            media=file["data"],
            caption=text,
            title=file.get("title"),
            performer=file.get("performer"),
            parse_mode=markup,
        )

    return types.InputMediaDocument(
        media=file["data"],
        caption=text,
        parse_mode=markup,
    )
