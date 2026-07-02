from pyrogram import filters
from pyrogram.types import CallbackQuery

from bot.client import app


# --------------------------------------------
# MAIN CALLBACK ROUTER
# --------------------------------------------

@app.on_callback_query()
async def callback_router(client, callback: CallbackQuery):

    data = callback.data

    # Always acknowledge the callback
    await callback.answer()

    # ---------------- Main Menu ---------------- #

    if data == "menu_audio":
        await open_audio_menu(callback)

    elif data == "menu_subtitle":
        await open_subtitle_menu(callback)

    elif data == "menu_video":
        await open_video_menu(callback)

    elif data == "menu_metadata":
        await open_metadata_menu(callback)

    elif data == "menu_container":
        await open_container_menu(callback)

    elif data == "menu_thumbnail":
        await open_thumbnail_menu(callback)

    # ---------------- Audio ---------------- #

    elif data.startswith("audio_"):
        await handle_audio(callback)

    # ---------------- Subtitle ---------------- #

    elif data.startswith("subtitle_"):
        await handle_subtitle(callback)

    # ---------------- Video ---------------- #

    elif data.startswith("video_"):
        await handle_video(callback)

    # ---------------- Metadata ---------------- #

    elif data.startswith("metadata_"):
        await handle_metadata(callback)

    # ---------------- Thumbnail ---------------- #

    elif data.startswith("thumbnail_"):
        await handle_thumbnail(callback)

    # ---------------- Workspace ---------------- #

    elif data == "apply_changes":
        await apply_changes(callback)

    elif data == "clear_workspace":
        await clear_workspace(callback)

    elif data == "cancel_job":
        await cancel_job(callback)

    elif data == "home":
        await go_home(callback)

    else:
        await callback.answer(
            "Unknown action.",
            show_alert=True
        )


# ======================================================
# TEMP PLACEHOLDER FUNCTIONS
# ======================================================

async def open_audio_menu(callback):
    await callback.message.edit_text(
        "🎵 Audio Menu\n\nComing soon."
    )


async def open_subtitle_menu(callback):
    await callback.message.edit_text(
        "💬 Subtitle Menu\n\nComing soon."
    )


async def open_video_menu(callback):
    await callback.message.edit_text(
        "🎥 Video Menu\n\nComing soon."
    )


async def open_metadata_menu(callback):
    await callback.message.edit_text(
        "📝 Metadata Menu\n\nComing soon."
    )


async def open_container_menu(callback):
    await callback.message.edit_text(
        "📦 Container Menu\n\nComing soon."
    )


async def open_thumbnail_menu(callback):
    await callback.message.edit_text(
        "🖼 Thumbnail Menu\n\nComing soon."
    )


async def handle_audio(callback):
    await callback.answer("Audio operation selected.")


async def handle_subtitle(callback):
    await callback.answer("Subtitle operation selected.")


async def handle_video(callback):
    await callback.answer("Video operation selected.")


async def handle_metadata(callback):
    await callback.answer("Metadata operation selected.")


async def handle_thumbnail(callback):
    await callback.answer("Thumbnail operation selected.")


async def apply_changes(callback):
    await callback.answer("Processing will be implemented.")


async def clear_workspace(callback):
    await callback.answer("Workspace cleared.")


async def cancel_job(callback):
    await callback.answer("Cancelled.")


async def go_home(callback):
    await callback.answer("Home.")
