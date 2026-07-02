from pyrogram import filters
from pyrogram.types import CallbackQuery

from bot.client import app
from bot.workspace import workspace
from core.callback_parser import CallbackParser
from core.navigation import navigation


@app.on_callback_query()
async def callback_handler(client, callback: CallbackQuery):

    user_id = callback.from_user.id

    ws = workspace.get(user_id)

    if ws is None:
        await callback.answer(
            "Please upload a video first.",
            show_alert=True
        )
        return

    data = CallbackParser.parse(callback.data)

    # ---------------- Navigation ---------------- #

    if data.category == "home":
        return await home(callback, ws)

    if data.category == "menu":
        return await menu(callback, ws, data)

    # ---------------- Audio ---------------- #

    if data.category == "audio":
        return await audio(callback, ws, data)

    # ---------------- Subtitle ---------------- #

    if data.category == "subtitle":
        return await subtitle(callback, ws, data)

    # ---------------- Video ---------------- #

    if data.category == "video":
        return await video(callback, ws, data)

    # ---------------- Metadata ---------------- #

    if data.category == "metadata":
        return await metadata(callback, ws, data)

    # ---------------- Thumbnail ---------------- #

    if data.category == "thumbnail":
        return await thumbnail(callback, ws, data)

    # ---------------- Export ---------------- #

    if data.category == "export":
        return await export(callback, ws, data)

    # ---------------- Workspace ---------------- #

    if data.category == "workspace":
        return await workspace_menu(callback, ws, data)

    await callback.answer(
        "Unknown action.",
        show_alert=True
    )


# ===================================================
# HOME
# ===================================================

async def home(callback, ws):
    await callback.answer("Home screen coming next.")


# ===================================================
# MENUS
# ===================================================

async def menu(callback, ws, data):
    await callback.answer(
        f"Opening {data.action} menu..."
    )


# ===================================================
# AUDIO
# ===================================================

async def audio(callback, ws, data):
    await callback.answer(
        f"Audio: {data.action}"
    )


# ===================================================
# SUBTITLE
# ===================================================

async def subtitle(callback, ws, data):
    await callback.answer(
        f"Subtitle: {data.action}"
    )


# ===================================================
# VIDEO
# ===================================================

async def video(callback, ws, data):
    await callback.answer(
        f"Video: {data.action}"
    )


# ===================================================
# METADATA
# ===================================================

async def metadata(callback, ws, data):
    await callback.answer(
        f"Metadata: {data.action}"
    )


# ===================================================
# THUMBNAIL
# ===================================================

async def thumbnail(callback, ws, data):

    if data.action == "upload":

        ws.pending_action.set(
            "thumbnail_upload"
        )

        await callback.message.reply_text(
            "🖼 Send the thumbnail image."
        )

        await callback.answer()

        return

    await callback.answer(
        f"Thumbnail: {data.action}"
    )


# ===================================================
# EXPORT
# ===================================================

async def export(callback, ws, data):
    await callback.answer(
        f"Export: {data.action}"
    )


# ===================================================
# WORKSPACE
# ===================================================

async def workspace_menu(callback, ws, data):
    await callback.answer(
        f"Workspace: {data.action}"
    )
