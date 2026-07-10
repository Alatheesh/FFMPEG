from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from engine.models import Workspace
from bot.helpers import format_size

def format_duration(seconds):
    if not seconds:
        return "00:00:00"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def render_dashboard(workspace: Workspace, menu_name="main") -> tuple:
    """
    Renders the dashboard text and keyboard based on current menu and workspace.
    Returns: (text_content, inline_keyboard)
    """
    # Verify if main video exists
    if not workspace.main_video_id or workspace.main_video_id not in workspace.assets:
        text = (
            "🤖 **Welcome to Auto Media Editor!**\n\n"
            "This is a non-destructive media editor. Upload a video file to begin your workspace session."
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Help & Info ℹ️", callback_data="menu#help")]
        ])
        return text, keyboard
        
    video_asset = workspace.assets[workspace.main_video_id]
    meta = video_asset.metadata
    
    # Extract filename outside f-string to avoid syntax error in Python < 3.12 (backslash in f-string)
    video_filename = video_asset.file_path.split('/')[-1].split('\\')[-1]
    
    # 1. Video Overview
    text = (
        "🎬 **Workspace Console**\n"
        "=========================\n"
        f"📂 **File:** `{video_filename}`\n"
        f"📊 **Size:** `{format_size(video_asset.file_size)}` | "
        f"⏱️ **Duration:** `{format_duration(meta.get('duration', 0.0))}`\n"
    )
    
    if meta.get("video_tracks"):
        vt = meta["video_tracks"][0]
        text += f"🎥 **Video:** `{vt.get('codec')}` | `{vt.get('width')}x{vt.get('height')}`\n"
        
    text += "=========================\n\n"
    
    # Render based on current submenu
    if menu_name == "main":
        text += render_main_info(workspace, meta)
        keyboard = build_main_keyboard(workspace)
    elif menu_name == "audio":
        text += render_audio_info(workspace, meta)
        keyboard = build_audio_keyboard(workspace)
    elif menu_name == "subtitle":
        text += render_subtitle_info(workspace, meta)
        keyboard = build_subtitle_keyboard(workspace)
    elif menu_name == "video":
        text += render_video_info(workspace, meta)
        keyboard = build_video_keyboard(workspace)
    elif menu_name == "metadata":
        text += render_metadata_info(workspace, meta)
        keyboard = build_metadata_keyboard(workspace)
    elif menu_name == "settings":
        text += render_settings_info(workspace, meta)
        keyboard = build_settings_keyboard(workspace)
    elif menu_name == "remove_audio_select":
        text += "✏️ **Select an Audio Track to remove from the output:**"
        keyboard = build_track_select_keyboard("remove_audio", meta.get("audio_tracks", []))
    elif menu_name == "remove_sub_select":
        text += "✏️ **Select a Subtitle Track to remove from the output:**"
        keyboard = build_track_select_keyboard("remove_sub", meta.get("subtitle_tracks", []))
    elif menu_name == "burn_sub_select":
        text += "🔥 **Select a Subtitle Track to burn into the video frames:**"
        keyboard = build_track_select_keyboard("burn_sub", meta.get("subtitle_tracks", []))
    elif menu_name == "help":
        text = (
            "📖 **Auto Media Editor Manual**\n\n"
            "• **Non-Destructive Editing**: Queue editing actions across multiple modules (Audio, Subtitles, Cover Art, Metadata). They are only compiled and executed when you press **Export**.\n"
            "• **Undo / Clear**: Easily revert the last action or clear the entire operations queue using the dashboard buttons.\n"
            "• **Output formats**: Toggles between MKV (supports soft subtitles, multiple audio tracks) and MP4 (highly compatible, soft subtitles converted to mov_text or hard-burned)."
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Back to Dashboard ⬅️", callback_data="menu#main")]])
        
    return text, keyboard

# --- Module Specific Renderers ---

def render_main_info(workspace, meta):
    # Lists current state of operations pipeline
    text = "📁 **Current Streams Inventory:**\n"
    text += f"• **Audio Tracks:** `{len(meta.get('audio_tracks', []))}`\n"
    text += f"• **Subtitle Tracks:** `{len(meta.get('subtitle_tracks', []))}`\n\n"
    
    text += "📋 **Queued Operations Pipeline:**\n"
    if not workspace.pipeline:
        text += "_None (No pending edits. Ready to export)_"
    else:
        for idx, op in enumerate(workspace.pipeline):
            op_desc = get_op_description(op, workspace)
            text += f" `{idx+1}.` {op_desc}\n"
            
    text += f"\n⚙️ **Output target:** `{workspace.output_settings['format'].upper()}`"
    if workspace.output_settings["compress"]:
        text += f" | Compression: `{workspace.output_settings['compress']}`"
    text += "\n"
    return text

def render_audio_info(workspace, meta):
    text = "🔊 **Audio Module Console**\n\n"
    text += "**Current Video Audio Tracks:**\n"
    for i, t in enumerate(meta.get("audio_tracks", [])):
        text += f"• `Track {i}:` codec: `{t['codec']}` | lang: `{t['language']}` | title: `\"{t['title']}\"`\n"
    
    # Highlight audio pipeline changes
    audio_ops = [op for op in workspace.pipeline if "audio" in op.op_type or "replace_audio" in op.op_type]
    if audio_ops:
        text += "\n📝 **Queued Audio Actions:**\n"
        for op in audio_ops:
            text += f"- {get_op_description(op, workspace)}\n"
    return text

def render_subtitle_info(workspace, meta):
    text = "📝 **Subtitle Module Console**\n\n"
    text += "**Current Subtitle Tracks:**\n"
    if not meta.get("subtitle_tracks"):
        text += "_No subtitles embedded in original video_\n"
    else:
        for i, t in enumerate(meta.get("subtitle_tracks", [])):
            text += f"• `Track {i}:` codec: `{t['codec']}` | lang: `{t['language']}` | title: `\"{t['title']}\"`\n"
            
    sub_ops = [op for op in workspace.pipeline if "subtitle" in op.op_type or "sub" in op.op_type]
    if sub_ops:
        text += "\n📝 **Queued Subtitle Actions:**\n"
        for op in sub_ops:
            text += f"- {get_op_description(op, workspace)}\n"
    return text

def render_video_info(workspace, meta):
    text = "🎥 **Video Trim & Crop Module**\n\n"
    video_ops = [op for op in workspace.pipeline if "video" in op.op_type or "trim" in op.op_type or "compress" in op.op_type]
    if video_ops:
        text += "**Queued Video Actions:**\n"
        for op in video_ops:
            text += f"- {get_op_description(op, workspace)}\n"
    else:
        text += "No trim or compression presets are queued. Video frames will be copied directly on export (ultra fast)."
    return text

def render_metadata_info(workspace, meta):
    text = "🏷️ **Metadata Customization Console**\n\n"
    meta_ops = [op for op in workspace.pipeline if "metadata" in op.op_type]
    if meta_ops:
        text += "**Pending global metadata values:**\n"
        for op in meta_ops:
            for k, v in op.params.items():
                text += f"• **{k.capitalize()}:** `{v}`\n"
    else:
        text += "Original metadata will be preserved or generated automatically."
    return text

def render_settings_info(workspace, meta):
    text = "⚙️ **Output Container Settings**\n\n"
    text += f"• **Output Container:** `{workspace.output_settings['format'].upper()}`\n"
    text += f"• **Video stream mode:** `{'Transcode/Encode' if workspace.output_settings['compress'] else 'Direct copy'}`\n"
    text += f"• **Audio stream mode:** `{workspace.output_settings['audio_codec'].upper()}`\n"
    return text

# --- Helper Logic ---

def get_op_description(op, workspace):
    op_type = op.op_type
    params = op.params
    if op_type == "replace_audio":
        return f"Replace Audio Track `{params.get('track_index')}` with `{params.get('title')}`"
    elif op_type == "remove_audio":
        return f"Remove Audio Track `{params.get('track_index')}`"
    elif op_type == "add_audio":
        return f"Add external audio track: `{params.get('title')}`"
    elif op_type == "add_subtitle":
        return f"Mux subtitle track: `{params.get('title')}` (`{params.get('language')}`)"
    elif op_type == "remove_subtitle":
        return f"Remove Subtitle Track `{params.get('track_index')}`"
    elif op_type == "burn_subtitle":
        return f"Hardcode/Burn Subtitle Track `{params.get('track_index')}` into video"
    elif op_type == "add_thumbnail":
        return "Inject new thumbnail / video cover art"
    elif op_type == "set_metadata":
        keys = ", ".join(params.keys())
        return f"Set global metadata: `{keys}`"
    elif op_type == "trim_video":
        return f"Trim video from `{format_duration(params.get('start'))}` to `{format_duration(params.get('end'))}`"
    elif op_type == "compress_video":
        return f"Compress video using preset: `{params.get('preset')}`"
    return f"Operation: {op_type}"

# --- Keyboard Builders ---

def build_main_keyboard(workspace: Workspace):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Audio Module 🔊", callback_data="menu#audio"),
            InlineKeyboardButton("Subtitles 📝", callback_data="menu#subtitle")
        ],
        [
            InlineKeyboardButton("Trim / Compress 🎥", callback_data="menu#video"),
            InlineKeyboardButton("Metadata 🏷️", callback_data="menu#metadata")
        ],
        [
            InlineKeyboardButton("Cover Art 🎨", callback_data="action#prompt#add_thumb"),
            InlineKeyboardButton("Container Settings ⚙️", callback_data="menu#settings")
        ],
        [
            InlineKeyboardButton("Undo Last ↩️", callback_data="action#undo"),
            InlineKeyboardButton("Clear All 🗑️", callback_data="action#clear")
        ],
        [
            InlineKeyboardButton("🚀 EXPORT MEDIA 🚀", callback_data="action#export")
        ]
    ])

