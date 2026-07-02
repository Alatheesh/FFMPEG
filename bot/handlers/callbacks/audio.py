from pyrogram.types import CallbackQuery

from bot.keyboards.audio import audio_menu
from bot.workspace import workspace


async def audio_router(callback: CallbackQuery):

    data = callback.data
    user_id = callback.from_user.id

    ws = workspace.get(user_id)

    if not ws:
        await callback.answer(
            "Please send a video first.",
            show_alert=True
        )
        return

    # ------------------------------------
    # Open Audio Menu
    # ------------------------------------

    if data == "menu_audio":

        audio_count = len(
            ws.assets.by_type("audio")
        )

        await callback.message.edit_reply_markup(
            reply_markup=audio_menu(audio_count)
        )

        return

    # ------------------------------------
    # Merge Audio
    # ------------------------------------

    if data == "audio_merge":

        ws.state = "waiting_audio_merge"

        await callback.message.reply_text(
            "🎵 Send one or more audio files to merge."
        )

        return

    # ------------------------------------
    # Replace Audio
    # ------------------------------------

    if data == "audio_replace":

        ws.state = "waiting_audio_replace"

        await callback.message.reply_text(
            "🎵 Select the track to replace.\n"
            "(Track selection menu will be added next.)"
        )

        return

    # ------------------------------------
    # Remove Audio
    # ------------------------------------

    if data == "audio_remove":

        ws.state = "waiting_audio_remove"

        await callback.message.reply_text(
            "🎵 Select the audio track(s) to remove."
        )

        return

    # ------------------------------------
    # Swap Audio
    # ------------------------------------

    if data == "audio_swap":

        ws.state = "waiting_audio_swap"

        await callback.message.reply_text(
            "🔀 Choose two tracks to swap."
        )

        return

    # ------------------------------------
    # Rename Track
    # ------------------------------------

    if data == "audio_rename":

        ws.state = "waiting_audio_rename"

        await callback.message.reply_text(
            "🏷 Select the track to rename."
        )

        return

    # ------------------------------------
    # Default Track
    # ------------------------------------

    if data == "audio_default":

        ws.state = "waiting_audio_default"

        await callback.message.reply_text(
            "⭐ Select the default audio track."
        )

        return

    # ------------------------------------
    # Extract Audio
    # ------------------------------------

    if data == "audio_extract":

        ws.state = "waiting_audio_extract"

        await callback.message.reply_text(
            "🎧 Select the track to extract."
        )

        return

    # ------------------------------------
    # Track Information
    # ------------------------------------

    if data == "audio_tracks":

        audios = ws.assets.by_type("audio")

        if not audios:

            await callback.answer(
                "No audio assets available.",
                show_alert=True
            )

            return

        text = "🎵 Audio Assets\n\n"

        for index, asset in enumerate(audios, start=1):

            text += f"{index}. {asset.name}\n"

        await callback.message.reply_text(text)

        return