def build_audio_keyboard(workspace: Workspace):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Replace Track 🔄", callback_data="action#prompt#replace_audio"),
            InlineKeyboardButton("Remove Track ❌", callback_data="menu#remove_audio_select")
        ],
        [
            InlineKeyboardButton("Add Extra Track ➕", callback_data="action#prompt#add_audio")
        ],
        [
            InlineKeyboardButton("Back to Dashboard ⬅️", callback_data="menu#main")
        ]
    ])

def build_subtitle_keyboard(workspace: Workspace):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Add Subtitle ➕", callback_data="action#prompt#add_sub"),
            InlineKeyboardButton("Remove Subtitle ❌", callback_data="menu#remove_sub_select")
        ],
        [
            InlineKeyboardButton("Burn Subtitle (Hardsub) 🔥", callback_data="menu#burn_sub_select")
        ],
        [
            InlineKeyboardButton("Back to Dashboard ⬅️", callback_data="menu#main")
        ]
    ])

def build_video_keyboard(workspace: Workspace):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Trim Range ✂️", callback_data="action#prompt#trim"),
            InlineKeyboardButton("Fast Compression ⚡", callback_data="action#compress#veryfast")
        ],
        [
            InlineKeyboardButton("Medium Compression 🎬", callback_data="action#compress#medium"),
            InlineKeyboardButton("High Compression 🗜️", callback_data="action#compress#slow")
        ],
        [
            InlineKeyboardButton("Back to Dashboard ⬅️", callback_data="menu#main")
        ]
    ])

def build_metadata_keyboard(workspace: Workspace):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Edit Title 📝", callback_data="action#prompt#edit_title"),
            InlineKeyboardButton("Edit Artist 🎤", callback_data="action#prompt#edit_artist")
        ],
        [
            InlineKeyboardButton("Back to Dashboard ⬅️", callback_data="menu#main")
        ]
    ])

def build_settings_keyboard(workspace: Workspace):
    next_fmt = "mp4" if workspace.output_settings["format"] == "mkv" else "mkv"
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"Output Format: {workspace.output_settings['format'].upper()} 🔄", callback_data=f"action#toggle_format#{next_fmt}")
        ],
        [
            InlineKeyboardButton("Back to Dashboard ⬅️", callback_data="menu#main")
        ]
    ])

def build_track_select_keyboard(action_prefix, tracks):
    buttons = []
    for i, t in enumerate(tracks):
        # Format string for selection: Track index, title, lang
        btn_text = f"Track {i}: {t.get('title')} ({t.get('language')})"
        buttons.append([InlineKeyboardButton(btn_text, callback_data=f"action#{action_prefix}#{i}")])
    buttons.append([InlineKeyboardButton("Cancel ❌", callback_data="menu#main")])
    return InlineKeyboardMarkup(buttons)
